import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from sqlalchemy.orm import Session
from mentor.database import engine
from mentor.prompt import create_agent_system_prompt
from mentor.services import session_service, message_service, progress_service
from mentor.tools import TOOL_DEFINITIONS
from mentor.tools.file_tools import write_workspace_file
from mentor.tools.shell_tools import execute_workspace_command
from mentor.tools.web_tools import web_search, scrape_web_page
from mentor.workspace import list_project_files

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def _handle_complete_milestone(milestone_name: str) -> str:
    success = progress_service.mark_milestone_completed("workspace", milestone_name)
    return f"Milestone '{milestone_name}' marked as completed!" if success else f"Milestone '{milestone_name}' not found."


TOOL_HANDLERS = {
    "write_workspace_file": lambda args: write_workspace_file(args["relative_path"], args["content"]),
    "execute_workspace_command": lambda args: execute_workspace_command(args["command"]),
    "web_search": lambda args: json.dumps(web_search(args["query"], args.get("max_results", 5)), indent=2),
    "scrape_web_page": lambda args: scrape_web_page(args["url"]),
    "complete_milestone": lambda args: _handle_complete_milestone(args.get("milestone_name") or args.get("milestone_id", "")),
}


def execute_tool_call(tool_name: str, args: dict) -> str:
    """Dispatches tool execution using O(1) dictionary lookup."""
    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return f"Unknown tool name: {tool_name}"
    try:
        return handler(args)
    except Exception as e:
        return f"SECURITY ERROR / EXECUTION FAILURE: {e}"


def run_agent_turn(session_id: str, user_input: str) -> str:
    """Executes a full turn in the agent interaction loop and persists to DB."""
    # 1. Load history from DB
    history_msgs = message_service.load_messages(session_id)

    # 2. Build system prompt from mentor/prompt.py with active workspace files
    files = list_project_files()
    file_list_str = "\n".join([f"- {f}" for f in files]) if files else "(No files yet)"
    sys_prompt = create_agent_system_prompt(file_list_str)

    messages = [{"role": "system", "content": sys_prompt}]
    for m in history_msgs:
        messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": user_input})
    message_service.save_message(session_id, "user", user_input)

    # 3. Call LLM (Pass 1)
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        tools=TOOL_DEFINITIONS,
        temperature=0.7,
    )

    msg = response.choices[0].message

    # 4. Handle Tool Calls
    if msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)

            output_str = execute_tool_call(fn_name, fn_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": output_str
            })

        # Pass 2: Send tool results back for final response
        final_resp = client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            messages=messages,
            temperature=0.7,
        )
        final_text = final_resp.choices[0].message.content
        content_to_save = final_text if (final_text and str(final_text).strip() != "") else "[Tool Execution Completed]"
        message_service.save_message(session_id, "assistant", content_to_save)
        return content_to_save
    else:
        final_text = msg.content
        content_to_save = final_text if (final_text and str(final_text).strip() != "") else "[Response Completed]"
        message_service.save_message(session_id, "assistant", content_to_save)
        return content_to_save

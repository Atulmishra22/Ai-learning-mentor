from mentor.llm import get_response
from mentor.manager import ConversationManager
from mentor.progress import ProgressTracker
from mentor.prompt import create_review_prompt
from mentor.utils import check_files_exist, read_file

milestones = [
    "1. Setup & API Connection",
    "2. Conversation Memory",
    "3. Code Review Mode",
    "4. Path Traversal Hardening",
    "5. Progress Tracking Dashboard"
]

tracker = ProgressTracker("AI Mentor Project", milestones)

def main():

    conversation_manager = ConversationManager("conversation.json")

    while True:
        user_input = input("you:").strip()

        if user_input.lower() in ["exit", "quit"]:

            print("Exiting the conversation.")
            break

        elif user_input.lower() in ["reset", "clear"]:

            conversation_manager.reset()
            print("Conversation history has been reset.")
            continue

        elif user_input.startswith("/review"):

            path = user_input.removeprefix("/review").strip()
            if not check_files_exist(path):
                print(f"File '{path}' does not exist or is not a valid file.")
                continue

            read_content = read_file(path)
            conversation_manager.append("user", create_review_prompt(path, read_content))
        elif user_input.startswith("/progress"):

            summary = tracker.get_summary()
            print(summary)
            continue
        elif user_input.startswith("/complete"):
            completed_name = tracker.current
            if tracker.complete_current_milestone():
                print(f"Milestone '{completed_name}' marked as complete.")
            else:
                print("No current milestone to complete.")
            continue


        else:

            conversation_manager.append("user", user_input)

        response = get_response(conversation_manager.conversation)
        print(f"mentor: {response}")

        conversation_manager.append("assistant", response)

if __name__ == "__main__":
    main()

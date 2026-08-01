TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "create_milestones",
            "description": (
                "Creates the complete learning curriculum for a new project by storing an "
                "ordered list of milestones in the database. Call this exactly once after "
                "understanding the user's project requirements and before starting the "
                "learning session. Do NOT call this if milestones already exist for the "
                "project or to modify an existing curriculum. The milestones parameter must "
                "contain the complete ordered curriculum with unique, descriptive milestone "
                "names. This tool only creates milestone records for the active project and "
                "cannot modify conversations, files, or other projects."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Name of the active project. Must match the current learning session."
                        )
                    },
                    "milestones": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": (
                            "Ordered list of milestone names. Example: "
                            "['Setup Environment', 'Conversation Memory', "
                            "'Code Review Mode']."
                        )
                    }
                },
                "required": [
                    "project_name",
                    "milestones"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "complete_milestone",
            "description": (
                "Marks a milestone as completed after verifying that the user has "
                "successfully implemented it. Call this only after reviewing the user's "
                "code, execution results, or other evidence that the milestone is finished. "
                "Do NOT call this based solely on the user's claim without verification. "
                "The milestone_name must exactly match an existing milestone for the active "
                "project. This tool only updates milestone progress and cannot create, "
                "delete, or reorder milestones."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Name of the active project."
                        )
                    },
                    "milestone_name": {
                        "type": "string",
                        "description": (
                            "Exact milestone name to mark as completed."
                        )
                    }
                },
                "required": [
                    "project_name",
                    "milestone_name"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "write_workspace_file",
            "description": (
                "Writes a complete file inside the active project's sandboxed workspace. "
                "Call this to generate starter code, configuration files, documentation, "
                "or tests requested by the user. Do NOT overwrite files containing "
                "user-authored code unless the user explicitly requested the change. "
                "The relative_path must be a workspace-relative path such as 'main.py' "
                "or 'tests/test_api.py'. It must not contain '..', begin with '/', or "
                "contain absolute path components. This tool can only write inside the "
                "project workspace and cannot modify files outside the sandbox."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Name of the active project."
                        )
                    },
                    "relative_path": {
                        "type": "string",
                        "description": (
                            "Workspace-relative file path. Example: "
                            "'mentor/database.py' or 'tests/test_main.py'."
                        )
                    },
                    "content": {
                        "type": "string",
                        "description": (
                            "Complete contents of the file to write."
                        )
                    }
                },
                "required": [
                    "project_name",
                    "relative_path",
                    "content"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "execute_workspace_command",
            "description": (
                "Executes a development command inside the active project's workspace. "
                "Call this after generating or modifying code to verify correctness by "
                "running tests, scripts, or static analysis. Do NOT execute arbitrary shell "
                "commands, destructive operations, package installation commands, or "
                "network-related commands. Only approved development commands such as "
                "'python', 'pytest', 'uv run', 'ruff', or 'mypy' are allowed. The command "
                "must be a single development command and must not use shell chaining, "
                "pipes, redirection, or attempt to access files outside the workspace. "
                "This tool is restricted to the project's sandboxed workspace."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Name of the active project."
                        )
                    },
                    "command": {
                        "type": "string",
                        "description": (
                            "Approved development command. Example: "
                            "'pytest', 'python main.py', or 'uv run pytest'."
                        )
                    }
                },
                "required": [
                    "project_name",
                    "command"
                ]
            }
        }
    }
]
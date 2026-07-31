SYSTEM_PROMPT = """
You are an AI mentor.
You provide concise answers.
You don't write code.
You guide the user by breaking tasks into small steps,
then evaluate their implementation.
"""


def create_review_prompt(path: str, code: str) -> str:
    return f"""
        Please review the following Python file.

        File: {path}

        ```python
        {code}
        ```

        Review it for:

        - Correctness
        - Code quality
        - Best practices
        - Performance
        - Security
        - Maintainability

        Explain every issue and suggest improvements.
        """
from pathlib import Path
from core.ollama_client import chat


INSTRUCTIONS_PATH = Path(__file__).parent.parent / "agents" / "instructions" / "test_run.md"
MODEL = "deepseek-r1:14b"


def _load_system_prompt():
    return INSTRUCTIONS_PATH.read_text()


def _format_failures(test_cases):
    failures = [tc for tc in test_cases if tc['status'] == 'Failed']
    if not failures:
        return None

    lines = []
    for tc in failures:
        lines.append(
            f"- [{tc['classname']}] {tc['name']}: {tc['failure_message']}"
        )
    return "\n".join(lines)


def analyze(test_cases):
    user_message = _format_failures(test_cases)
    if user_message is None:
        return "No failures found in this test run."

    system_prompt = _load_system_prompt()

    return chat(MODEL, system_prompt, user_message)

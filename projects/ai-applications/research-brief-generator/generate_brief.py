import json
import sys
from pathlib import Path


PROMPT_TEMPLATE = """You are preparing an implementation-focused research brief.
Return valid JSON with these fields:
- title
- research_question
- methods
- main_findings
- operational_implications
- equity_notes
- limitations

Paper text:
{paper_text}
"""


def mock_brief(paper_text: str) -> dict:
    lines = [line.strip() for line in paper_text.splitlines() if line.strip()]
    title = lines[0] if lines else "Untitled paper"
    return {
        "title": title,
        "research_question": "What operational problem is the paper trying to solve?",
        "methods": "Mixed-methods or observational design extracted from paper text.",
        "main_findings": [
            "Key finding placeholder based on provided text.",
            "A human reviewer should verify the generated brief before circulation."
        ],
        "operational_implications": [
            "Convert findings into one or two programme actions.",
            "Highlight resource or staffing implications."
        ],
        "equity_notes": "Check whether the paper discusses distributional or low-resource constraints.",
        "limitations": "Generated with the local mock fallback. Replace with provider output for live use."
    }


def call_model(prompt: str) -> dict:
    # Portfolio-safe fallback. Replace with a live provider call when wiring up an API key.
    return mock_brief(prompt)


def main() -> None:
    if len(sys.argv) != 2:
      raise SystemExit("Usage: python generate_brief.py <paper_text_file>")

    input_path = Path(sys.argv[1])
    paper_text = input_path.read_text(encoding="utf-8")
    prompt = PROMPT_TEMPLATE.format(paper_text=paper_text)
    brief = call_model(prompt)
    print(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()

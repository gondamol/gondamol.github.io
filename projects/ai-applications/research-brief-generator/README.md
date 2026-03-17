# Research Brief Generator

LLM-assisted workflow for converting long-form papers into structured implementation briefs.

## Files

- `index.qmd`: portfolio narrative
- `generate_brief.py`: command-line script
- `examples/sample_paper.txt`: example text input
- `examples/sample_brief.json`: example structured output

## Notes

- The script includes a mock fallback so the project structure remains reviewable without an API key.
- Replace the `call_model` function with your preferred provider implementation.

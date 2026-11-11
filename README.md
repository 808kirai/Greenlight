Greenlight

An AI agent that fixes broken dependency upgrade PRs. It reads the failing tests, looks up the library's changelog, writes a patch, and opens a PR once the tests pass.

Where it stands

Early stage. The test runner works, the agent around it is not built yet.

- test_runner.py - Clones a repo at a branch, makes a venv inside it, installs its dependencies from requirements.txt, pyproject.toml or setup.py, runs pytest and returns whether it passed with the output, then deletes the clone
- hello_nemotron.py - Checks the LLM connection by listing the Nemotron models and sending one test message

Planned

- Read the failing test output and the upgrade diff
- Look up the library's changelog for the breaking change
- Write a patch, rerun the tests, and open a PR once they pass

Run it

Needs Python 3.12 or newer and git.

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env

Fill in LLM_BASE_URL and LLM_API_KEY in .env, then:

    python hello_nemotron.py
    python test_runner.py

On Linux or macOS use source .venv/bin/activate and cp instead of copy.

Settings

- `LLM_BASE_URL` - Any OpenAI compatible endpoint
- `LLM_API_KEY` - Key for that endpoint
- `GITHUB_TOKEN`, `TAVILY_API_KEY`, `NEBIUS_API_KEY` - Planned, not used yet

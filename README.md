# Multi-Agent RAG System for CI/CD Pipelines

This project uses AI agents deployed via GitHub Actions to assist with **code generation** and **code reviews** in CI/CD pipelines.

## Project Overview

### Agent 1: Code Generation Agent
- **Trigger:** Manual dispatch, `/generate-code` comment on issues/PRs, GitHub Issue Label, Custom GitHub Action input, Scheduled Runs.
- **Responsibilities:** 
  - Generates or modifies code based on prompts (extracted from issues/PRs).
  - Uses the **Gemini API** for code generation.
  - Commits the generated code to a new branch or creates a PR.
  - Generates using declaration.

---

## Project Structure

- `.github/workflows/` - GitHub Actions workflows for the agents.
- `agents/` - Python scripts for each agent (code generation and review).
- `generated_code/` - Folder for AI-generated code.

---

## Setup

1. **Clone the repo:**

    ```bash
    git clone https://github.com/supergitX/code_generator.git
    cd code_generator
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your secrets:**
    - Add your **Gemini API key** to GitHub secrets: `GEMINI_API_KEY`.
    - This key will be used for code generation via Gemini API.

4. **Configure GitHub Actions:**
    - The workflows (`code_generation.yml`) are pre-configured. You can trigger them manually or based on specific events.

---

## Usage

- **Code Generation Agent:** 
  - Trigger the agent via a `/generate-code` comment on issues/PRs, GitHub Issue Label, or scheduled runs.
  - The generated code will be saved in the `generated_code/` folder.

---

## Contributing

Feel free to fork the repo and submit pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

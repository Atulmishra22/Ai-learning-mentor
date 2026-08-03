# AI Learning Mentor 🚀
### Stack-Agnostic Senior Staff Engineering Coach & Sandboxed Agent Engine

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Playwright](https://img.shields.io/badge/scraping-Playwright-green.svg)](https://playwright.dev/)
[![Typer & Rich](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-magenta.svg)](https://typer.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent, interactive AI engineering mentor designed to guide developers through hands-on, production-grade software engineering projects. Rather than acting as a lazy code generator, **AI Learning Mentor** operates as a **Senior Staff Engineering Coach** — teaching modern industry standards, conducting rigorous code reviews, verifying up-to-date documentation via live web search, and enforcing sandbox security.

---

## 🌟 Key Features

- 🧠 **Stack-Agnostic Mentorship**: Teaches production-grade engineering across any language, framework, or tool (React, Next.js, Python, FastAPI, Node.js, Go, Rust, PostgreSQL, Redis, Docker, CI/CD).
- 🏗️ **Milestone Zero (Professional Scaffolding)**: Teaches company onboarding foundations that self-taught developers often miss — idiomatic module structures, secrets handling (`.env`), linters/formatters (`ruff`/`eslint`), testing setups, Docker containerization, and Conventional Commits.
- 🛡️ **Empirical Red-Team Security Architecture**: Includes multi-layer sandboxing against prompt injection, path traversal, interpreter pivot attacks, and prompt evasion techniques. See our published academic study in [RESEARCH.md](RESEARCH.md).
- 🔍 **Live Double-Engine Web Search & Scraper**: Integrates DuckDuckGo API and headless Playwright Chromium to fetch up-to-date documentation and security advisories before recommending libraries or patterns.
- 💾 **Persistent PostgreSQL Memory**: Automatically saves conversation turns, assistant messages, and learning milestones. Sessions auto-resume across terminal restarts.
- 🖥️ **Interactive Terminal CLI**: Built with `Typer` and `Rich` panels. Features in-session slash commands (`/progress`, `/review [file]`, `/files`, `/help`, `/exit`) so you never have to quit the app to run reviews or check milestones.

---

## 🏛️ System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          INTERACTIVE CLI ROUTER (main.py)                       │
│  Commands: init-db | start | progress | review [file]                          │
│  In-Session: /progress | /review | /files | /help | /exit                       │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      AUTONOMOUS AGENT ENGINE (mentor/agent.py)                  │
│  - System Prompt Generation & Spatial File Awareness (mentor/prompt.py)         │
│  - O(1) Dictionary Tool Call Dispatcher                                         │
│  - 2-Pass LLM Execution Loop (Gemini 3.1 Flash Lite API)                        │
└──────────┬───────────────────────────┬───────────────────────────┬──────────────┘
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌───────────────────────────┐
│  SANDBOXED TOOLS    │    │  LIVE SCRAPER ENGINE│    │   PERSISTENCE LAYER       │
│ - file_tools.py     │    │ - web_tools.py      │    │ - PostgreSQL DB           │
│ - shell_tools.py    │    │   (DDGS + Playwright│    │ - SQLAlchemy 2.0 ORM      │
│ - workspace.py      │    │    Chromium + BS4)   │    │ - sessions/messages/      │
│   (Path Sandboxing) │    └─────────────────────┘    │   progresstable           │
└─────────────────────┘                               └───────────────────────────┘
```

---

## ⚙️ Getting Started

### 1. Prerequisites
- Python `>= 3.12`
- `uv` package manager (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- PostgreSQL database instance

### 2. Environment Setup
Clone the repository and copy the environment configuration template:

```bash
git clone https://github.com/your-username/ai-mentor.git
cd ai-mentor
cp .env.example .env
```

Update your `.env` file with your credentials:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_mentor_db
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install Dependencies
Synchronize dependencies using `uv`:

```bash
uv sync
uv run playwright install chromium
```

### 4. Initialize Database
Create PostgreSQL database tables:

```bash
uv run python main.py init-db
```

*(To reset tables to a clean state at any time, run `uv run python main.py init-db --force`)*.

---

## 🚀 Usage Guide

### Starting an Interactive Mentoring Session

Launch the continuous chat session:

```bash
uv run python main.py start
```

- **Resuming Sessions**: The app automatically auto-resumes your most recent session and conversation memory from PostgreSQL!
- **Starting a Fresh Session**: To start a brand new session, run:
  ```bash
  uv run python main.py start --new
  ```

### In-Session Slash Commands

Inside the active chat (`👤 You >`), you can use slash commands without quitting the app:

- **`/progress`**: Renders a Rich table of your current learning milestones and completion status.
- **`/review [file]`**: Performs a production-grade AI code review. If no file is specified, it auto-detects all workspace files and conducts a **Full Project Architecture Review**!
- **`/files`**: Lists all active non-ignored files in `workspace/`.
- **`/help`**: Displays available in-session commands.
- **`/exit`**: Exits the chat loop cleanly.

---

## 🔬 Security Research & Red-Team Paper

This project includes an extensive empirical security study on securing LLM tool access against prompt injection, context framing attacks, secondary channel pivots, and content scanner evasions.

- 📄 Read the full academic study: **[RESEARCH.md](RESEARCH.md)**
- 🔬 View empirical lab notes & raw execution traces: **[docs/security_research.md](docs/security_research.md)**

---

## 🧪 Automated Testing

Run the unit and integration test suite (covering workspace sandboxing, path traversal prevention, file handlers, and security whitelists):

```bash
uv run pytest
```

```text
============================= 14 passed in 0.21s ==============================
```

---

## 📁 Repository Structure

```text
ai-mentor/
├── main.py                        # Typer CLI Router & Interactive Chat Session Loop
├── mentor/
│   ├── agent.py                   # Autonomous Agent Engine & Tool Dispatcher
│   ├── prompt.py                  # Stack-Agnostic System & Code Review Prompts
│   ├── workspace.py               # Single Workspace Manager & Path Sandboxing
│   ├── database/                  # SQLAlchemy 2.0 ORM Models & Engine
│   ├── services/                  # Database Repositories (sessions, messages, progress)
│   └── tools/                     # Sandboxed Tool Handlers (file, shell, web)
├── tests/                         # Pytest Suite & Red-Team Benchmark Scripts
├── docs/
│   └── security_research.md       # Empirical Lab Notes & Trace Logs
├── RESEARCH.md                    # Academic Red-Team Security Research Paper
├── pytest.ini                     # Pytest Configuration
└── pyproject.toml                 # UV Project Dependencies & Metadata
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

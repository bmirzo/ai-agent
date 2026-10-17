# AI Agent

A command-line AI coding agent built with Python, the OpenAI SDK, and OpenRouter. Inspired by tools like Claude Code and Cursor, this project demonstrates how an LLM can interact with a codebase, execute tools, and iteratively solve coding tasks.

## Features

- **File Inspection** — List files and directories.
- **File Reading** — Read file contents.
- **File Writing** — Create or modify files.
- **Python Execution** — Run Python scripts and inspect their output.
- **Agent Loop** — Let the LLM call tools iteratively until the task is completed.

## Tech Stack

- Python 3.10+
- OpenAI Python SDK
- OpenRouter API
- uv

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bmirzo/ai-agent.git
   cd ai-agent
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file and add your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Usage

Run the agent with a coding task:

```bash
uv run main.py "Fix my calculator app"
```

The agent can inspect files, read and write code, execute Python scripts, and use the results to continue working toward a solution.

## Purpose

Built as part of the [Boot.dev](https://www.boot.dev/) *Build an AI Agent* project to explore tool calling, LLM-powered workflows, and the fundamentals of agentic AI.
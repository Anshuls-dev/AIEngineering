# AI Engineering

My hands-on log of learning LLM engineering: calling frontier and open-source models, building small AI tools, and working up to RAG, agents and evaluation.

I'm a software engineer with 10+ years of experience (banking, automotive), moving into AI engineering. This repo tracks what I build along the way.

> Coursework is based on Ed Donner's [LLM Engineering](https://github.com/ed-donner/llm_engineering) course. Files adapted from the course are credited in their headers. My own additions are marked below.

## What's here

| File | What it does |
|---|---|
| `WebPageScrapingOpenAI.ipynb` | Scrapes a web page and summarises it with an OpenAI model, using system and user prompts |
| `WebPageScrapingOllama.ipynb` | Calls the OpenAI API three ways (raw HTTP with `requests`, the SDK, and a local model through Ollama's OpenAI-compatible endpoint), then runs the same summariser on local models (`llama3.2`, `deepseek-r1`) |
| `solution.py` | Day 2 exercise as a command-line script: summarises a page with a local Ollama model (`uv run solution.py <url> --model llama3.2`), stripping `<think>` blocks from reasoning models |
| `scraper.py` | Fetches a page's title and text with `requests` and BeautifulSoup (adapted from the course) |

## What I've learned so far

- **Chat completions API:** the `messages` format (`system` / `user` roles) that most LLM providers share
- **Prompting basics:** the system prompt sets task and tone, the user prompt carries the input
- **Frontier vs local models:** OpenAI in the cloud vs Ollama on my own machine, with the same client code by changing `base_url`
- **Practical limits:** simple scraping fails on JavaScript-rendered sites and bot-protected pages, and reasoning models like `deepseek-r1` return `<think>` blocks that need stripping

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Anshuls-dev/AIEngineering.git
cd AIEngineering
uv sync
```

Create a `.env` file in the project root (it's git-ignored):

```
OPENAI_API_KEY=sk-proj-...
```

For local models, install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull llama3.2
```

Then open the notebooks in Cursor or VS Code and select the `.venv` kernel.

## Progress

- [x] Week 1, Day 1: first API call, website summariser
- [x] Week 1, Day 2: raw HTTP vs SDK, local models with Ollama
- [ ] My own project: incident-ticket summariser that switches between OpenAI and Ollama with a single parameter, comparing quality and speed
- [ ] RAG
- [ ] Agents and tool calling
- [ ] Evaluation and deployment

## Tech

Python · OpenAI API · Ollama · BeautifulSoup · uv · Jupyter

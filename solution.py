"""
Day 2 exercise: summarise a web page with an open-source model running locally via Ollama
instead of OpenAI. Adapted from Ed Donner's LLM Engineering course (week 1, day 1 and day 2).

Usage:
    uv run solution.py [url] [--model MODEL]
"""

import argparse
import re

import requests
from openai import OpenAI

from scraper import fetch_website_contents


OLLAMA_URL = "http://localhost:11434"
OLLAMA_BASE_URL = f"{OLLAMA_URL}/v1"
DEFAULT_MODEL = "llama3.2"
DEFAULT_URL = "https://www.theverge.com/"

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]


def strip_thinking(text):
    """Reasoning models like deepseek-r1 prefix their answer with a <think>...</think> block"""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def check_ollama(model):
    """Fail early with a helpful message if Ollama isn't running or the model isn't pulled"""
    try:
        tags = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5).json()
    except requests.ConnectionError:
        raise SystemExit("Ollama isn't running - start it with `ollama serve`")
    installed = {m["name"] for m in tags.get("models", [])}
    if model not in installed and f"{model}:latest" not in installed:
        raise SystemExit(f"Model {model} isn't installed - run `ollama pull {model}`")


def summarize(url, model=DEFAULT_MODEL):
    website = fetch_website_contents(url)
    response = ollama.chat.completions.create(
        model=model,
        messages=messages_for(website)
    )
    return strip_thinking(response.choices[0].message.content)


def main():
    parser = argparse.ArgumentParser(description="Summarise a web page using a local Ollama model")
    parser.add_argument("url", nargs="?", default=DEFAULT_URL, help=f"page to summarise (default: {DEFAULT_URL})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model to use (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    check_ollama(args.model)
    print(f"Summarising {args.url} with {args.model}...\n")
    print(summarize(args.url, args.model))


if __name__ == "__main__":
    main()

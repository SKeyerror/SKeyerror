#!/usr/bin/env python3
"""Refresh the "Anime Quote of the Day" block in README.md from AnimeChan.

Idempotent: on API failure it leaves the current quote untouched and exits 0,
so the workflow never fails just because the free API is having a bad day.
"""
import json
import pathlib
import re
import sys
import time
import urllib.request

API = "https://api.animechan.io/v1/quotes/random"
START, END = "<!-- ANIME-QUOTE:START -->", "<!-- ANIME-QUOTE:END -->"


def fetch(retries: int = 3) -> dict | None:
    err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API, headers={"User-Agent": "SKeyerror-profile-readme"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                payload = json.load(resp)
            if payload.get("status") == "success":
                return payload["data"]
            err = payload
        except Exception as exc:  # noqa: BLE001 - any failure just means "retry"
            err = exc
        time.sleep(3 * (attempt + 1))
    print(f"animechan unavailable, keeping the current quote: {err}")
    return None


def md_escape(text: str) -> str:
    return re.sub(r"([*_`~\[\]])", r"\\\1", text.strip())


def render(data: dict) -> str:
    content = md_escape(data["content"])
    anime = data["anime"]
    title = md_escape(anime["name"])
    alt = anime.get("altName")
    if alt and alt != anime["name"]:
        title += f" ({md_escape(alt)})"
    character = md_escape(data["character"]["name"])
    return f"> 「{content}」\n>\n> — **{character}**, *{title}*"


def main() -> int:
    data = fetch()
    if data is None:
        return 0
    readme = pathlib.Path("README.md")
    text = readme.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r"\n.*?\n" + re.escape(END), re.S)
    if not pattern.search(text):
        print("quote markers not found in README.md", file=sys.stderr)
        return 1
    new = pattern.sub(lambda _: f"{START}\n{render(data)}\n{END}", text)
    if new != text:
        readme.write_text(new, encoding="utf-8")
        print("updated quote:", data["content"][:60])
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Image generation via Pexels API (free stock photos)."""
from __future__ import annotations

import os
import random
import time
from pathlib import Path

import httpx

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

STYLE_SUFFIX = ""  # Not used for Pexels but kept for compatibility

DEFAULT_NEGATIVE = ""  # Not used for Pexels but kept for compatibility

# Finance-related fallback keywords if prompt search returns nothing
FALLBACK_QUERIES = [
    "stock market", "money", "finance", "business", "gold",
    "economy", "investment", "wealth", "banking", "corporate"
]


def full_visual_prompt(scene: str, style_suffix: str | None = None) -> str:
    """Extract keywords from scene description for Pexels search."""
    return scene.strip()


def _extract_search_query(prompt: str) -> str:
    """Extract 2-3 key words from image prompt for Pexels search."""
    # Remove style suffixes and extract core subject
    clean = prompt.split(",")[0].strip()
    # Take first 5 words max
    words = clean.split()[:5]
    return " ".join(words)


def _pexels_search(
    query: str,
    *,
    api_key: str,
    per_page: int = 15,
) -> list[str]:
    """Search Pexels and return list of image URLs."""
    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "square",
    }

    with httpx.Client(timeout=30.0) as client:
        resp = client.get(PEXELS_SEARCH_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        photos = data.get("photos", [])
        if not photos:
            return []
        return [p["src"]["large"] for p in photos]


def _download_image(url: str, api_key: str) -> bytes:
    """Download image from URL."""
    headers = {"Authorization": api_key}
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.content


def save_scene_image(
    index: int,
    prompt: str,
    out_path: Path,
    *,
    width: int = 768,
    height: int = 768,
    negative: str = DEFAULT_NEGATIVE,
) -> tuple[str, str]:
    """Search Pexels for relevant image and save it. Returns (status, detail)."""
    api_key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not api_key:
        return "fail", "PEXELS_API_KEY not set"

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Extract search query from prompt
    query = _extract_search_query(prompt)

    try:
        # Try the specific query first
        urls = _pexels_search(query, api_key=api_key)

        # Fall back to finance keywords if no results
        if not urls:
            fallback = random.choice(FALLBACK_QUERIES)
            print(f"      Pexels: no results for '{query}', trying '{fallback}'")
            urls = _pexels_search(fallback, api_key=api_key)

        if not urls:
            return "fail", f"Pexels: no images found for '{query}'"

        # Pick a different image per index for variety
        url = urls[index % len(urls)]

        img_bytes = _download_image(url, api_key)
        out_path.write_bytes(img_bytes)
        print(f"      Pexels image saved (query: '{query}')")
        return "ok", "pexels"

    except Exception as e:
        # Try fallback on any error
        try:
            fallback = random.choice(FALLBACK_QUERIES)
            urls = _pexels_search(fallback, api_key=api_key)
            if urls:
                url = urls[index % len(urls)]
                img_bytes = _download_image(url, api_key)
                out_path.write_bytes(img_bytes)
                print(f"      Pexels fallback image saved (query: '{fallback}')")
                return "ok", "pexels-fallback"
        except Exception:
            pass
        return "fail", str(e)

"""Image generation via Pollinations.ai (free, no API key required)."""
from __future__ import annotations

import time
import urllib.parse
from pathlib import Path

import httpx

STYLE_SUFFIX = (
    ", cinematic photography, dramatic lighting, ultra detailed, "
    "8k, sharp focus, professional camera, financial aesthetic, "
    "moody contrast, depth of field, no text, no captions, no watermark, no logos"
)

DEFAULT_NEGATIVE = (
    "blurry, low quality, watermark, logo, text, title, signature, ugly, grainy, "
    "cartoon, anime, illustration, gore, blood, nudity, child-unsafe"
)


def full_visual_prompt(scene: str, style_suffix: str | None = None) -> str:
    """Combine the scene description with a channel-specific style suffix."""
    return f"{scene.strip()}{(style_suffix or STYLE_SUFFIX)}"


def _pollinations_generate(
    prompt: str,
    *,
    width: int = 768,
    height: int = 768,
    seed: int | None = None,
    max_retries: int = 5,
) -> bytes:
    """Call Pollinations.ai and return raw image bytes."""
    encoded_prompt = urllib.parse.quote(prompt)

    params = {
        "width": width,
        "height": height,
        "nologo": "true",
        "model": "flux",
    }
    if seed is not None:
        params["seed"] = seed

    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        for attempt in range(1, max_retries + 1):
            try:
                resp = client.get(url, params=params)

                if resp.status_code == 429:
                    wait = 20 * attempt
                    print(f"      Pollinations rate limit — waiting {wait}s (attempt {attempt}/{max_retries})...")
                    time.sleep(wait)
                    continue

                if resp.status_code == 503:
                    wait = 15 * attempt
                    print(f"      Pollinations unavailable — waiting {wait}s (attempt {attempt}/{max_retries})...")
                    time.sleep(wait)
                    continue

                if resp.status_code == 402:
                    raise RuntimeError("Pollinations 402 — feature not available on free tier")

                resp.raise_for_status()

                content_type = resp.headers.get("content-type", "")
                if "image" in content_type:
                    print(f"      Pollinations image done (attempt {attempt})")
                    return resp.content

                raise RuntimeError(f"Unexpected response: {resp.status_code} {resp.text[:200]}")

            except httpx.TimeoutException:
                wait = 10 * attempt
                print(f"      Pollinations timeout — waiting {wait}s (attempt {attempt}/{max_retries})...")
                time.sleep(wait)
                continue

        raise RuntimeError(f"Pollinations failed after {max_retries} attempts")


def save_scene_image(
    index: int,
    prompt: str,
    out_path: Path,
    *,
    width: int = 768,
    height: int = 768,
    negative: str = DEFAULT_NEGATIVE,
) -> tuple[str, str]:
    """Generate and save one image. Returns (status, detail)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    seed = 1000 + index * 137

    try:
        img_bytes = _pollinations_generate(
            prompt,
            width=width,
            height=height,
            seed=seed,
        )
        out_path.write_bytes(img_bytes)
        return "ok", "pollinations"
    except Exception as e:
        return "fail", str(e)

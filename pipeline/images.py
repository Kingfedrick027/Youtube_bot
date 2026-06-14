"""Image generation via HuggingFace Inference API (free tier)."""
from __future__ import annotations

import os
import time
from pathlib import Path

import httpx

HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

STYLE_SUFFIX = (
    ", cinematic digital illustration, detailed scene art, strong composition, "
    "professional youtube visual quality, no text, no captions, no watermark, no logos"
)

DEFAULT_NEGATIVE = (
    "blurry, low quality, watermark, logo, text, title, signature, ugly, grainy, "
    "gore, blood, nudity, child-unsafe"
)


def full_visual_prompt(scene: str, style_suffix: str | None = None) -> str:
    """Combine the scene description with a channel-specific style suffix."""
    return f"{scene.strip()}{(style_suffix or STYLE_SUFFIX)}"


def _hf_generate(
    prompt: str,
    *,
    api_key: str,
    negative_prompt: str = DEFAULT_NEGATIVE,
    width: int = 768,
    height: int = 768,
    max_retries: int = 5,
) -> bytes:
    """Call HuggingFace Inference API and return raw image bytes."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "image/png",
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        },
    }

    with httpx.Client(timeout=120.0) as client:
        for attempt in range(1, max_retries + 1):
            resp = client.post(HF_API_URL, json=payload, headers=headers)

            # Model still loading — wait and retry
            if resp.status_code == 503:
                wait = 20 * attempt
                print(f"      HF model loading — waiting {wait}s (attempt {attempt}/{max_retries})…")
                time.sleep(wait)
                continue

            # Rate limited — wait and retry
            if resp.status_code == 429:
                wait = 30 * attempt
                print(f"      HF rate limit — waiting {wait}s (attempt {attempt}/{max_retries})…")
                time.sleep(wait)
                continue

            resp.raise_for_status()

            content_type = resp.headers.get("content-type", "")
            if "image" in content_type:
                print(f"      HF image done (attempt {attempt})")
                return resp.content

            # Unexpected response
            raise RuntimeError(f"HF unexpected response: {resp.status_code} {resp.text[:200]}")

        raise RuntimeError(f"HF failed after {max_retries} attempts")


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
    api_key = os.environ.get("HF_TOKEN", "").strip()
    if not api_key:
        return "fail", "HF_TOKEN not set"

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        img_bytes = _hf_generate(
            prompt,
            api_key=api_key,
            negative_prompt=negative,
            width=width,
            height=height,
        )
        out_path.write_bytes(img_bytes)
        return "ok", "huggingface"
    except Exception as e:
        return "fail", str(e)

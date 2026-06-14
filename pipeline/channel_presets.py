"""Channel niches: system prompt + defaults for Groq script generation.

Each preset includes a topic_pool — a list of setting/situation ideas.
One is picked randomly per run if no --topic is provided, ensuring variety.
"""

from __future__ import annotations

from typing import TypedDict


class Variant(TypedDict, total=False):
    """One output variant — same images, different audio/subs/upload target."""
    lang: str  # "en", "hi", etc. used as key in Groq response
    label: str  # human-readable for logs
    tts_voice: str  # Edge TTS voice (e.g. "hi-IN-MadhurNeural")
    caption_font: str  # font filename inside assets/fonts/
    caption_font_name: str  # FFmpeg-visible font family name
    yt_token_env: str  # env var name for YouTube refresh token (e.g. "YT_REFRESH_TOKEN_HI")
    min_words: int  # min word count for narration validation


class ChannelPreset(TypedDict, total=False):
    id: str
    label: str
    groq_system_hint: str
    segment_count: int  # images + script beats
    topic_pool: list[str]
    image_style_suffix: str  # appended to every image prompt
    image_negative_prompt: str  # passed as negative prompt
    # Single-variant fields (backward compat — used when `variants` is absent):
    language: str
    tts_voice: str
    caption_font: str
    caption_font_name: str
    min_words: int  # min word count for narration validation (single-variant)
    # Multi-variant mode — Groq returns translations for each lang, pipeline renders+uploads per variant.
    variants: list[Variant]
    # topic_rotation: "myth" → pipeline/myth_topics.py (IST day theme + no-repeat within theme)
    topic_rotation: str
    # Single-variant YouTube upload: which env var holds this channel's refresh token
    yt_token_env: str
    # Extra uploads: same MP4 uploaded to additional channels using these env var names
    extra_yt_token_envs: list[str]


PRESETS: dict[str, ChannelPreset] = {
   "finance_facts": {
        "id": "finance_facts",
        "label": "Dark Money & Finance Facts (bilingual — Hindi + English)",
        "variants": [
            {
                "lang": "hi",
                "label": "Hindi",
                "tts_voice": "hi-IN-MadhurNeural",
                "caption_font": "NotoSansDevanagari-Bold.ttf",
                "caption_font_name": "Noto Sans Devanagari",
                "yt_token_env": "YT_REFRESH_TOKEN_HI",
                "min_words": 80,
            },
            {
                "lang": "en",
                "label": "English",
                "tts_voice": "en-US-GuyNeural",
                "caption_font": "BebasNeue-Regular.ttf",
                "caption_font_name": "Bebas Neue",
                "yt_token_env": "YT_REFRESH_TOKEN_EN",
                "min_words": 70,
            },
        ],
        "groq_system_hint": (
            "You write punchy YouTube Shorts about shocking money facts, billionaire secrets, "
            "dark side of wealth, and financial truths nobody teaches in school. "
            "STRUCTURE: hook with a shocking money fact in opening, 3 developed beats with real examples, "
            "strong closing line that makes people think. "
            "TONE: confident, eye-opening, slightly controversial but factually grounded. "
            "Never give investment advice. Use 'historically' or 'reportedly' when needed. "
            "No hashtags inside narration. Original phrasing only. "
            "IMAGE PROMPT RULE: write image prompts in ENGLISH only. Describe real photographs or cinematic stills. "
            "Use real-world subjects — stock exchanges, cash, gold, luxury, corporations, charts. "
            "NEVER write 'cartoon', 'illustration', 'anime', or 'stylized'. "
            "Examples: 'aerial view of Wall Street New York at night with lights', "
            "'close-up of gold bars stacked in a vault with dramatic lighting', "
            "'wide shot of a stock market crash screen with red numbers'. "
            "BILINGUAL RULE: same story expressed naturally in each language — not word-for-word translation. "
            "HINDI LENGTH: aim ~150 Devanagari words, rich detail, ~55-70 seconds spoken. "
            "ENGLISH LENGTH: aim 120-155 English words, hook + 3-4 beats + strong close, ~40-50 seconds spoken."
        ),
        "segment_count": 5,
        "image_style_suffix": (
            ", photorealistic cinematic photography, dramatic lighting, ultra detailed, "
            "8k, sharp focus, professional camera, financial aesthetic, "
            "moody contrast, depth of field, no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "cartoon, anime, illustration, painting, drawing, sketch, 3d render, cgi, "
            "stylized, flat colors, low quality, blurry, watermark, logo, text, signature, "
            "deformed, ugly, extra limbs"
        ),
        "topic_pool": [
            # Billionaires & Wealth
            "how Mukesh Ambani built his empire", "dark secrets of the Tata family",
            "how Elon Musk really made his first million", "the Rothschild family conspiracy",
            "how Jeff Bezos crushed competitors", "the real story of Warren Buffett",
            "billionaires who lost everything overnight", "how old money hides wealth",
            "the Adani rise explained", "dark side of the Walmart family",
            "how billionaires pay zero tax legally", "the real cost of being a billionaire",
            "richest people in history adjusted for inflation", "how royals stay rich forever",
            "self-made billionaires who started with nothing",
            # Dark Side of Money
            "how banks create money from nothing", "the truth about credit card companies",
            "how insurance companies make billions off you", "dark side of microfinance in India",
            "how payday loans trap poor people", "the real reason inflation happens",
            "how the 2008 financial crisis was caused", "the truth about pyramid schemes",
            "how MLM companies work", "dark side of stock market manipulation",
            "how hedge funds short stocks", "the real story of Harshad Mehta",
            "the Satyam scandal explained", "how ponzi schemes collapse",
            "dark side of real estate in India",
            # Money Psychology
            "why poor people stay poor", "the psychology of impulse buying",
            "why lottery winners go broke", "how rich people think differently",
            "the real reason you can't save money", "lifestyle inflation explained",
            "why most people never invest", "the psychology of debt",
            "how social media makes you spend more", "why we undervalue future money",
            "the truth about get rich quick schemes", "how advertising manipulates spending",
            "why most businesses fail in year one", "the sunk cost trap explained",
            "why people fear the stock market",
            # Financial Systems
            "how the Federal Reserve controls the world", "what happens when a country goes broke",
            "the truth about gold as an investment", "how cryptocurrency really works",
            "dark side of Bitcoin", "how tax havens work",
            "how the IMF controls poor countries", "the petrodollar system explained",
            "how China is buying the world", "dark side of foreign aid",
            "how wars are funded", "the real cost of corruption in India",
            "how black money works in India", "the hawala system explained",
            "how demonetization really affected India",
            # Hustle & Business
            "businesses that print money quietly", "how to think like an entrepreneur",
            "dark side of startup culture", "how Amazon destroyed small businesses",
            "the truth about passive income", "how dropshipping really works",
            "dark side of influencer marketing", "how franchises trap business owners",
            "the real story of McDonald's business model", "how Apple keeps you buying",
            "dark side of fast fashion economics", "how Zara dominates retail",
            "the business of fear and insurance", "how hospitals make money",
            "dark side of the pharmaceutical industry",
            # India Money Stories
            "how the East India Company looted India", "India's GDP story explained",
            "the real value of gold in Indian households", "chit funds explained",
            "how Indian farmers get trapped in debt", "the business of weddings in India",
            "how real estate black money works in India", "India's richest kings in history",
            "the Nizam of Hyderabad's wealth", "how Dhirubhai Ambani started from zero",
            "the rise of Zerodha", "dark side of Indian banking",
            "how UPI changed India's economy", "the business of IPL",
            "India's informal economy explained",
        ],
    },

def list_channel_ids() -> list[str]:
    return sorted(PRESETS.keys())


def get_preset(channel_id: str) -> ChannelPreset:
    key = channel_id.strip().lower().replace("-", "_")
    if key not in PRESETS:
        raise KeyError(f"Unknown channel preset {channel_id!r}. Try: {', '.join(list_channel_ids())}")
    return PRESETS[key]

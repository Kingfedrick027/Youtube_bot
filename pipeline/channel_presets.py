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
    "facts": {
        "id": "facts",
        "label": "Mind-blowing facts Short (bilingual — Hindi + English)",
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
            "You write punchy YouTube Shorts about surprising, verified facts — in MULTIPLE languages. "
            "The same fact will be published as separate videos on different language channels. "
            "STRUCTURE: hook fact in opening, supporting facts in the middle, punchline + takeaway at end. "
            "TONE: energetic, curious, confident. No clickbait lies. "
            "Each fact must be broadly accurate; if unsure, use safer wording like "
            "'scientists believe' or 'some research suggests'. "
            "No medical advice. No hashtags inside narration. Original phrasing only. "
            "IMAGE PROMPT RULE: write image prompts in ENGLISH only. Describe real photographs or documentary stills. "
            "Use real-world subjects, real lighting, real environments. NEVER write 'cartoon', 'illustration', "
            "'anime', or 'stylized'. Examples: 'a real octopus underwater in clear blue ocean, sunlight rays', "
            "'close-up macro photo of a honeybee on a yellow flower', "
            "'wide shot of Saturn V rocket launching at night with flames'. "
            "BILINGUAL RULE: the SAME story/facts must be expressed naturally in each language — "
            "do not literally translate word-for-word; rephrase so each version sounds native and flows well. "
            "HINDI LENGTH: variants.hi.full_narration should be long-form — "
            "aim ~150 Devanagari words (acceptable band roughly 135-170) with rich detail and connective phrases "
            "so the Hindi voiceover is substantial (~55-70 seconds). "
            "ENGLISH LENGTH: variants.en.full_narration must be long-form too — "
            "aim 120-155 English words (never a short teaser); include hook, 3-4 developed beats with examples, "
            "and a strong closing line so the English voiceover is ~40-50 seconds."
        ),
        "segment_count": 5,
        "image_style_suffix": (
            ", photorealistic documentary photography, cinematic lighting, ultra detailed, "
            "8k, sharp focus, professional camera, National Geographic style, realistic textures, "
            "natural colors, depth of field, no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "cartoon, anime, illustration, painting, drawing, sketch, 3d render, cgi, "
            "stylized, flat colors, low quality, blurry, watermark, logo, text, signature, "
            "deformed, ugly, extra limbs, mutated"
        ),
        "topic_pool": [
            # Space & Universe
            "black holes", "neutron stars", "Mars mysteries", "Moon secrets", "exoplanets",
            "the Big Bang", "dark matter", "the asteroid belt", "Saturn's rings",
            "Jupiter's storms", "sounds in space", "dead stars", "parallel universes",
            "time dilation", "cosmic radiation", "space colonies", "SETI and alien signals",
            "the Voyager probe", "sun facts", "galaxy collisions", "space weather",
            "quantum physics weirdness", "multiverse theory", "wormholes",
            "the edge of the observable universe",
            # Animals & Nature
            "deep sea creatures", "parasites that control minds", "animal superpowers",
            "extinct animals", "animals that basically can't die",
            "venomous creatures of India", "crow intelligence", "the octopus brain",
            "the mantis shrimp", "tardigrades", "animal sleep habits", "migration mysteries",
            "camouflage masters", "animals that mourn their dead", "bioluminescence",
            "carnivorous plants", "fungi intelligence", "ant colonies", "whale communication",
            "spider silk science", "the immortal jellyfish", "animal self-medication",
            "dolphin language", "electric eels", "naked mole rats", "bird navigation",
            "snake facts", "insects you didn't know exist", "animals in Indian forests",
            "microorganisms living in your body",
            # Human Body & Psychology
            "brain illusions", "the science of sleep paralysis", "memory tricks",
            "the placebo effect", "pain tolerance", "human senses you didn't know about",
            "DNA secrets", "the gut-brain connection", "adrenaline effects",
            "the subconscious mind", "phobias explained", "the science of dreams",
            "body language secrets", "why we laugh", "human evolution oddities",
            "the science of aging", "near-death experiences", "hypnosis facts",
            "déjà vu explained", "emotional memory", "synesthesia", "muscle memory",
            "the fear response", "the science of addiction", "human body record breakers",
            # History & Civilizations
            "Ancient Egypt secrets", "dark facts about the Roman Empire", "lost civilizations",
            "medieval torture devices", "ancient Indian empires", "Mughal secrets",
            "forgotten inventions", "unknown facts about World War 2", "Cold War spy stories",
            "Greek myths debunked", "real Viking history", "the Aztec civilization",
            "the Indus Valley mystery", "the Maurya Empire", "the Chola naval empire",
            "the history of slavery", "ancient medicines", "the oldest cities on Earth",
            "ancient trade routes", "Genghis Khan facts", "the real Cleopatra",
            "Alexander the Great", "dark facts about British India",
            "untold partition of India stories", "ancient Chinese secrets",
            "the real life of samurai", "real pirate history", "the Byzantine Empire",
            "the Ottoman Empire", "ancient astronomy",
            # India Specific
            "India's unsolved mysteries", "cursed places in India",
            "unknown Indian inventions", "weird Indian laws",
            "dark stories from Indian mythology", "haunted forts of India",
            "untold Indian freedom fighters", "India's richest kings in history",
            "origin stories of Indian street food", "India's rarest animals",
            "Indian space program facts", "the engineering of ancient temples",
            "India's tribal cultures", "Bollywood dark secrets",
            "India's geographical oddities", "mysteries of Indian rivers",
            "Indian martial arts", "underground cities of India",
            "India's hottest and coldest places", "facts about Indian languages",
            # Money & Power
            "the richest people in history", "how billionaires think",
            "the dark side of corporations", "famous stock market crashes",
            "consequences of money printing", "heists gone wrong",
            "underground economies", "tax havens explained",
            "the richest countries in history", "failed currencies",
            "the gold standard", "dark stories from crypto", "the mafia economy",
            "war profiteering", "untold stories of India's richest businessmen",
            "how banks really work", "money psychology", "poverty traps",
            "famous economic collapses", "the dark side of diamonds",
            # Science & Tech
            "when AI went wrong", "internet dark secrets", "nuclear energy facts",
            "genetic engineering", "CRISPR experiments", "lab-grown meat",
            "deepfake technology", "social media algorithms", "dark web facts",
            "surveillance technology", "robot evolution", "battery technology secrets",
            "shocking climate science facts", "plastic in the human body",
            "microwave radiation", "5G facts vs myths", "quantum computing",
            "the history of bioweapons", "chemical reactions gone wrong",
            "future technology predictions",
            # Food & Substances
            "foods your brain is addicted to", "the dark side of sugar",
            "fast food secrets", "spices that changed history",
            "poisonous foods we eat daily", "the science of fermentation",
            "caffeine deep dive", "the science of alcohol",
            "the spiciest things on Earth", "food frauds worldwide",
            "ancient recipes still used today", "rare foods only the rich eat",
            "the history of Indian spices", "foods banned around the world",
            "GMO food facts",
            # Crime & Dark Secrets
            "unsolved murders", "serial killer psychology",
            "cults that shocked the world", "government experiments on humans",
            "corporate cover-ups", "art heists", "counterfeit economies",
            "organized crime facts", "famous prison escapes",
            "cold cases solved by DNA", "the biggest cyber crimes ever",
            "assassination plots", "whistleblower stories",
            "the dark side of Hollywood", "scams that fooled millions",
            "human trafficking networks", "drug cartel economics",
            "facts about corrupt governments", "identity theft stories",
            "history of con artists",
            # Wildcards
            "dreams that predicted the future", "coincidences too weird to be real",
            "things banned in other countries", "phobias with unpronounceable names",
            "world records that sound fake", "the science of optical illusions",
            "superstitions with real origins", "things that didn't exist 20 years ago",
            "urban legends debunked", "numbers with dark histories",
        ],
    },
    "hindi_myth": {
        "id": "hindi_myth",
        "label": "Hindi mythology & devotion Shorts (Ganesha → Shiva → … by IST day)",
        "topic_rotation": "myth",
        "language": "hi",
        "min_words": 100,
        "tts_voice": "hi-IN-SwaraNeural",
        "caption_font": "NotoSansDevanagari-Bold.ttf",
        "caption_font_name": "Noto Sans Devanagari",
        "yt_token_env": "YT_REFRESH_TOKEN_MYTH",
        "extra_yt_token_envs": ["YT_REFRESH_TOKEN_MYTH_2"],
        "groq_system_hint": (
            "You write respectful Hindi Shorts about Indian mythology, epics, and devotion — for a general audience. "
            "LANGUAGE: full_narration, youtube_title, youtube_description entirely in Devanagari Hindi. "
            "IMAGE PROMPTS: English only — cinematic scene descriptions (no text in image). "
            "CRITICAL LENGTH: full_narration 105-135 Devanagari words (~40-50 sec spoken). "
            "Tone: warm, storytelling, reverent — NOT mocking faith. Retell traditional narratives in your own words; "
            "do not copy long scripture passages. PG-13, no graphic gore, no hate toward any group. "
            "No hashtags in narration. The creator gives a specific story angle in the user message — stay on that topic."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", cinematic Indian mythology digital painting, golden hour lighting, rich jewel tones, "
            "detailed divine atmosphere, epic composition, respectful devotional art style, "
            "high quality illustration, no text, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "photorealistic human face close-up as real celebrity, gore, blood, horror jumpscare, "
            "disrespectful parody, political symbols, watermark, text, logo, blurry, low quality, "
            "multiple conflicting styles, broken anatomy"
        ),
        "topic_pool": [],
    },
    "school_story": {
        "id": "school_story",
        "label": "School drama / storytime Short",
        "groq_system_hint": (
            "You write fictional school storytime Shorts. Tone: suspense + heart. "
            "Characters are original (no copyrighted names). Hook in line 1. "
            "Build to one memorable twist. Keep each kid-safe."
        ),
        "segment_count": 5,
        "topic_pool": [
            "the new kid nobody noticed",
            "a locker that wouldn't open",
            "a substitute teacher with a secret",
            "the lost lunchbox mystery",
            "a field trip gone strange",
            "the science fair disaster",
            "a friendship bracelet with a twist",
            "a school play that went wrong",
            "the detention room incident",
            "a letter passed in class",
        ],
    },
    "psych_tradeoff": {
        "id": "psych_tradeoff",
        "label": "Psychology / habits (non-clinical)",
        "groq_system_hint": (
            "You write Shorts about habits, motivation, and everyday psychology. "
            "Never diagnose or claim medical facts. Use 'some people' / 'research suggests' carefully. "
            "Practical tips only."
        ),
        "segment_count": 5,
        "topic_pool": [
            "why procrastination actually happens",
            "the 2-minute rule for habits",
            "why we care what strangers think",
            "how your morning sets your day",
            "the truth about motivation",
            "why boredom is good for you",
            "the psychology of saying no",
            "why small wins matter",
            "how overthinking actually hurts",
            "the real reason we scroll endlessly",
        ],
    },
    "history_micro": {
        "id": "history_micro",
        "label": "One moment in history",
        "groq_system_hint": (
            "You write one tight historical anecdote per Short. Pick public-domain or widely taught events. "
            "No graphic violence. End with why it matters in one line."
        ),
        "segment_count": 5,
        "topic_pool": [
            "a lesser-known ancient invention",
            "a moment that almost changed history",
            "an underrated figure from ancient times",
            "a coincidence that shaped a war",
            "a forgotten discovery at sea",
            "an ancient ruler's unexpected habit",
            "a medieval tradition nobody remembers",
            "a natural disaster that changed a city",
            "a lost city that was finally found",
            "an accidental scientific breakthrough",
        ],
    },
    "ghost_stories": {
        "id": "ghost_stories",
        "label": "Ghost / horror storytime Short",
        "min_words": 100,
        "groq_system_hint": (
            "You write spooky ghost story Shorts for YouTube. "
            "CRITICAL LENGTH RULE: The TOTAL word count across ALL 6 segments MUST be 120-140 words. "
            "Each segment narration = 2-3 sentences, about 20-25 words per segment. "
            "This produces 35-45 seconds of audio when read aloud. "
            "Tone: eerie, suspenseful, creepy but NOT gory or violent. "
            "Segment 1: hook that stops scrolling. Last segment: chilling twist or unanswered question. "
            "All stories fictional. Original characters. PG-13. No hashtags in narration."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", dark spooky cartoon illustration, eerie atmosphere, creepy stylized art, "
            "bold outlines, muted haunting colors, horror cartoon aesthetic, ghostly shadows, "
            "dramatic lighting, sinister mood, professional youtube thumbnail quality, "
            "no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "photorealistic, photograph, happy cheerful bright, anime eyes, blurry, "
            "low quality, watermark, logo, text, title, signature, ugly, grainy, "
            "gore, blood, nudity, child-unsafe"
        ),
        "topic_pool": [
            "a ghost haunting an empty school at night",
            "a strange presence in a family home",
            "something unexplained during a picnic in the woods",
            "a ghost encounter at a friend's sleepover",
            "a haunted old cabin during a camping trip",
            "a ghost on a late-night train",
            "something wrong with the new neighbor's house",
            "a spirit in grandparents' attic",
            "an abandoned playground after dark",
            "a ghost at a roadside motel",
            "strange events at a wedding venue",
            "a haunted library after closing",
            "something watching from the forest edge",
            "a ghost during a blackout storm",
            "an eerie presence at a local hospital",
            "something in the basement nobody talks about",
            "a ghost on a deserted beach at night",
            "a haunted elevator in an old building",
            "a strange figure at a bus stop at 3 AM",
            "something whispering from an old well",
            "a ghost in a classroom after everyone left",
            "a haunted antique bought from a flea market",
            "a spirit tied to an old family photograph",
            "something in the fog on a mountain road",
            "a ghost at a summer camp",
        ],
    },
}


def list_channel_ids() -> list[str]:
    return sorted(PRESETS.keys())


def get_preset(channel_id: str) -> ChannelPreset:
    key = channel_id.strip().lower().replace("-", "_")
    if key not in PRESETS:
        raise KeyError(f"Unknown channel preset {channel_id!r}. Try: {', '.join(list_channel_ids())}")
    return PRESETS[key]

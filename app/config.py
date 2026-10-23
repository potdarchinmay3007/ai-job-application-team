import os

from dotenv import load_dotenv

# Read the .env file and load its values into the environment
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Low temperature = more consistent, less "creative" output
TEMPERATURE = 0.2

# The reviewer can send the draft back to the writer at most this many times
MAX_REVISIONS = 2


def validate_config() -> None:
    """Stop early with a clear message if the API key is missing."""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_api_key_here":
        raise ValueError(
            "GOOGLE_API_KEY is missing. Add your key to the .env file "
            "(see .env.example for the format)."
        )
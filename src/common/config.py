"""
This module loads Azure Custom Vision API credentials from
environment variables.
"""

import os

from dotenv import load_dotenv

load_dotenv()
CUSTOM_VISION_KEY = os.getenv("CUSTOM_VISION_KEY")
CUSTOM_VISION_ENDPOINT = os.getenv("CUSTOM_VISION_ENDPOINT")
CUSTOM_VISION_PROJECT_ID = os.getenv("CUSTOM_VISION_PROJECT_ID")
CUSTOM_VISION_PUBLISHED_NAME = os.getenv("CUSTOM_VISION_PUBLISHED_NAME")

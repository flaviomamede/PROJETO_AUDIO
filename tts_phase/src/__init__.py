"""
Módulos da fase TTS - Text-to-Speech com Voice Cloning
"""

__version__ = "2.0.0"
__author__ = "Flavio Mamede"

from .voice_cloner import VoiceCloner
from .tts_engine import TTSEngine

__all__ = ["VoiceCloner", "TTSEngine"]

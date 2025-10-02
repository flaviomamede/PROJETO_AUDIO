# Configurações do projeto

import os
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent.parent  # Volta para o diretório raiz do projeto
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
TESTS_DIR = PROJECT_ROOT / "tests"

# Criar diretórios se não existirem
OUTPUT_DIR.mkdir(exist_ok=True)

# Configurações de download
YOUTUBE_CONFIG = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': str(OUTPUT_DIR / '%(title)s.%(ext)s'),
    'noplaylist': True,
}

# Configurações do Whisper
WHISPER_CONFIG = {
    'model': 'medium',  # tiny, base, small, medium, large
    'language': 'pt',   # português
    'verbose': True,
}

# Formatos suportados
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mkv', '.avi', '.mov', '.webm']
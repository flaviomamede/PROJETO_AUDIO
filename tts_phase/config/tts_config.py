"""
Configurações para o sistema TTS com clonagem de voz
"""

import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
MODELS_DIR = BASE_DIR / "models"
VOICE_SAMPLES_DIR = BASE_DIR / "voice_samples"
OUTPUT_DIR = BASE_DIR / "output"
TRAINING_DATA_DIR = BASE_DIR / "training_data"

# Configurações do modelo TTS
TTS_CONFIG = {
    # Modelos disponíveis
    "models": {
        "coqui": {
            "name": "tts_models/multilingual/multi-dataset/xtts_v2",
            "language": "pt",
            "description": "Coqui XTTS v2 - Multilingual"
        },
        "tacotron2": {
            "name": "tts_models/pt/cv/vits",
            "language": "pt", 
            "description": "Tacotron2 para português"
        },
        "fastspeech2": {
            "name": "tts_models/pt/cv/fastspeech2",
            "language": "pt",
            "description": "FastSpeech2 para português"
        }
    },
    
    # Configurações de áudio
    "audio": {
        "sample_rate": 22050,
        "hop_length": 256,
        "win_length": 1024,
        "n_fft": 1024,
        "n_mels": 80,
        "fmin": 0,
        "fmax": 8000
    },
    
    # Configurações de voz
    "voice": {
        "min_duration": 3.0,  # segundos mínimos para treinar
        "max_duration": 30.0,  # segundos máximos por amostra
        "target_sample_rate": 22050,
        "normalize": True,
        "remove_noise": True
    },
    
    # Configurações de síntese
    "synthesis": {
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 1.0,
        "emphasis": 1.0,
        "emotion": "neutral"  # neutral, happy, sad, angry
    }
}

# Configurações de clonagem de voz
VOICE_CLONING_CONFIG = {
    "encoder": {
        "model_path": MODELS_DIR / "encoder" / "saved_models",
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "speaker_embedding_dim": 256
    },
    
    "synthesizer": {
        "model_path": MODELS_DIR / "synthesizer" / "saved_models",
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "sample_rate": 16000,
        "spec_channels": 80,
        "embed_dims": 512,
        "encoder_dims": 256,
        "decoder_dims": 512,
        "ff_dims": 1024,
        "num_heads": 4,
        "num_layers": 6,
        "dropout": 0.1
    },
    
    "vocoder": {
        "model_path": MODELS_DIR / "vocoder" / "saved_models",
        "device": "cuda" if os.system("nvidia-smi > /dev/null 2>&1") == 0 else "cpu",
        "sample_rate": 16000,
        "hop_length": 256,
        "win_length": 1024
    }
}

# Configurações de treinamento
TRAINING_CONFIG = {
    "batch_size": 16,
    "learning_rate": 1e-4,
    "epochs": 100,
    "save_every": 10,
    "validation_split": 0.2,
    "early_stopping_patience": 20,
    "gradient_clip_norm": 1.0
}

# Configurações de qualidade
QUALITY_CONFIG = {
    "noise_reduction": {
        "enabled": True,
        "stationary": True,
        "prop_decrease": 0.8
    },
    
    "audio_enhancement": {
        "normalize": True,
        "trim_silence": True,
        "fade_in_ms": 50,
        "fade_out_ms": 50
    },
    
    "output_format": {
        "format": "wav",
        "bit_depth": 16,
        "channels": 1,
        "sample_rate": 22050
    }
}

# Configurações de interface
UI_CONFIG = {
    "web_interface": {
        "enabled": True,
        "port": 7860,
        "host": "0.0.0.0",
        "share": False
    },
    
    "cli": {
        "enabled": True,
        "verbose": True,
        "progress_bar": True
    }
}

def ensure_directories():
    """Garante que todos os diretórios necessários existam"""
    directories = [
        SRC_DIR,
        MODELS_DIR,
        VOICE_SAMPLES_DIR,
        OUTPUT_DIR,
        TRAINING_DATA_DIR,
        MODELS_DIR / "encoder" / "saved_models",
        MODELS_DIR / "synthesizer" / "saved_models", 
        MODELS_DIR / "vocoder" / "saved_models"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return directories

def get_device():
    """Detecta o melhor dispositivo disponível"""
    import torch
    
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return "mps"  # Apple Silicon
    else:
        return "cpu"

def update_device_config():
    """Atualiza configurações com o dispositivo detectado"""
    device = get_device()
    
    VOICE_CLONING_CONFIG["encoder"]["device"] = device
    VOICE_CLONING_CONFIG["synthesizer"]["device"] = device
    VOICE_CLONING_CONFIG["vocoder"]["device"] = device
    
    return device

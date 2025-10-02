# Utilitários gerais do projeto

import re
import logging
from pathlib import Path
from typing import Optional
from colorama import Fore, Style, init

# Inicializar colorama para Windows
init(autoreset=True)

def sanitize_filename(filename: str) -> str:
    """
    Remove ou substitui caracteres inválidos em nomes de arquivo.
    
    Args:
        filename: Nome original do arquivo
        
    Returns:
        Nome sanitizado seguro para uso
    """
    # Caracteres inválidos no Windows/Linux
    invalid_chars = r'[<>:"/\\|?*]'
    
    # Substituir caracteres inválidos por underscore
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remover espaços extras e pontos no final
    sanitized = sanitized.strip('. ')
    
    # Limitar tamanho (Windows tem limite de 255 caracteres)
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Cria um logger configurado com formatação colorida.
    
    Args:
        name: Nome do logger
        level: Nível de logging
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Criar handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formato com cores
    class ColoredFormatter(logging.Formatter):
        """Formatter com cores para diferentes níveis"""
        
        COLORS = {
            'DEBUG': Fore.CYAN,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.MAGENTA,
        }
        
        def format(self, record):
            log_color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
            
            # Formato: [TIMESTAMP] LEVEL - MODULE: MESSAGE
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                datefmt='%H:%M:%S'
            )
            
            return formatter.format(record)
    
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    return logger

def format_duration(seconds: float) -> str:
    """
    Formata duração em segundos para formato legível.
    
    Args:
        seconds: Duração em segundos
        
    Returns:
        String formatada (ex: "2:30" ou "1:05:30")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em bytes para formato legível.
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        String formatada (ex: "1.5 MB", "2.3 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def ensure_directory(path: Path) -> Path:
    """
    Garante que um diretório existe, criando se necessário.
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Path do diretório (garantidamente existente)
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def is_audio_file(file_path: Path) -> bool:
    """
    Verifica se um arquivo é de áudio baseado na extensão.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        True se for arquivo de áudio
    """
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma'}
    return file_path.suffix.lower() in audio_extensions

def is_video_file(file_path: Path) -> bool:
    """
    Verifica se um arquivo é de vídeo baseado na extensão.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        True se for arquivo de vídeo
    """
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv'}
    return file_path.suffix.lower() in video_extensions

def validate_url(url: str) -> bool:
    """
    Validação básica de URL.
    
    Args:
        url: URL para validar
        
    Returns:
        True se URL parece válida
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None
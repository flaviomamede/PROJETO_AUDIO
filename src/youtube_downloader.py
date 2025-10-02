# YouTube Audio Downloader
# Utiliza yt-dlp (sucessor mais robusto do youtube-dl)

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any
import yt_dlp
from .config import YOUTUBE_CONFIG, OUTPUT_DIR
from .utils import sanitize_filename, get_logger

logger = get_logger(__name__)

class YouTubeDownloader:
    """
    Classe para download de áudio de vídeos do YouTube usando yt-dlp.
    
    Vantagens do yt-dlp sobre outras ferramentas:
    - Mais rápido e robusto que youtube-dl
    - Suporta mais sites e formatos
    - Mantido ativamente
    - Melhor tratamento de erros
    """
    
    def __init__(self, output_dir: Optional[Path] = None, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o downloader.
        
        Args:
            output_dir: Diretório de saída (padrão: ./output)
            config: Configurações customizadas do yt-dlp
        """
        self.output_dir = output_dir or OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
        
        # Configuração padrão do yt-dlp
        self.config = config or YOUTUBE_CONFIG.copy()
        self.config['outtmpl'] = str(self.output_dir / '%(title)s.%(ext)s')
        
        logger.info(f"YouTubeDownloader inicializado. Saída: {self.output_dir}")
    
    def download(self, url: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        Baixa o áudio de um vídeo do YouTube.
        
        Args:
            url: URL do vídeo do YouTube
            filename: Nome customizado para o arquivo (opcional)
            
        Returns:
            Path do arquivo baixado ou None se falhou
        """
        if not self._is_valid_youtube_url(url):
            logger.error(f"URL inválida: {url}")
            return None
        
        try:
            # Configuração para este download
            config = self.config.copy()
            
            if filename:
                sanitized_name = sanitize_filename(filename)
                config['outtmpl'] = str(self.output_dir / f'{sanitized_name}.%(ext)s')
            
            # Hooks para capturrar o nome do arquivo
            downloaded_file = None
            
            def hook(d):
                nonlocal downloaded_file
                if d['status'] == 'finished':
                    downloaded_file = Path(d['filename'])
                    logger.info(f"Download concluído: {downloaded_file.name}")
            
            config['progress_hooks'] = [hook]
            
            # Executar download
            with yt_dlp.YoutubeDL(config) as ydl:
                logger.info(f"Iniciando download: {url}")
                ydl.download([url])
                
                if downloaded_file and downloaded_file.exists():
                    return downloaded_file
                else:
                    logger.error("Arquivo não encontrado após download")
                    return None
                    
        except Exception as e:
            logger.error(f"Erro ao baixar {url}: {str(e)}")
            return None
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações sobre o vídeo sem baixar.
        
        Args:
            url: URL do vídeo
            
        Returns:
            Dicionário com informações do vídeo ou None
        """
        if not self._is_valid_youtube_url(url):
            return None
        
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Sem título'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Desconhecido'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                }
        except Exception as e:
            logger.error(f"Erro ao extrair informações: {str(e)}")
            return None
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """
        Verifica se a URL é válida do YouTube.
        
        Args:
            url: URL para verificar
            
        Returns:
            True se válida, False caso contrário
        """
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://(?:www\.)?youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/live/[\w-]+',  # Suporte para live streams
            r'https?://(?:www\.)?youtube\.com/.*[?&]v=[\w-]+',  # URLs com parâmetros extras
        ]
        
        return any(re.search(pattern, url) for pattern in youtube_patterns)
    
    def list_downloaded_files(self) -> list[Path]:
        """
        Lista todos os arquivos de áudio baixados.
        
        Returns:
            Lista de caminhos dos arquivos
        """
        audio_extensions = ['.mp3', '.m4a', '.wav', '.ogg', '.flac']
        files = []
        
        for file in self.output_dir.iterdir():
            if file.is_file() and file.suffix.lower() in audio_extensions:
                files.append(file)
        
        return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def download_sample(self, url: str, filename: Optional[str] = None, duration_seconds: int = 60) -> Optional[Path]:
        """
        Baixa apenas uma amostra (primeiros N segundos) do vídeo para teste.
        
        Args:
            url: URL do vídeo do YouTube
            filename: Nome customizado para o arquivo (opcional)
            duration_seconds: Duração da amostra em segundos
            
        Returns:
            Path do arquivo baixado ou None se falhou
        """
        if not self._is_valid_youtube_url(url):
            logger.error(f"URL inválida: {url}")
            return None
        
        try:
            # Configuração para este download com duração limitada
            config = self.config.copy()
            
            # Adicionar filtros para limitar duração
            config['postprocessor_args'] = {
                'ffmpeg': ['-t', str(duration_seconds)]
            }
            
            if filename:
                sanitized_name = sanitize_filename(f"{filename}_sample_{duration_seconds}s")
                config['outtmpl'] = str(self.output_dir / f'{sanitized_name}.%(ext)s')
            else:
                config['outtmpl'] = str(self.output_dir / f'sample_{duration_seconds}s_%(title)s.%(ext)s')
            
            # Hooks para capturrar o nome do arquivo
            downloaded_file = None
            
            def hook(d):
                nonlocal downloaded_file
                if d['status'] == 'finished':
                    downloaded_file = Path(d['filename'])
                    logger.info(f"Amostra baixada: {downloaded_file.name}")
            
            config['progress_hooks'] = [hook]
            
            # Executar download
            with yt_dlp.YoutubeDL(config) as ydl:
                logger.info(f"Baixando amostra ({duration_seconds}s): {url}")
                ydl.download([url])
                
                if downloaded_file and downloaded_file.exists():
                    return downloaded_file
                else:
                    logger.error("Arquivo de amostra não encontrado após download")
                    return None
                    
        except Exception as e:
            logger.error(f"Erro ao baixar amostra de {url}: {str(e)}")
            return None
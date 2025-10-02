# Audio Transcriber usando OpenAI Whisper
# Whisper é gratuito, funciona offline e tem alta precisão

import os
from pathlib import Path
from typing import Optional, Union, Dict, Any
import whisper
from .config import WHISPER_CONFIG
from .utils import get_logger
from .ai_postprocessor import enhance_transcription_with_ai

logger = get_logger(__name__)

class AudioTranscriber:
    """
    Classe para transcrição de áudio usando OpenAI Whisper.
    
    Vantagens do Whisper:
    - Gratuito e open source
    - Funciona 100% offline
    - Alta precisão para português
    - Múltiplos modelos (velocidade vs qualidade)
    - Suporte nativo ao português brasileiro
    """
    
    def __init__(self, model_size: str = "medium", language: str = "pt"):
        """
        Inicializa o transcriber.
        
        Args:
            model_size: Tamanho do modelo ('tiny', 'base', 'small', 'medium', 'large')
            language: Código do idioma ('pt' para português)
        """
        self.model_size = model_size
        self.language = language
        self.model = None
        
        logger.info(f"AudioTranscriber inicializado - Modelo: {model_size}, Idioma: {language}")
        
        # Informações sobre os modelos
        self.model_info = {
            'tiny': {'size': '~72 MB', 'ram': '~1 GB', 'speed': 'Muito rápida', 'quality': 'Básica'},
            'base': {'size': '~142 MB', 'ram': '~1 GB', 'speed': 'Rápida', 'quality': 'Boa'},
            'small': {'size': '~483 MB', 'ram': '~2 GB', 'speed': 'Moderada', 'quality': 'Muito boa'},
            'medium': {'size': '~1.4 GB', 'ram': '~5 GB', 'speed': 'Lenta', 'quality': 'Excelente'},
            'large': {'size': '~3.1 GB', 'ram': '~10 GB', 'speed': 'Muito lenta', 'quality': 'Máxima'}
        }
    
    def load_model(self) -> bool:
        """
        Carrega o modelo Whisper (download automático na primeira vez).
        
        Returns:
            True se carregado com sucesso, False caso contrário
        """
        try:
            if self.model is None:
                info = self.model_info.get(self.model_size, {})
                logger.info(f"Carregando modelo '{self.model_size}' ({info.get('size', 'desconhecido')})")
                logger.info("Primeira execução pode demorar (download do modelo)")
                
                self.model = whisper.load_model(self.model_size)
                logger.info("Modelo carregado com sucesso")
                
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            return False
    
    def transcribe(self, audio_path: Union[str, Path], 
                  output_path: Optional[Union[str, Path]] = None,
                  include_timestamps: bool = False,
                  enhance_with_ai: bool = True) -> Optional[str]:
        """
        Transcreve um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            output_path: Caminho para salvar a transcrição (opcional)
            include_timestamps: Se incluir timestamps na transcrição
            enhance_with_ai: Se aplicar pós-processamento com IA (padrão: True)
            
        Returns:
            Texto transcrito ou None se falhou
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            logger.error(f"Arquivo não encontrado: {audio_path}")
            return None
        
        if not self.load_model():
            return None
        
        try:
            logger.info(f"Iniciando transcrição: {audio_path.name}")
            
            # Executar transcrição
            result = self.model.transcribe(
                str(audio_path),
                language=self.language,
                verbose=True
            )
            
            # Extrair texto
            if include_timestamps:
                text = self._format_with_timestamps(result)
            else:
                text = result['text'].strip()
            
            logger.info(f"Transcrição básica concluída ({len(text)} caracteres)")
            
            # Aplicar pós-processamento com IA se solicitado
            if enhance_with_ai and not include_timestamps:
                logger.info("Aplicando melhorias com IA...")
                text = enhance_transcription_with_ai(text)
                logger.info(f"Texto melhorado com IA ({len(text)} caracteres)")
            
            logger.info(f"Transcrição final concluída ({len(text)} caracteres)")
            
            # Salvar arquivo se especificado
            if output_path:
                self._save_transcription(text, output_path)
            else:
                # Salvar no mesmo diretório do áudio
                output_path = audio_path.with_suffix('.txt')
                self._save_transcription(text, output_path)
            
            return text
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {str(e)}")
            return None
    
    def transcribe_batch(self, audio_files: list[Path], 
                        output_dir: Optional[Path] = None) -> Dict[str, Optional[str]]:
        """
        Transcreve múltiplos arquivos de áudio.
        
        Args:
            audio_files: Lista de caminhos para arquivos de áudio
            output_dir: Diretório de saída (padrão: mesmo dos áudios)
            
        Returns:
            Dicionário {nome_arquivo: texto_transcrito}
        """
        results = {}
        
        if not self.load_model():
            return results
        
        for audio_file in audio_files:
            if output_dir:
                output_path = output_dir / f"{audio_file.stem}.txt"
            else:
                output_path = None
            
            text = self.transcribe(audio_file, output_path)
            results[audio_file.name] = text
        
        return results
    
    def _format_with_timestamps(self, result: Dict[str, Any]) -> str:
        """
        Formata o resultado com timestamps.
        
        Args:
            result: Resultado do Whisper
            
        Returns:
            Texto formatado com timestamps
        """
        formatted_text = []
        
        for segment in result['segments']:
            start = self._format_timestamp(segment['start'])
            end = self._format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            formatted_text.append(f"[{start} -> {end}] {text}")
        
        return '\n'.join(formatted_text)
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Formata segundos em MM:SS.
        
        Args:
            seconds: Tempo em segundos
            
        Returns:
            String formatada MM:SS
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def _save_transcription(self, text: str, output_path: Union[str, Path]) -> bool:
        """
        Salva a transcrição em arquivo.
        
        Args:
            text: Texto a salvar
            output_path: Caminho do arquivo de saída
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            logger.info(f"Transcrição salva: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar transcrição: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Obtém informações sobre o modelo atual.
        
        Returns:
            Dicionário com informações do modelo
        """
        return {
            'model': self.model_size,
            'language': self.language,
            **self.model_info.get(self.model_size, {})
        }
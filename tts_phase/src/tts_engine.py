"""
Engine principal para Text-to-Speech com clonagem de voz
"""

import os
import torch
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging
import json
from datetime import datetime

from ..config.tts_config import (
    TTS_CONFIG,
    QUALITY_CONFIG,
    OUTPUT_DIR,
    VOICE_SAMPLES_DIR
)
from .voice_cloner import VoiceCloner

logger = logging.getLogger(__name__)

class TTSEngine:
    """
    Engine principal para síntese de fala com clonagem de voz.
    
    Funcionalidades:
    - Síntese de texto em áudio
    - Clonagem de voz personalizada
    - Controle de parâmetros de voz
    - Processamento em lote
    - Interface web e CLI
    """
    
    def __init__(self, model_type: str = "coqui", device: Optional[str] = None):
        """
        Inicializa o engine TTS.
        
        Args:
            model_type: Tipo de modelo ('coqui', 'rtvc', 'custom')
            device: Dispositivo para inferência
        """
        self.model_type = model_type
        self.device = device
        self.voice_cloner = VoiceCloner(model_type=model_type, device=device)
        self.current_voice = None
        self.voice_cache = {}
        
        logger.info(f"TTSEngine inicializado - Modelo: {model_type}")
    
    def initialize(self) -> bool:
        """
        Inicializa o engine carregando o modelo.
        
        Returns:
            True se inicializado com sucesso
        """
        try:
            logger.info("Inicializando TTSEngine...")
            
            if not self.voice_cloner.load_model():
                logger.error("Falha ao carregar modelo de clonagem")
                return False
            
            logger.info("TTSEngine inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro na inicialização: {str(e)}")
            return False
    
    def train_voice_from_samples(self, voice_name: str, 
                                voice_samples: List[Union[str, Path]],
                                text_samples: Optional[List[str]] = None) -> bool:
        """
        Treina uma nova voz a partir de amostras de áudio.
        
        Args:
            voice_name: Nome da voz a ser criada
            voice_samples: Lista de arquivos de áudio
            text_samples: Textos correspondentes (opcional)
            
        Returns:
            True se o treinamento foi bem-sucedido
        """
        try:
            logger.info(f"Iniciando treinamento da voz: {voice_name}")
            
            # Validar entrada
            if not voice_samples:
                logger.error("Nenhuma amostra de voz fornecida")
                return False
            
            if not voice_name or not voice_name.strip():
                logger.error("Nome da voz não pode estar vazio")
                return False
            
            # Treinar voz
            success = self.voice_cloner.train_voice(
                voice_samples=voice_samples,
                voice_name=voice_name,
                text_samples=text_samples
            )
            
            if success:
                logger.info(f"Voz '{voice_name}' treinada com sucesso")
                # Atualizar cache
                self._update_voice_cache()
            else:
                logger.error(f"Falha no treinamento da voz '{voice_name}'")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {str(e)}")
            return False
    
    def synthesize(self, text: str, voice_name: Optional[str] = None,
                  reference_voice: Optional[Union[str, Path]] = None,
                  output_path: Optional[Union[str, Path]] = None,
                  **synthesis_params) -> Optional[Path]:
        """
        Sintetiza texto em áudio usando voz especificada.
        
        Args:
            text: Texto para sintetizar
            voice_name: Nome da voz treinada
            reference_voice: Caminho para amostra de referência
            output_path: Caminho de saída
            **synthesis_params: Parâmetros de síntese (speed, pitch, etc.)
            
        Returns:
            Caminho do arquivo gerado ou None
        """
        try:
            logger.info(f"Sintetizando texto: {text[:50]}...")
            
            # Determinar voz de referência
            ref_voice = self._resolve_reference_voice(voice_name, reference_voice)
            if not ref_voice:
                logger.error("Não foi possível determinar voz de referência")
                return None
            
            # Gerar áudio
            audio_path = self.voice_cloner.clone_voice(
                text=text,
                reference_voice=ref_voice,
                output_path=output_path,
                **synthesis_params
            )
            
            if audio_path:
                # Pós-processar áudio
                processed_path = self._post_process_audio(audio_path, **synthesis_params)
                logger.info(f"Áudio sintetizado: {processed_path}")
                return processed_path
            else:
                logger.error("Falha na síntese de áudio")
                return None
                
        except Exception as e:
            logger.error(f"Erro na síntese: {str(e)}")
            return None
    
    def synthesize_batch(self, texts: List[str], 
                        voice_name: Optional[str] = None,
                        reference_voice: Optional[Union[str, Path]] = None,
                        output_dir: Optional[Union[str, Path]] = None,
                        **synthesis_params) -> List[Optional[Path]]:
        """
        Sintetiza múltiplos textos em lote.
        
        Args:
            texts: Lista de textos para sintetizar
            voice_name: Nome da voz treinada
            reference_voice: Caminho para amostra de referência
            output_dir: Diretório de saída
            **synthesis_params: Parâmetros de síntese
            
        Returns:
            Lista de caminhos dos arquivos gerados
        """
        try:
            logger.info(f"Sintetizando lote de {len(texts)} textos")
            
            # Preparar diretório de saída
            if output_dir:
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
            
            results = []
            
            for i, text in enumerate(texts):
                logger.info(f"Processando texto {i+1}/{len(texts)}")
                
                # Gerar nome de arquivo
                filename = f"batch_{i+1:03d}.wav"
                output_path = output_dir / filename if output_dir else None
                
                # Sintetizar
                result = self.synthesize(
                    text=text,
                    voice_name=voice_name,
                    reference_voice=reference_voice,
                    output_path=output_path,
                    **synthesis_params
                )
                
                results.append(result)
            
            successful = sum(1 for r in results if r is not None)
            logger.info(f"Lote concluído: {successful}/{len(texts)} sucessos")
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na síntese em lote: {str(e)}")
            return [None] * len(texts)
    
    def _resolve_reference_voice(self, voice_name: Optional[str], 
                                reference_voice: Optional[Union[str, Path]]) -> Optional[Path]:
        """Resolve a voz de referência a ser usada"""
        
        # Prioridade: reference_voice direto
        if reference_voice:
            ref_path = Path(reference_voice)
            if ref_path.exists():
                return ref_path
            else:
                logger.error(f"Arquivo de referência não encontrado: {reference_voice}")
                return None
        
        # Fallback: voice_name
        if voice_name:
            # Procurar em vozes treinadas
            voice_dir = VOICE_SAMPLES_DIR / voice_name
            if voice_dir.exists():
                # Encontrar primeira amostra .wav
                for sample_file in voice_dir.glob("*.wav"):
                    return sample_file
                logger.error(f"Nenhuma amostra .wav encontrada para voz: {voice_name}")
            else:
                logger.error(f"Voz não encontrada: {voice_name}")
        
        return None
    
    def _post_process_audio(self, audio_path: Path, **params) -> Path:
        """
        Pós-processa o áudio gerado para melhorar qualidade.
        
        Args:
            audio_path: Caminho do áudio original
            **params: Parâmetros de processamento
            
        Returns:
            Caminho do áudio processado
        """
        try:
            # Carregar áudio
            audio, sr = librosa.load(str(audio_path), sr=TTS_CONFIG["audio"]["sample_rate"])
            
            # Aplicar melhorias de qualidade
            if QUALITY_CONFIG["noise_reduction"]["enabled"]:
                audio = self._reduce_noise(audio, sr)
            
            if QUALITY_CONFIG["audio_enhancement"]["normalize"]:
                audio = librosa.util.normalize(audio)
            
            if QUALITY_CONFIG["audio_enhancement"]["trim_silence"]:
                audio = self._trim_silence(audio, sr)
            
            # Aplicar fade in/out
            fade_in_ms = QUALITY_CONFIG["audio_enhancement"]["fade_in_ms"]
            fade_out_ms = QUALITY_CONFIG["audio_enhancement"]["fade_out_ms"]
            
            if fade_in_ms > 0 or fade_out_ms > 0:
                audio = self._apply_fade(audio, sr, fade_in_ms, fade_out_ms)
            
            # Salvar áudio processado
            processed_path = audio_path.parent / f"{audio_path.stem}_processed{audio_path.suffix}"
            
            sf.write(
                processed_path,
                audio,
                QUALITY_CONFIG["output_format"]["sample_rate"],
                format=QUALITY_CONFIG["output_format"]["format"],
                subtype=f"PCM_{QUALITY_CONFIG['output_format']['bit_depth']}"
            )
            
            return processed_path
            
        except Exception as e:
            logger.error(f"Erro no pós-processamento: {str(e)}")
            return audio_path  # Retornar original se falhar
    
    def _reduce_noise(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Reduz ruído do áudio"""
        try:
            import noisereduce as nr
            config = QUALITY_CONFIG["noise_reduction"]
            return nr.reduce_noise(
                y=audio,
                sr=sr,
                stationary=config["stationary"],
                prop_decrease=config["prop_decrease"]
            )
        except Exception as e:
            logger.warning(f"Erro na redução de ruído: {str(e)}")
            return audio
    
    def _trim_silence(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Remove silêncio do início e fim"""
        try:
            # Detectar silêncio
            intervals = librosa.effects.split(
                audio,
                top_db=20,  # dB abaixo do pico para considerar silêncio
                frame_length=2048,
                hop_length=512
            )
            
            if len(intervals) > 0:
                # Usar primeiro intervalo não-silencioso
                start = intervals[0][0]
                end = intervals[-1][1]
                return audio[start:end]
            
            return audio
            
        except Exception as e:
            logger.warning(f"Erro no trim de silêncio: {str(e)}")
            return audio
    
    def _apply_fade(self, audio: np.ndarray, sr: int, 
                   fade_in_ms: int, fade_out_ms: int) -> np.ndarray:
        """Aplica fade in/out ao áudio"""
        try:
            # Converter ms para samples
            fade_in_samples = int(fade_in_ms * sr / 1000)
            fade_out_samples = int(fade_out_ms * sr / 1000)
            
            # Aplicar fade in
            if fade_in_samples > 0:
                fade_in = np.linspace(0, 1, fade_in_samples)
                audio[:fade_in_samples] *= fade_in
            
            # Aplicar fade out
            if fade_out_samples > 0:
                fade_out = np.linspace(1, 0, fade_out_samples)
                audio[-fade_out_samples:] *= fade_out
            
            return audio
            
        except Exception as e:
            logger.warning(f"Erro no fade: {str(e)}")
            return audio
    
    def _update_voice_cache(self):
        """Atualiza cache de vozes disponíveis"""
        try:
            voices_dir = VOICE_SAMPLES_DIR
            self.voice_cache = {}
            
            if voices_dir.exists():
                for voice_dir in voices_dir.iterdir():
                    if voice_dir.is_dir():
                        self.voice_cache[voice_dir.name] = {
                            "path": voice_dir,
                            "samples": list(voice_dir.glob("*.wav")),
                            "info": self.voice_cloner.get_voice_info(voice_dir.name)
                        }
            
            logger.info(f"Cache atualizado: {len(self.voice_cache)} vozes disponíveis")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar cache: {str(e)}")
    
    def list_voices(self) -> List[Dict[str, Any]]:
        """Lista todas as vozes disponíveis"""
        if not self.voice_cache:
            self._update_voice_cache()
        
        voices = []
        for name, data in self.voice_cache.items():
            voices.append({
                "name": name,
                "samples": len(data["samples"]),
                "info": data["info"]
            })
        
        return sorted(voices, key=lambda x: x["name"])
    
    def get_voice_details(self, voice_name: str) -> Dict[str, Any]:
        """Obtém detalhes de uma voz específica"""
        if voice_name in self.voice_cache:
            return self.voice_cache[voice_name]["info"]
        else:
            return self.voice_cloner.get_voice_info(voice_name)
    
    def delete_voice(self, voice_name: str) -> bool:
        """
        Remove uma voz treinada.
        
        Args:
            voice_name: Nome da voz a ser removida
            
        Returns:
            True se removida com sucesso
        """
        try:
            voice_dir = VOICE_SAMPLES_DIR / voice_name
            
            if not voice_dir.exists():
                logger.error(f"Voz não encontrada: {voice_name}")
                return False
            
            # Remover diretório
            import shutil
            shutil.rmtree(voice_dir)
            
            # Atualizar cache
            self._update_voice_cache()
            
            logger.info(f"Voz '{voice_name}' removida com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover voz: {str(e)}")
            return False

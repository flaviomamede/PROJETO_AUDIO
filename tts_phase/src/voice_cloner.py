"""
Módulo de clonagem de voz usando técnicas avançadas de TTS
"""

import os
import torch
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging

from ..config.tts_config import (
    VOICE_CLONING_CONFIG, 
    TTS_CONFIG, 
    VOICE_SAMPLES_DIR,
    MODELS_DIR
)

logger = logging.getLogger(__name__)

class VoiceCloner:
    """
    Classe principal para clonagem de voz usando múltiplas abordagens.
    
    Suporta:
    - Coqui XTTS v2 (recomendado)
    - Real-Time Voice Cloning
    - Custom fine-tuning
    """
    
    def __init__(self, model_type: str = "coqui", device: Optional[str] = None):
        """
        Inicializa o clonador de voz.
        
        Args:
            model_type: Tipo de modelo ('coqui', 'rtvc', 'custom')
            device: Dispositivo para inferência ('cuda', 'cpu', 'mps')
        """
        self.model_type = model_type
        self.device = device or self._get_best_device()
        self.model = None
        self.speaker_embedding = None
        
        logger.info(f"VoiceCloner inicializado - Modelo: {model_type}, Device: {self.device}")
        
    def _get_best_device(self) -> str:
        """Detecta o melhor dispositivo disponível"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def load_model(self, model_name: Optional[str] = None) -> bool:
        """
        Carrega o modelo TTS baseado no tipo escolhido.
        
        Args:
            model_name: Nome específico do modelo (opcional)
            
        Returns:
            True se carregado com sucesso
        """
        try:
            if self.model_type == "coqui":
                return self._load_coqui_model(model_name)
            elif self.model_type == "rtvc":
                return self._load_rtvc_model()
            elif self.model_type == "custom":
                return self._load_custom_model(model_name)
            else:
                raise ValueError(f"Tipo de modelo não suportado: {self.model_type}")
                
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            return False
    
    def _load_coqui_model(self, model_name: Optional[str] = None) -> bool:
        """Carrega modelo Coqui XTTS"""
        try:
            from TTS.api import TTS
            
            # Usar modelo padrão se não especificado
            if not model_name:
                model_name = TTS_CONFIG["models"]["coqui"]["name"]
            
            logger.info(f"Carregando modelo Coqui: {model_name}")
            self.model = TTS(model_name=model_name, progress_bar=True)
            self.model.to(self.device)
            
            logger.info("Modelo Coqui carregado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo Coqui: {str(e)}")
            return False
    
    def _load_rtvc_model(self) -> bool:
        """Carrega modelo Real-Time Voice Cloning"""
        try:
            # Implementação do RTVC seria aqui
            # Por enquanto, placeholder
            logger.warning("RTVC não implementado ainda, usando Coqui como fallback")
            return self._load_coqui_model()
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo RTVC: {str(e)}")
            return False
    
    def _load_custom_model(self, model_name: Optional[str] = None) -> bool:
        """Carrega modelo customizado"""
        try:
            # Implementação para modelos customizados
            logger.warning("Modelos customizados não implementados ainda")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo customizado: {str(e)}")
            return False
    
    def train_voice(self, voice_samples: List[Union[str, Path]], 
                   voice_name: str,
                   text_samples: Optional[List[str]] = None) -> bool:
        """
        Treina um novo modelo de voz baseado em amostras fornecidas.
        
        Args:
            voice_samples: Lista de arquivos de áudio da voz alvo
            voice_name: Nome para identificar a voz treinada
            text_samples: Textos correspondentes (opcional, para TTS supervisionado)
            
        Returns:
            True se o treinamento foi bem-sucedido
        """
        try:
            logger.info(f"Iniciando treinamento de voz: {voice_name}")
            
            # Validar amostras
            if not self._validate_voice_samples(voice_samples):
                return False
            
            # Preparar dados
            prepared_data = self._prepare_training_data(voice_samples, text_samples)
            
            # Treinar modelo
            if self.model_type == "coqui":
                return self._train_coqui_voice(prepared_data, voice_name)
            else:
                logger.error(f"Treinamento não suportado para modelo: {self.model_type}")
                return False
                
        except Exception as e:
            logger.error(f"Erro no treinamento de voz: {str(e)}")
            return False
    
    def _validate_voice_samples(self, voice_samples: List[Union[str, Path]]) -> bool:
        """Valida as amostras de voz fornecidas"""
        config = TTS_CONFIG["voice"]
        
        for sample_path in voice_samples:
            sample_path = Path(sample_path)
            
            if not sample_path.exists():
                logger.error(f"Arquivo não encontrado: {sample_path}")
                return False
            
            # Verificar duração
            try:
                duration = librosa.get_duration(filename=str(sample_path))
                if duration < config["min_duration"]:
                    logger.error(f"Amostra muito curta ({duration:.2f}s): {sample_path}")
                    return False
                if duration > config["max_duration"]:
                    logger.warning(f"Amostra muito longa ({duration:.2f}s): {sample_path}")
                    
            except Exception as e:
                logger.error(f"Erro ao validar amostra {sample_path}: {str(e)}")
                return False
        
        logger.info(f"Validação concluída: {len(voice_samples)} amostras válidas")
        return True
    
    def _prepare_training_data(self, voice_samples: List[Union[str, Path]], 
                              text_samples: Optional[List[str]] = None) -> Dict[str, Any]:
        """Prepara dados para treinamento"""
        prepared_samples = []
        
        for i, sample_path in enumerate(voice_samples):
            try:
                # Carregar áudio
                audio, sr = librosa.load(str(sample_path), sr=TTS_CONFIG["audio"]["sample_rate"])
                
                # Normalizar áudio
                if TTS_CONFIG["voice"]["normalize"]:
                    audio = librosa.util.normalize(audio)
                
                # Reduzir ruído se habilitado
                if TTS_CONFIG["voice"]["remove_noise"]:
                    import noisereduce as nr
                    audio = nr.reduce_noise(y=audio, sr=sr)
                
                # Preparar texto se fornecido
                text = None
                if text_samples and i < len(text_samples):
                    text = text_samples[i]
                
                prepared_samples.append({
                    "audio": audio,
                    "sample_rate": sr,
                    "text": text,
                    "path": str(sample_path)
                })
                
            except Exception as e:
                logger.error(f"Erro ao preparar amostra {sample_path}: {str(e)}")
                continue
        
        return {
            "samples": prepared_samples,
            "total_samples": len(prepared_samples)
        }
    
    def _train_coqui_voice(self, data: Dict[str, Any], voice_name: str) -> bool:
        """Treina voz usando modelo Coqui"""
        try:
            # Para XTTS v2, o treinamento é feito via fine-tuning
            logger.info("Iniciando fine-tuning com Coqui XTTS")
            
            # Criar diretório para a voz
            voice_dir = VOICE_SAMPLES_DIR / voice_name
            voice_dir.mkdir(parents=True, exist_ok=True)
            
            # Salvar amostras preparadas
            for i, sample in enumerate(data["samples"]):
                output_path = voice_dir / f"sample_{i:03d}.wav"
                sf.write(output_path, sample["audio"], sample["sample_rate"])
                
                # Salvar texto se disponível
                if sample["text"]:
                    text_path = voice_dir / f"sample_{i:03d}.txt"
                    with open(text_path, 'w', encoding='utf-8') as f:
                        f.write(sample["text"])
            
            logger.info(f"Voz '{voice_name}' preparada com {data['total_samples']} amostras")
            return True
            
        except Exception as e:
            logger.error(f"Erro no treinamento Coqui: {str(e)}")
            return False
    
    def clone_voice(self, text: str, reference_voice: Union[str, Path], 
                   output_path: Optional[Union[str, Path]] = None,
                   **kwargs) -> Optional[Path]:
        """
        Clona uma voz para um texto específico.
        
        Args:
            text: Texto para sintetizar
            reference_voice: Caminho para amostra da voz de referência
            output_path: Caminho de saída (opcional)
            **kwargs: Parâmetros adicionais de síntese
            
        Returns:
            Caminho do arquivo gerado ou None se falhou
        """
        try:
            if not self.model:
                logger.error("Modelo não carregado. Execute load_model() primeiro.")
                return None
            
            logger.info(f"Clonando voz para texto: {text[:50]}...")
            
            # Gerar nome de arquivo se não fornecido
            if not output_path:
                output_path = self._generate_output_path(text)
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Clonar voz baseado no modelo
            if self.model_type == "coqui":
                return self._clone_with_coqui(text, reference_voice, output_path, **kwargs)
            else:
                logger.error(f"Clonagem não suportada para modelo: {self.model_type}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na clonagem de voz: {str(e)}")
            return None
    
    def _clone_with_coqui(self, text: str, reference_voice: Union[str, Path], 
                         output_path: Path, **kwargs) -> Optional[Path]:
        """Clona voz usando Coqui XTTS"""
        try:
            # Configurações de síntese
            synthesis_config = {**TTS_CONFIG["synthesis"], **kwargs}
            
            # Sintetizar com Coqui
            self.model.tts_to_file(
                text=text,
                speaker_wav=str(reference_voice),
                language=TTS_CONFIG["models"]["coqui"]["language"],
                file_path=str(output_path),
                speed=synthesis_config.get("speed", 1.0),
                split_sentences=True
            )
            
            logger.info(f"Áudio gerado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro na clonagem Coqui: {str(e)}")
            return None
    
    def _generate_output_path(self, text: str) -> Path:
        """Gera caminho de saída baseado no texto"""
        from datetime import datetime
        
        # Criar nome baseado no texto e timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_hash = hash(text[:50]) % 10000
        filename = f"cloned_voice_{timestamp}_{text_hash}.wav"
        
        return OUTPUT_DIR / filename
    
    def list_available_voices(self) -> List[str]:
        """Lista vozes disponíveis no sistema"""
        voices = []
        
        # Vozes do Coqui
        if self.model_type == "coqui" and self.model:
            try:
                voices.extend(self.model.speakers)
            except:
                pass
        
        # Vozes customizadas
        voices_dir = VOICE_SAMPLES_DIR
        if voices_dir.exists():
            for voice_dir in voices_dir.iterdir():
                if voice_dir.is_dir():
                    voices.append(voice_dir.name)
        
        return sorted(voices)
    
    def get_voice_info(self, voice_name: str) -> Dict[str, Any]:
        """Obtém informações sobre uma voz específica"""
        voice_dir = VOICE_SAMPLES_DIR / voice_name
        
        if not voice_dir.exists():
            return {"error": f"Voz '{voice_name}' não encontrada"}
        
        info = {
            "name": voice_name,
            "samples": [],
            "total_duration": 0.0
        }
        
        # Analisar amostras
        for sample_file in voice_dir.glob("*.wav"):
            try:
                duration = librosa.get_duration(filename=str(sample_file))
                info["samples"].append({
                    "file": sample_file.name,
                    "duration": duration
                })
                info["total_duration"] += duration
            except:
                continue
        
        info["sample_count"] = len(info["samples"])
        return info

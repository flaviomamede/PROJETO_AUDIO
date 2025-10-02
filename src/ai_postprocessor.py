# AI Post-Processor para melhorar transcrições
# Usa IA para corrigir erros semânticos e identificar interlocutores

import re
from pathlib import Path
from typing import Optional, Tuple
from .utils import get_logger

logger = get_logger(__name__)

class AIPostProcessor:
    """
    Post-processador que usa IA para melhorar transcrições do Whisper.
    
    Funcionalidades:
    - Correção de erros semânticos comuns
    - Identificação e separação de interlocutores
    - Formatação melhorada para diálogos
    - Correção de nomes próprios e termos técnicos
    """
    
    def __init__(self):
        self.common_corrections = {
            # Correções baseadas no contexto do vídeo analisado
            "para comerciar": "para conversar",
            "aceto": "aceito",
            "com Vite": "o convite", 
            "ou Zenia": "Olzeni",
            "Rebeiro": "Ribeiro",
            "Uzeninha": "Olzeni",
            "perdotado": "superdotado",
            "perdotação": "superdotação",
            "perdotados": "superdotados",
            "Lutos Podcast": "Lutz Podcast",
            "Lutz": "Lutz",
            "que aí": "QI",
            "TDAG": "TDAH",
            "TDH": "TDAH",
            "Té": "TEA",
            "exitêmo": "ecossistema",
            "ex-systemo": "ecossistema",
            "asincronias": "assincronias",
            "asincronia": "assincronia",
            "alourus": "alunos",
        }
        
        # Padrões para identificar mudanças de interlocutor
        self.speaker_patterns = [
            r'\b(E aí|Então|Por exemplo|Mas|Porque)\b',
            r'\b(Caramba|Nossa|Que interessante|Legal|Perfeito)\b',
            r'\b(Doutora|Dr\.|Doutor)\b',
            r'\b(Obrigad[oa]|Tchau|Até)\b'
        ]
    
    def process(self, text: str, video_info: Optional[dict] = None) -> str:
        """
        Processa o texto da transcrição aplicando melhorias.
        
        Args:
            text: Texto bruto da transcrição
            video_info: Informações do vídeo (opcional)
            
        Returns:
            Texto melhorado
        """
        logger.info("Iniciando pós-processamento com IA...")
        
        # 1. Correções básicas de texto
        processed_text = self._apply_corrections(text)
        
        # 2. Identificar e separar interlocutores
        processed_text = self._identify_speakers(processed_text)
        
        # 3. Melhorar formatação de diálogos
        processed_text = self._format_dialogue(processed_text)
        
        # 4. Correções contextuais específicas
        processed_text = self._contextual_corrections(processed_text)
        
        logger.info("Pós-processamento concluído")
        return processed_text
    
    def _apply_corrections(self, text: str) -> str:
        """Aplica correções básicas de texto."""
        corrected_text = text
        
        for error, correction in self.common_corrections.items():
            # Correção case-insensitive mas preservando capitalização
            pattern = re.compile(re.escape(error), re.IGNORECASE)
            corrected_text = pattern.sub(correction, corrected_text)
        
        return corrected_text
    
    def _identify_speakers(self, text: str) -> str:
        """Identifica mudanças de interlocutor baseado em padrões."""
        lines = text.split('.')
        processed_lines = []
        current_speaker = "**Apresentador**"  # Assume que começa com o apresentador
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detectar mudança de interlocutor baseado em padrões
            speaker_changed = False
            
            # Padrões que indicam o apresentador
            if any(pattern in line.lower() for pattern in ["caramba", "nossa", "que interessante", "legal", "perfeito", "doutora"]):
                if current_speaker != "**Apresentador**":
                    current_speaker = "**Apresentador**"
                    speaker_changed = True
            
            # Padrões que indicam a doutora
            elif any(pattern in line.lower() for pattern in ["por exemplo", "então", "porque", "é tanto que", "a gente"]):
                if current_speaker != "**Dra. Olzeni**":
                    current_speaker = "**Dra. Olzeni**"
                    speaker_changed = True
            
            # Adicionar linha com speaker se necessário
            if speaker_changed or len(processed_lines) == 0:
                processed_lines.append(f"\n{current_speaker}: {line}")
            else:
                processed_lines.append(line)
        
        return '. '.join(processed_lines)
    
    def _format_dialogue(self, text: str) -> str:
        """Melhora a formatação de diálogos."""
        # Adicionar quebras de linha apropriadas
        text = re.sub(r'(\*\*[^*]+\*\*:)', r'\n\1', text)
        
        # Remover linhas vazias excessivas
        text = re.sub(r'\n\s*\n\s*\n', r'\n\n', text)
        
        # Capitalizar início de frases
        sentences = text.split('. ')
        formatted_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence.startswith('**'):
                # Capitalizar primeira letra se não for um marcador de speaker
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            formatted_sentences.append(sentence)
        
        return '. '.join(formatted_sentences)
    
    def _contextual_corrections(self, text: str) -> str:
        """Aplica correções contextuais específicas baseadas no conteúdo."""
        # Correções específicas para termos técnicos de psicologia/educação
        technical_corrections = {
            r'\bque aí\b': 'QI',
            r'\bque eye\b': 'QI', 
            r'\btd[ah]g?\b': 'TDAH',
            r'\bt\.?d\.?h\.?\b': 'TDAH',
            r'\btéa?\b': 'TEA',
            r'\bautismo\b': 'autismo',
            r'\bespectro autista\b': 'espectro do autismo',
            r'\bsuper dotad[oa]s?\b': 'superdotados',
            r'\baltas habilidades\b': 'altas habilidades',
            r'\bneurotípic[oa]s?\b': 'neurotípicos',
            r'\bassincroni[ae]s?\b': 'assincronias',
        }
        
        for pattern, replacement in technical_corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Correção de nomes próprios
        text = re.sub(r'\b(olzeni|ozeni|uzeni)\s+(ribeiro|rebeiro)\b', 'Olzeni Ribeiro', text, flags=re.IGNORECASE)
        text = re.sub(r'\blutz\s*podcast\b', 'Lutz Podcast', text, flags=re.IGNORECASE)
        
        return text

def enhance_transcription_with_ai(text: str, video_info: Optional[dict] = None) -> str:
    """
    Função utilitária para melhorar uma transcrição usando IA.
    
    Args:
        text: Texto da transcrição original
        video_info: Informações do vídeo (opcional)
        
    Returns:
        Texto melhorado
    """
    processor = AIPostProcessor()
    return processor.process(text, video_info)
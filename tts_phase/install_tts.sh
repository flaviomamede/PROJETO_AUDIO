#!/bin/bash

# Script de instalação para a fase TTS
# PROJETO_AUDIO - Fase 2: Text-to-Speech com Voice Cloning

echo "🎤 Instalando TTS Phase - Text-to-Speech com Voice Cloning"
echo "=========================================================="

# Verificar se estamos no ambiente correto
if [[ "$CONDA_DEFAULT_ENV" != "projeto_audio" ]]; then
    echo "❌ Ambiente conda 'projeto_audio' não ativado"
    echo "Execute: conda activate projeto_audio"
    exit 1
fi

echo "✅ Ambiente conda ativo: $CONDA_DEFAULT_ENV"

# Instalar dependências básicas
echo "📦 Instalando dependências básicas..."
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar dependências TTS
echo "📦 Instalando dependências TTS..."
pip install -r requirements_tts.txt

# Verificar instalação do Coqui TTS
echo "🔍 Verificando instalação do Coqui TTS..."
python -c "import TTS; print(f'✅ Coqui TTS versão: {TTS.__version__}')" || {
    echo "❌ Erro na instalação do Coqui TTS"
    exit 1
}

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p models/{encoder,synthesizer,vocoder}/saved_models
mkdir -p voice_samples
mkdir -p output
mkdir -p training_data

# Baixar modelo XTTS v2 (opcional)
echo "🤖 Baixando modelo XTTS v2..."
python -c "
from TTS.api import TTS
print('Baixando modelo XTTS v2...')
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')
print('✅ Modelo baixado com sucesso!')
" || echo "⚠️  Modelo será baixado na primeira execução"

# Testar instalação
echo "🧪 Testando instalação..."
python -c "
from src.tts_engine import TTSEngine
engine = TTSEngine()
print('✅ TTSEngine importado com sucesso')
print(f'✅ Device detectado: {engine.voice_cloner.device}')
"

echo ""
echo "🎉 Instalação da fase TTS concluída com sucesso!"
echo ""
echo "📖 Próximos passos:"
echo "   1. Leia o README_TTS.md para instruções detalhadas"
echo "   2. Teste com: python tts_main.py --help"
echo "   3. Treine sua primeira voz com suas amostras de áudio"
echo ""
echo "🎯 Exemplo de uso:"
echo "   python tts_main.py train --voice-name minha_voz --samples audio1.wav audio2.wav"
echo ""

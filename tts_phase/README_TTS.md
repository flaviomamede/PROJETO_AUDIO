# 🎤 TTS Phase - Text-to-Speech com Voice Cloning

**Fase 2 do PROJETO_AUDIO** - Sistema avançado de síntese de fala com clonagem de voz personalizada.

## ✨ Recursos

* 🎯 **Clonagem de voz personalizada** usando Coqui XTTS v2
* 🎵 **Síntese de alta qualidade** com controle de parâmetros
* 📦 **Processamento em lote** para múltiplos textos
* 🌐 **Interface web interativa** com Gradio
* ⚡ **Otimização para GPU/CPU** automática
* 🔧 **Pós-processamento de áudio** avançado
* 📊 **Gestão de vozes** treinadas
* 🎛️ **Controle fino** de velocidade, tom e volume

## 🚀 Instalação

### 1. Ativar ambiente

```bash
# No diretório do projeto principal
conda activate projeto_audio
```

### 2. Instalar dependências TTS

```bash
cd tts_phase
pip install -r requirements_tts.txt
```

### 3. Verificar instalação

```bash
python tts_main.py --help
```

## 📖 Como Usar

### 🎯 Treinamento de Voz

Para treinar sua voz personalizada:

```bash
# Treinar com amostras de áudio
python tts_main.py train \
  --voice-name "minha_voz" \
  --samples audio1.wav audio2.wav audio3.wav

# Treinar com textos correspondentes (opcional)
python tts_main.py train \
  --voice-name "minha_voz" \
  --samples audio1.wav audio2.wav \
  --texts textos_correspondentes.txt
```

**Requisitos das amostras:**
- Formato: WAV, MP3, FLAC
- Duração: 3-30 segundos por amostra
- Qualidade: Clara, sem ruído excessivo
- Quantidade: Mínimo 3 amostras recomendado

### 🎵 Síntese de Texto

```bash
# Síntese básica
python tts_main.py synthesize \
  --text "Olá, este é um teste da minha voz clonada!" \
  --voice-name "minha_voz"

# Síntese com parâmetros personalizados
python tts_main.py synthesize \
  --text "Texto personalizado" \
  --voice-name "minha_voz" \
  --speed 1.2 \
  --pitch 0.9 \
  --volume 1.1 \
  --output meu_audio.wav
```

### 📦 Síntese em Lote

```bash
# Criar arquivo com textos
echo "Primeiro texto para síntese" > textos.txt
echo "Segundo texto para síntese" >> textos.txt
echo "Terceiro texto para síntese" >> textos.txt

# Processar lote
python tts_main.py batch \
  --input-file textos.txt \
  --voice-name "minha_voz" \
  --output-dir ./output_lote
```

### 🌐 Interface Web

```bash
# Iniciar interface web
python tts_main.py web --port 7860

# Acessar: http://localhost:7860
```

### 📋 Gerenciamento de Vozes

```bash
# Listar vozes disponíveis
python tts_main.py list

# Informações detalhadas de uma voz
python tts_main.py info --voice-name "minha_voz"

# Remover voz
python tts_main.py delete --voice-name "minha_voz" --confirm
```

## 🔧 Parâmetros de Síntese

| Parâmetro | Descrição | Padrão | Faixa |
|-----------|-----------|--------|-------|
| `--speed` | Velocidade de fala | 1.0 | 0.5 - 2.0 |
| `--pitch` | Tom de voz | 1.0 | 0.5 - 2.0 |
| `--volume` | Volume do áudio | 1.0 | 0.1 - 3.0 |

## 📁 Estrutura de Diretórios

```
tts_phase/
├── 📂 src/
│   ├── 🎤 voice_cloner.py     # Clonagem de voz
│   ├── ⚙️ tts_engine.py       # Engine principal
│   └── 🌐 web_interface.py    # Interface web
├── 📂 config/
│   └── ⚙️ tts_config.py       # Configurações
├── 📂 models/                 # Modelos treinados
├── 📂 voice_samples/          # Amostras de voz
├── 📂 output/                 # Áudios gerados
├── 📂 training_data/          # Dados de treinamento
├── 🎤 tts_main.py             # Script principal
├── 📋 requirements_tts.txt    # Dependências
└── 📖 README_TTS.md           # Esta documentação
```

## 🤖 Modelos Suportados

### Coqui XTTS v2 (Recomendado)
- **Vantagens**: Multilíngue, alta qualidade, fácil uso
- **Idiomas**: Português, inglês, espanhol, francês, alemão
- **Requisitos**: 4GB RAM, GPU opcional

### Real-Time Voice Cloning (Em desenvolvimento)
- **Vantagens**: Clonagem em tempo real
- **Uso**: Aplicações interativas
- **Requisitos**: 8GB RAM, GPU recomendada

## 📊 Qualidade e Pós-processamento

O sistema inclui melhorias automáticas:

* 🔇 **Redução de ruído** inteligente
* 📏 **Normalização** de volume
* ✂️ **Remoção de silêncio** excessivo
* 🎵 **Fade in/out** suave
* 📈 **Melhoria de espectro** de frequências

## 🎛️ Configurações Avançadas

### Personalizar configurações

Edite `config/tts_config.py` para ajustar:

```python
# Configurações de áudio
"audio": {
    "sample_rate": 22050,
    "hop_length": 256,
    # ...
}

# Configurações de qualidade
"quality": {
    "noise_reduction": {
        "enabled": True,
        "stationary": True,
        # ...
    }
}
```

## 🔍 Solução de Problemas

### Erro: "Modelo não encontrado"
```bash
# Reinstalar dependências
pip install --upgrade -r requirements_tts.txt
```

### Erro: "CUDA out of memory"
```bash
# Usar CPU
export CUDA_VISIBLE_DEVICES=""
python tts_main.py synthesize --text "teste"
```

### Qualidade baixa na síntese
1. Verificar qualidade das amostras de treinamento
2. Usar mais amostras (5-10 recomendado)
3. Garantir amostras sem ruído
4. Ajustar parâmetros de síntese

## 📈 Performance

### Requisitos mínimos
- **CPU**: 4 cores, 2.5GHz
- **RAM**: 4GB
- **Espaço**: 2GB livres
- **OS**: Linux, Windows, macOS

### Requisitos recomendados
- **CPU**: 8 cores, 3.0GHz+
- **RAM**: 8GB+
- **GPU**: NVIDIA RTX 3060+ (opcional)
- **SSD**: Para melhor performance

## 🔗 Integração com Fase 1

Este sistema pode ser integrado com a **Fase 1** (transcrição):

```bash
# 1. Transcrever áudio (Fase 1)
python main.py --url "https://youtube.com/video" --model medium

# 2. Treinar voz com a transcrição
python tts_phase/tts_main.py train \
  --voice-name "voz_original" \
  --samples audio_original.wav

# 3. Sintetizar texto modificado
python tts_phase/tts_main.py synthesize \
  --text "Texto modificado da transcrição" \
  --voice-name "voz_original"
```

## 🎯 Casos de Uso

* 🎬 **Dublagem automática** de vídeos
* 📚 **Livros em áudio** personalizados
* 🎮 **Narração de jogos** com voz própria
* 📱 **Assistentes virtuais** personalizados
* 🎭 **Produção de podcasts** automatizada
* 📖 **Acessibilidade** para pessoas com deficiência

## 🤝 Contribuição

Para contribuir com a fase TTS:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas melhorias
4. Teste thoroughly
5. Submeta um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido com ❤️ como extensão do PROJETO_AUDIO**

### 🔗 Links Úteis

- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [Real-Time Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- [Gradio](https://gradio.app/)
- [Librosa](https://librosa.org/)

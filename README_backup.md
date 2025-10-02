# YouTube Audio Transcription

Este projeto permite baixar áudio de vídeos do YouTube e fazer transcrição automatizada usando ferramentas gratuitas e de alta qualidade.

## Características

### 🎵 Download de Áudio
- **yt-dlp**: Ferramenta mais robusta e atualizada para download do YouTube
- Suporte a diversos formatos de áudio
- Download direto em MP3 de alta qualidade

### 🎤 Transcrição de Áudio
- **OpenAI Whisper**: IA gratuita e altamente precisa para transcrição
- Funciona 100% offline (sem custos de API)
- Suporte nativo ao português brasileiro
- Múltiplos modelos disponíveis (tiny, base, small, medium, large)

### 💡 Vantagens sobre outras abordagens
- **Mais moderno** que youtube-dl e pytube
- **Mais preciso** que Google Speech Recognition
- **Totalmente gratuito** (sem limites de API)
- **Funciona offline** (sem dependência de internet após instalação)

## Estrutura do Projeto

```
PROJETO_AUDIO/
├── src/
│   ├── __init__.py
│   ├── youtube_downloader.py    # Download de áudio do YouTube
│   ├── audio_transcriber.py     # Transcrição com Whisper
│   ├── config.py               # Configurações do projeto
│   └── utils.py                # Utilitários gerais
├── tests/
│   ├── __init__.py
│   └── test_basic.py
├── output/                     # Arquivos de saída (áudio e texto)
├── requirements.txt            # Dependências do projeto
├── .gitignore                  # Arquivos a ignorar no Git
├── main.py                     # Script principal
└── README.md                   # Este arquivo
```

## Instalação

### Pré-requisitos (Windows)

1. **Python 3.8+** instalado
2. **FFmpeg** (necessário para processamento de áudio):
   ```powershell
   # Opção 1: Via Chocolatey (recomendado)
   choco install ffmpeg
   
   # Opção 2: Download manual
   # Baixe de: https://ffmpeg.org/download.html
   # Extraia e adicione ao PATH do Windows
   ```

### Instalação das Dependências

```powershell
# Clone ou baixe este projeto
cd PROJETO_AUDIO

# Instale as dependências Python
pip install -r requirements.txt
```

## Como Usar

### Uso Básico

```python
# Execute o script principal
python main.py

# Digite a URL do YouTube quando solicitado
# O programa irá:
# 1. Baixar o áudio em MP3
# 2. Transcrever usando Whisper
# 3. Salvar o texto na pasta output/
```

### Uso Avançado

```python
from src.youtube_downloader import YouTubeDownloader
from src.audio_transcriber import AudioTranscriber

# Configurar
downloader = YouTubeDownloader()
transcriber = AudioTranscriber(model_size="medium")  # ou "large" para máxima qualidade

# Baixar áudio
url = "https://www.youtube.com/watch?v=EXEMPLO"
audio_path = downloader.download(url)

# Transcrever
text = transcriber.transcribe(audio_path)
print(text)
```

## Modelos Whisper Disponíveis

| Modelo | Tamanho | Velocidade | Qualidade | Memória RAM |
|--------|---------|------------|-----------|-------------|
| tiny   | 39 MB   | Muito rápida | Básica    | ~1 GB       |
| base   | 74 MB   | Rápida       | Boa       | ~1 GB       |
| small  | 244 MB  | Moderada     | Muito boa | ~2 GB       |
| medium | 769 MB  | Lenta        | Excelente | ~5 GB       |
| large  | 1550 MB | Muito lenta  | Máxima    | ~10 GB      |

**Recomendação**: Use `medium` para melhor custo-benefício entre qualidade e velocidade.

## Comparação com Outras Ferramentas

### Download de Áudio
- ✅ **yt-dlp**: Mais rápido, mais formatos, mantido ativamente
- ❌ **youtube-dl**: Desatualizado, muitos vídeos não funcionam
- ❌ **pytube**: Simples mas frequentemente quebra

### Transcrição
- ✅ **OpenAI Whisper**: Gratuito, offline, altíssima precisão
- ❌ **Google Speech API**: Limites de uso, requer internet, menos preciso
- ❌ **Azure Speech**: Pago, requer conta Microsoft

## Requisitos do Sistema

- **Python**: 3.8 ou superior
- **RAM**: Mínimo 4GB (recomendado 8GB+ para modelos grandes)
- **Espaço**: ~2GB para modelos e dependências
- **Internet**: Apenas para download inicial e dos vídeos

## Solução de Problemas

### Erro de FFmpeg
```powershell
# Windows - instalar FFmpeg
choco install ffmpeg
# OU baixar manualmente e adicionar ao PATH
```

### Erro de memória
```python
# Use um modelo menor
transcriber = AudioTranscriber(model_size="small")  # ao invés de "large"
```

### URL não funciona
- Verifique se o vídeo não é privado
- Alguns vídeos têm proteção contra download
- Tente com outro vídeo público

## Desenvolvimento

Para contribuir com o projeto:

```powershell
# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Executar testes
python -m pytest tests/

# Executar com debug
python main.py --debug
```

## Licença

Este projeto é para uso educacional. Respeite os termos de uso do YouTube e direitos autorais dos conteúdos baixados.
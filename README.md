# 🎵 YouTube Audio Transcriber

Um projeto Python avançado para baixar áudios do YouTube e transcrevê-los com alta precisão usando yt-dlp, OpenAI Whisper e pós-processamento com IA.

## ✨ Recursos

- ✅ **Download inteligente** de áudios do YouTube usando yt-dlp
- ✅ **Transcrição de alta qualidade** usando OpenAI Whisper
- ✅ **Pós-processamento com IA** para correções semânticas e identificação de interlocutores
- ✅ **Múltiplos modelos** de IA (tiny, base, small, medium, large)
- ✅ **Suporte nativo ao português brasileiro**
- ✅ **Funcionamento 100% offline** (após download inicial dos modelos)
- ✅ **Interface de linha de comando** intuitiva
- ✅ **Logs detalhados** e informativos
- ✅ **Relatórios em Markdown** com formatação profissional
- ✅ **Teste com amostras** para validação rápida
- ✅ **Suporte a live streams** do YouTube

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/flaviomamede/PROJETO_AUDIO.git
cd PROJETO_AUDIO
```

### 2. Configure o ambiente Python
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Instale o FFmpeg
- **Windows**: `winget install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`
- **Mac**: `brew install ffmpeg`

## 📖 Como Usar

### 🎯 Uso Básico
```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### ⚙️ Uso Avançado
```bash
# Com modelo específico e pós-processamento IA
python main.py --url "URL_DO_VIDEO" --model medium

# Desabilitar pós-processamento IA
python main.py --url "URL_DO_VIDEO" --no-ai-enhance

# Teste rápido com amostra de 2 minutos
python main.py --test-sample --duration 120 --url "URL_DO_VIDEO"
```

## 🔧 Opções Disponíveis

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `--url` | URL do vídeo do YouTube | `--url "https://youtu.be/..."` |
| `--model` | Modelo Whisper | `--model medium` |
| `--test-sample` | Baixar apenas amostra | `--test-sample` |
| `--duration` | Duração da amostra (segundos) | `--duration 120` |
| `--no-ai-enhance` | Desabilitar pós-processamento IA | `--no-ai-enhance` |

## 🤖 Modelos Whisper

| Modelo | Tamanho | RAM | Velocidade | Qualidade | **Recomendado para** |
|--------|---------|-----|------------|-----------|----------------------|
| **tiny** | ~72 MB | ~1 GB | ⚡⚡⚡⚡ | ⭐⭐ | Testes rápidos |
| **base** | ~142 MB | ~1 GB | ⚡⚡⚡ | ⭐⭐⭐ | Uso casual |
| **small** | ~483 MB | ~2 GB | ⚡⚡ | ⭐⭐⭐⭐ | Boa qualidade |
| **medium** | ~1.4 GB | ~5 GB | ⚡ | ⭐⭐⭐⭐⭐ | **Recomendado** |
| **large** | ~3.1 GB | ~10 GB | 🐌 | ⭐⭐⭐⭐⭐ | Máxima precisão |

## 🧠 Pós-processamento com IA

O sistema inclui um módulo avançado de pós-processamento que:

- 🎯 **Identifica interlocutores** automaticamente
- ✏️ **Corrige erros semânticos** comuns
- 📝 **Melhora a pontuação** e capitalização  
- 🔧 **Aplica correções contextuais** específicas
- 📋 **Formata em Markdown** profissionalmente

### Exemplos de correções automáticas:
- "para comerciar" → "para conversar"
- "aceito com Vite" → "aceito o convite"
- "a doutora ou Zenia" → "a doutora Olzeni"

## 📁 Estrutura do Projeto

```
PROJETO_AUDIO/
├── 📂 src/
│   ├── 🔧 config.py              # Configurações
│   ├── 📥 youtube_downloader.py  # Download YouTube
│   ├── 🎙️ audio_transcriber.py   # Transcrição Whisper
│   ├── 🤖 ai_postprocessor.py    # Pós-processamento IA
│   └── 🛠️ utils.py              # Utilitários
├── 📂 tests/                    # Testes unitários
├── 📂 output/                   # Arquivos gerados (git ignore)
├── 🚀 main.py                   # Script principal
├── 📋 requirements.txt          # Dependências
└── 📖 README.md                # Documentação
```

## 📄 Arquivos Gerados

Para cada transcrição, o sistema gera:

1. **🎵 Áudio**: `output/titulo_do_video.webm`
2. **📝 Transcrição**: `output/titulo_do_video.txt` 
3. **📊 Relatório**: `output/titulo_do_video_transcricao.md`

## 🎯 Exemplo de Saída

```
📊 RESULTADOS:
==================================================
Arquivo de áudio: video_exemplo.webm
Caracteres transcritos: 45,230
Modelo usado: medium + pós-processamento IA

📝 PREVIEW DA TRANSCRIÇÃO:
**Apresentador**: Bem-vindos ao nosso podcast...
**Entrevistado**: Muito obrigado por ter me convidado...
```

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔗 Links Úteis

- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

---

**Desenvolvido com ❤️ por [Flavio Mamede](https://github.com/flaviomamede)**
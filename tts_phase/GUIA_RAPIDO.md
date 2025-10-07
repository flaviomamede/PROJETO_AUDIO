# 🚀 Guia Rápido - TTS com Clonagem de Voz

## ✅ Instalação Concluída!

O Coqui TTS foi instalado com sucesso no ambiente `projeto_audio_tts` (Python 3.11).

## 📍 Situação Atual

✅ **Sua voz já está pronta!**
- Arquivo: `tts_phase/voice_samples/20251002-130747.mp3`
- Duração: ~14 minutos (843 segundos)
- Qualidade: Excelente para treinamento

## 🎯 Próximos Passos

### 1️⃣ Treinar sua voz

```bash
# Ativar o ambiente correto
conda activate projeto_audio_tts

# Ir para o diretório TTS
cd tts_phase

# Treinar sua voz
python tts_main.py train \
  --voice-name "flavio_voz" \
  --samples voice_samples/20251002-130747.mp3
```

### 2️⃣ Testar a síntese de voz

```bash
# Sintetizar um texto simples
python tts_main.py synthesize \
  --text "Olá, esta é a minha voz clonada!" \
  --voice-name "flavio_voz" \
  --output teste_voz.wav
```

### 3️⃣ Sintetizar textos longos

```bash
# Criar arquivo com texto
echo "Primeiro parágrafo do texto longo" > meu_texto.txt
echo "Segundo parágrafo do texto longo" >> meu_texto.txt

# Sintetizar
python tts_main.py synthesize \
  --text "$(cat meu_texto.txt)" \
  --voice-name "flavio_voz" \
  --output audio_completo.wav
```

### 4️⃣ Síntese em lote

```bash
# Criar arquivo com vários textos (um por linha)
cat > textos_lote.txt << EOF
Primeiro texto para sintetizar
Segundo texto para sintetizar  
Terceiro texto para sintetizar
EOF

# Processar lote
python tts_main.py batch \
  --input-file textos_lote.txt \
  --voice-name "flavio_voz" \
  --output-dir ./audios_gerados
```

## ⚙️ Parâmetros Opcionais

### Controlar a voz

```bash
# Velocidade mais rápida
--speed 1.2

# Velocidade mais lenta
--speed 0.8

# Tom mais grave
--pitch 0.9

# Tom mais agudo
--pitch 1.1

# Volume mais alto
--volume 1.2
```

### Exemplo completo

```bash
python tts_main.py synthesize \
  --text "Este é um teste com parâmetros customizados" \
  --voice-name "flavio_voz" \
  --speed 1.1 \
  --pitch 0.95 \
  --volume 1.05 \
  --output audio_customizado.wav
```

## 🔍 Gerenciamento de Vozes

```bash
# Listar todas as vozes treinadas
python tts_main.py list

# Ver detalhes de uma voz
python tts_main.py info --voice-name "flavio_voz"

# Remover uma voz
python tts_main.py delete --voice-name "nome_voz" --confirm
```

## 🌐 Interface Web (Opcional)

```bash
# Iniciar interface gráfica
python tts_main.py web --port 7860

# Acessar no navegador
# http://localhost:7860
```

## 📝 Integração com Fase 1 (Transcrição)

Você pode usar a transcrição da Fase 1 para gerar áudios:

```bash
# 1. Transcrever vídeo (Fase 1 - ambiente projeto_audio)
conda activate projeto_audio
python main.py --url "URL_VIDEO" --model medium

# 2. Ativar ambiente TTS
conda activate projeto_audio_tts
cd tts_phase

# 3. Sintetizar a transcrição com sua voz
python tts_main.py synthesize \
  --text "$(cat ../output/NOME_DO_ARQUIVO.txt)" \
  --voice-name "flavio_voz" \
  --output audio_resintetizado.wav
```

## ⚠️ IMPORTANTE: Ambientes Separados

**Fase 1 (Transcrição)**: Python 3.12
```bash
conda activate projeto_audio
python main.py ...
```

**Fase 2 (TTS)**: Python 3.11
```bash
conda activate projeto_audio_tts
cd tts_phase
python tts_main.py ...
```

## 🎨 Exemplo Completo: Workflow Completo

```bash
# ===== FASE 1: TRANSCRIÇÃO =====
conda activate projeto_audio
cd /home/flavio/Documentos/PESSOAL/PROJETO_AUDIO/PROJETO_AUDIO

# Transcrever vídeo
python main.py --url "https://youtube.com/watch?v=VIDEO_ID" --model medium

# ===== FASE 2: TTS COM SUA VOZ =====
conda activate projeto_audio_tts
cd tts_phase

# Treinar sua voz (primeira vez apenas)
python tts_main.py train \
  --voice-name "flavio_voz" \
  --samples voice_samples/20251002-130747.mp3

# Sintetizar texto modificado com sua voz
python tts_main.py synthesize \
  --text "Texto editado ou resumido da transcrição" \
  --voice-name "flavio_voz" \
  --output audio_final.wav
```

## 🆘 Solução de Problemas

### Erro: "Modelo não encontrado"
```bash
# O modelo será baixado automaticamente na primeira vez
# Aguarde o download (~2GB)
```

### Erro: "No module named 'TTS'"
```bash
# Certifique-se de estar no ambiente correto
conda activate projeto_audio_tts
```

### Erro: "CUDA out of memory"
```bash
# Use CPU em vez de GPU
export CUDA_VISIBLE_DEVICES=""
```

### Qualidade de voz ruim
- Use mais tempo de áudio (recomendado: 5-15 minutos)
- Garanta áudio limpo, sem ruído
- Use áudio com apenas uma pessoa falando

## 📊 Performance Esperada

- **Treinamento**: ~1-5 minutos (primeira vez)
- **Síntese**: ~1-2 segundos por segundo de áudio
- **Qualidade**: Excelente com 10+ minutos de áudio de treinamento

## 🎯 Casos de Uso

1. **Narração de textos** com sua voz
2. **Dublagem** de vídeos
3. **Podcasts** automatizados
4. **Audiobooks** personalizados
5. **Assistentes virtuais** com sua voz
6. **Legendas em áudio** para vídeos

## 📚 Documentação Completa

Para mais detalhes, veja:
- `README_TTS.md` - Documentação completa
- `tts_main.py --help` - Ajuda dos comandos

---

**🎤 Agora é só começar a clonar sua voz!**

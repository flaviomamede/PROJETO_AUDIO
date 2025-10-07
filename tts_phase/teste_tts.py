#!/usr/bin/env python3
"""
Teste simples do Coqui TTS para verificar se está funcionando
"""

import os
import sys
from pathlib import Path

# Verificar se estamos no diretório correto
print(f"Diretório atual: {os.getcwd()}")
print(f"Arquivo de voz: {Path('voice_samples/20251002-130747.mp3').exists()}")

try:
    from TTS.api import TTS
    print("✅ Coqui TTS importado com sucesso!")
    
    # Pular listagem de modelos por enquanto
    print("\n🔍 Modelos disponíveis (pulando listagem)")
    
    # Tentar carregar um modelo básico
    print("\n🔄 Carregando modelo básico...")
    tts = TTS("tts_models/pt/cv/vits")
    print("✅ Modelo carregado com sucesso!")
    
    # Testar síntese básica
    print("\n🎤 Testando síntese de voz...")
    texto_teste = "Olá, este é um teste do sistema de síntese de voz."
    
    output_path = Path("output/teste_basico.wav")
    output_path.parent.mkdir(exist_ok=True)
    
    tts.tts_to_file(
        text=texto_teste,
        file_path=str(output_path)
    )
    
    print(f"✅ Áudio de teste gerado: {output_path}")
    print(f"📁 Tamanho do arquivo: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Testar com sua voz (zero-shot)
    print("\n🎯 Testando com sua voz...")
    voz_path = Path("voice_samples/20251002-130747.mp3")
    
    if voz_path.exists():
        print(f"📂 Usando arquivo de voz: {voz_path}")
        
        output_path_voz = Path("output/teste_com_sua_voz.wav")
        
        # Usar modelo que suporta speaker_wav
        tts_voz = TTS("tts_models/multilingual/multi-dataset/your_tts")
        
        tts_voz.tts_to_file(
            text="Olá, esta é minha voz clonada!",
            speaker_wav=str(voz_path),
            file_path=str(output_path_voz),
            language="pt-br"
        )
        
        print(f"✅ Áudio com sua voz gerado: {output_path_voz}")
        print(f"📁 Tamanho do arquivo: {output_path_voz.stat().st_size / 1024:.1f} KB")
        
    else:
        print(f"❌ Arquivo de voz não encontrado: {voz_path}")
    
    print("\n🎉 Teste concluído com sucesso!")
    
except ImportError as e:
    print(f"❌ Erro ao importar TTS: {e}")
    print("Execute: pip install TTS")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

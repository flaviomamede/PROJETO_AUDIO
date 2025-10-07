#!/usr/bin/env python3
"""
Teste do TTS com um parágrafo completo usando sua voz clonada
"""

from TTS.api import TTS
from pathlib import Path

# Texto do parágrafo para testar
texto_paragrafo = """
A inteligência artificial representa uma das maiores revoluções tecnológicas do século XXI. 
Ela tem transformado profundamente diversos setores da sociedade, desde a medicina até o 
entretenimento. No campo da educação, a IA oferece oportunidades únicas para personalizar 
o aprendizado e adaptar o ensino às necessidades individuais de cada estudante. 
Além disso, a automação de processos complexos tem permitido que profissionais se concentrem 
em tarefas mais criativas e estratégicas. Contudo, é fundamental abordar os desafios éticos 
e garantir que essa tecnologia seja desenvolvida de forma responsável e inclusiva.
"""

def main():
    print("🎤 Testando TTS com parágrafo completo...")
    print(f"📝 Tamanho do texto: {len(texto_paragrafo)} caracteres")
    print(f"📊 Número de palavras: {len(texto_paragrafo.split())}")
    
    # Carregar modelo de clonagem de voz
    print("\n🔄 Carregando modelo de clonagem...")
    tts = TTS("tts_models/multilingual/multi-dataset/your_tts")
    
    # Arquivo de saída
    output_path = Path("output/teste_paragrafo_completo.wav")
    output_path.parent.mkdir(exist_ok=True)
    
    # Arquivo da sua voz
    voz_path = Path("voice_samples/20251002-130747.mp3")
    
    print(f"📂 Usando arquivo de voz: {voz_path.name}")
    print("🎯 Gerando áudio com sua voz clonada...")
    
    # Gerar áudio com sua voz
    tts.tts_to_file(
        text=texto_paragrafo,
        speaker_wav=str(voz_path),
        file_path=str(output_path),
        language="pt-br"
    )
    
    # Informações do arquivo gerado
    if output_path.exists():
        tamanho_kb = output_path.stat().st_size / 1024
        print(f"\n✅ Parágrafo sintetizado com sucesso!")
        print(f"📁 Arquivo gerado: {output_path}")
        print(f"📊 Tamanho: {tamanho_kb:.1f} KB")
        print(f"🎵 Duração estimada: ~{len(texto_paragrafo.split()) * 0.5:.1f} segundos")
        
        # Teste adicional: parágrafo mais curto para comparação
        print("\n🔄 Gerando teste adicional com texto mais curto...")
        
        texto_curto = "Olá! Este é um teste rápido para verificar a qualidade da síntese de voz. " \
                     "A clonagem de voz permite criar áudios personalizados com características únicas. " \
                     "Esta tecnologia tem aplicações incríveis em diversos campos."
        
        output_curto = Path("output/teste_texto_curto.wav")
        
        tts.tts_to_file(
            text=texto_curto,
            speaker_wav=str(voz_path),
            file_path=str(output_curto),
            language="pt-br"
        )
        
        if output_curto.exists():
            tamanho_curto = output_curto.stat().st_size / 1024
            print(f"✅ Teste curto gerado: {output_curto}")
            print(f"📊 Tamanho: {tamanho_curto:.1f} KB")
        
        print("\n🎉 Testes concluídos! Ouça os arquivos para avaliar a qualidade!")
        
    else:
        print("❌ Erro ao gerar arquivo de áudio")

if __name__ == "__main__":
    main()

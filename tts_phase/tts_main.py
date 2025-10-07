#!/usr/bin/env python3
"""
Script principal para TTS com clonagem de voz
Fase 2 do PROJETO_AUDIO - Text-to-Speech com Voice Cloning
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.tts_engine import TTSEngine
    from config.tts_config import ensure_directories, update_device_config
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Execute: pip install -r requirements_tts.txt")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tts_phase/tts.log')
    ]
)

logger = logging.getLogger(__name__)

class TTSApp:
    """Aplicação principal para TTS com clonagem de voz."""
    
    def __init__(self):
        self.engine = None
        self.model_type = "coqui"
        
    def run(self, args):
        """
        Executa a aplicação TTS baseada nos argumentos fornecidos.
        
        Args:
            args: Argumentos da linha de comando
        """
        logger.info("🎤 TTS Phase - Text-to-Speech com Voice Cloning")
        logger.info("=" * 60)
        
        # Garantir que diretórios existem
        ensure_directories()
        update_device_config()
        
        # Inicializar engine
        self.engine = TTSEngine(model_type=args.model_type)
        
        if not self.engine.initialize():
            logger.error("Falha na inicialização do engine TTS")
            return False
        
        # Executar comando baseado nos argumentos
        if args.command == "train":
            return self._train_voice(args)
        elif args.command == "synthesize":
            return self._synthesize_text(args)
        elif args.command == "batch":
            return self._batch_synthesis(args)
        elif args.command == "list":
            return self._list_voices(args)
        elif args.command == "info":
            return self._voice_info(args)
        elif args.command == "delete":
            return self._delete_voice(args)
        elif args.command == "web":
            return self._start_web_interface(args)
        else:
            logger.error(f"Comando não reconhecido: {args.command}")
            return False
    
    def _train_voice(self, args):
        """Treina uma nova voz"""
        try:
            logger.info(f"🎯 Treinando voz: {args.voice_name}")
            
            # Validar amostras
            voice_samples = [Path(s) for s in args.samples]
            invalid_samples = [s for s in voice_samples if not s.exists()]
            
            if invalid_samples:
                logger.error(f"Amostras não encontradas: {invalid_samples}")
                return False
            
            # Carregar textos se fornecidos
            text_samples = None
            if args.texts:
                try:
                    with open(args.texts, 'r', encoding='utf-8') as f:
                        text_samples = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    logger.error(f"Erro ao carregar textos: {str(e)}")
                    return False
            
            # Treinar voz
            success = self.engine.train_voice_from_samples(
                voice_name=args.voice_name,
                voice_samples=voice_samples,
                text_samples=text_samples
            )
            
            if success:
                logger.info(f"✅ Voz '{args.voice_name}' treinada com sucesso!")
                self._show_voice_info(args.voice_name)
            else:
                logger.error(f"❌ Falha no treinamento da voz '{args.voice_name}'")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {str(e)}")
            return False
    
    def _synthesize_text(self, args):
        """Sintetiza texto em áudio"""
        try:
            logger.info(f"🎵 Sintetizando: {args.text[:50]}...")
            
            # Parâmetros de síntese
            synthesis_params = {
                "speed": args.speed,
                "pitch": args.pitch,
                "volume": args.volume
            }
            
            # Sintetizar
            output_path = self.engine.synthesize(
                text=args.text,
                voice_name=args.voice_name,
                reference_voice=args.reference_voice,
                output_path=args.output,
                **synthesis_params
            )
            
            if output_path:
                logger.info(f"✅ Áudio gerado: {output_path}")
                self._show_audio_info(output_path)
                return True
            else:
                logger.error("❌ Falha na síntese")
                return False
                
        except Exception as e:
            logger.error(f"Erro na síntese: {str(e)}")
            return False
    
    def _batch_synthesis(self, args):
        """Síntese em lote"""
        try:
            logger.info(f"📦 Processando lote: {args.input_file}")
            
            # Carregar textos
            with open(args.input_file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Textos carregados: {len(texts)}")
            
            # Parâmetros
            synthesis_params = {
                "speed": args.speed,
                "pitch": args.pitch,
                "volume": args.volume
            }
            
            # Processar em lote
            results = self.engine.synthesize_batch(
                texts=texts,
                voice_name=args.voice_name,
                reference_voice=args.reference_voice,
                output_dir=args.output_dir,
                **synthesis_params
            )
            
            successful = sum(1 for r in results if r is not None)
            logger.info(f"✅ Lote concluído: {successful}/{len(texts)} sucessos")
            
            return successful > 0
            
        except Exception as e:
            logger.error(f"Erro na síntese em lote: {str(e)}")
            return False
    
    def _list_voices(self, args):
        """Lista vozes disponíveis"""
        try:
            voices = self.engine.list_voices()
            
            if not voices:
                print("📭 Nenhuma voz treinada encontrada")
                return True
            
            print(f"\n🎭 VOZES DISPONÍVEIS ({len(voices)}):")
            print("=" * 50)
            
            for voice in voices:
                info = voice["info"]
                print(f"\n📢 {voice['name']}")
                print(f"   Amostras: {voice['samples']}")
                if "total_duration" in info:
                    print(f"   Duração total: {info['total_duration']:.1f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao listar vozes: {str(e)}")
            return False
    
    def _voice_info(self, args):
        """Mostra informações de uma voz específica"""
        try:
            info = self.engine.get_voice_details(args.voice_name)
            
            if "error" in info:
                print(f"❌ {info['error']}")
                return False
            
            print(f"\n🎭 INFORMAÇÕES DA VOZ: {args.voice_name}")
            print("=" * 50)
            print(f"Amostras: {info.get('sample_count', 0)}")
            print(f"Duração total: {info.get('total_duration', 0):.1f}s")
            
            if info.get('samples'):
                print("\n📁 Amostras:")
                for sample in info['samples']:
                    print(f"   • {sample['file']} ({sample['duration']:.1f}s)")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao obter informações: {str(e)}")
            return False
    
    def _delete_voice(self, args):
        """Remove uma voz"""
        try:
            if not args.confirm:
                confirm = input(f"Tem certeza que deseja remover a voz '{args.voice_name}'? [y/N]: ")
                if confirm.lower() not in ['y', 'yes']:
                    logger.info("Operação cancelada")
                    return True
            
            success = self.engine.delete_voice(args.voice_name)
            
            if success:
                logger.info(f"✅ Voz '{args.voice_name}' removida com sucesso")
            else:
                logger.error(f"❌ Falha ao remover voz '{args.voice_name}'")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao remover voz: {str(e)}")
            return False
    
    def _start_web_interface(self, args):
        """Inicia interface web"""
        try:
            logger.info("🌐 Iniciando interface web...")
            
            # Importar e iniciar interface web
            from src.web_interface import start_web_interface
            
            start_web_interface(
                host=args.host,
                port=args.port,
                share=args.share
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na interface web: {str(e)}")
            return False
    
    def _show_voice_info(self, voice_name: str):
        """Mostra informações da voz treinada"""
        info = self.engine.get_voice_details(voice_name)
        
        print(f"\n📊 INFORMAÇÕES DA VOZ TREINADA:")
        print(f"   Nome: {voice_name}")
        print(f"   Amostras: {info.get('sample_count', 0)}")
        print(f"   Duração total: {info.get('total_duration', 0):.1f}s")
    
    def _show_audio_info(self, audio_path: Path):
        """Mostra informações do áudio gerado"""
        try:
            import librosa
            duration = librosa.get_duration(filename=str(audio_path))
            size = audio_path.stat().st_size / 1024 / 1024  # MB
            
            print(f"\n📊 INFORMAÇÕES DO ÁUDIO:")
            print(f"   Arquivo: {audio_path.name}")
            print(f"   Duração: {duration:.1f}s")
            print(f"   Tamanho: {size:.1f} MB")
            
        except Exception as e:
            logger.warning(f"Erro ao obter informações do áudio: {str(e)}")

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="TTS com clonagem de voz - Fase 2 do PROJETO_AUDIO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Treinar nova voz
  %(prog)s train --voice-name "minha_voz" --samples audio1.wav audio2.wav

  # Sintetizar texto
  %(prog)s synthesize --text "Olá mundo" --voice-name "minha_voz"

  # Síntese em lote
  %(prog)s batch --input-file textos.txt --voice-name "minha_voz"

  # Listar vozes
  %(prog)s list

  # Interface web
  %(prog)s web --port 7860

Modelos disponíveis:
  coqui    - Coqui XTTS v2 (recomendado)
  rtvc     - Real-Time Voice Cloning
  custom   - Modelos customizados
        """
    )
    
    # Comando principal
    parser.add_argument(
        'command',
        choices=['train', 'synthesize', 'batch', 'list', 'info', 'delete', 'web'],
        help='Comando a executar'
    )
    
    # Configurações gerais
    parser.add_argument(
        '--model-type', '-m',
        choices=['coqui', 'rtvc', 'custom'],
        default='coqui',
        help='Tipo de modelo TTS (padrão: coqui)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso'
    )
    
    # Comandos de treinamento
    parser.add_argument(
        '--voice-name', '-n',
        help='Nome da voz'
    )
    
    parser.add_argument(
        '--samples', '-s',
        nargs='+',
        help='Arquivos de amostra de voz'
    )
    
    parser.add_argument(
        '--texts', '-t',
        help='Arquivo com textos correspondentes às amostras'
    )
    
    # Comandos de síntese
    parser.add_argument(
        '--text',
        help='Texto para sintetizar'
    )
    
    parser.add_argument(
        '--reference-voice', '-r',
        help='Arquivo de áudio de referência'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Arquivo de saída'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Diretório de saída para lote'
    )
    
    parser.add_argument(
        '--input-file', '-i',
        help='Arquivo com textos para síntese em lote'
    )
    
    # Parâmetros de síntese
    parser.add_argument(
        '--speed',
        type=float,
        default=1.0,
        help='Velocidade de fala (padrão: 1.0)'
    )
    
    parser.add_argument(
        '--pitch',
        type=float,
        default=1.0,
        help='Tom de voz (padrão: 1.0)'
    )
    
    parser.add_argument(
        '--volume',
        type=float,
        default=1.0,
        help='Volume (padrão: 1.0)'
    )
    
    # Interface web
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host para interface web'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=7860,
        help='Porta para interface web'
    )
    
    parser.add_argument(
        '--share',
        action='store_true',
        help='Compartilhar interface web publicamente'
    )
    
    # Confirmação
    parser.add_argument(
        '--confirm',
        action='store_true',
        help='Confirmar operações destrutivas'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Executar aplicação
    try:
        app = TTSApp()
        success = app.run(args)
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
YouTube Audio Transcription Tool

Script principal para baixar áudio do YouTube e fazer transcrição automatizada.
Utiliza yt-dlp para download e OpenAI Whisper para transcrição.

Exemplo de uso:
    python main.py
    python main.py --url "https://www.youtube.com/watch?v=EXEMPLO"
    python main.py --model large --timestamps
    python main.py --test-sample --duration 60  # Baixar apenas 1 minuto para teste
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.youtube_downloader import YouTubeDownloader
    from src.audio_transcriber import AudioTranscriber
    from src.utils import get_logger, format_duration, validate_url
    from src.config import OUTPUT_DIR
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

logger = get_logger(__name__)

class YouTubeTranscriptionApp:
    """Aplicação principal para download e transcrição de áudio do YouTube."""
    
    def __init__(self):
        self.downloader = YouTubeDownloader()
        self.transcriber = None  # Será inicializado com modelo escolhido
        
    def run(self, args):
        """
        Executa o processo completo de download e transcrição.
        
        Args:
            args: Argumentos da linha de comando
        """
        logger.info("🎵 YouTube Audio Transcription Tool")
        logger.info("=" * 50)
        
        # URL de exemplo se não fornecida
        if not args.url and not args.interactive:
            # URL do vídeo de exemplo fornecido pelo usuário
            args.url = "https://www.youtube.com/live/o6MbvfXckec?si=z40QXIfwR0L7wT6t"
            logger.info(f"📺 Usando vídeo de exemplo: {args.url}")
        
        # Configurar transcriber com modelo escolhido
        self.transcriber = AudioTranscriber(
            model_size=args.model,
            language='pt'
        )
        
        # Obter URL
        url = args.url or self._get_url_from_user()
        
        if not validate_url(url):
            logger.error("URL inválida")
            return False
        
        # Mostrar informações do vídeo
        if not args.quiet:
            self._show_video_info(url)
        
        # Confirmar se é teste com amostra
        if args.test_sample:
            duration = args.duration or 60
            logger.info(f"🧪 Modo teste: baixando apenas {duration} segundos")
            if not args.quiet:
                confirm = input(f"Continuar com teste de {duration}s? [Y/n]: ").strip().lower()
                if confirm and confirm != 'y' and confirm != 'yes':
                    logger.info("❌ Teste cancelado pelo usuário")
                    return False
        
        # Download do áudio
        logger.info("📥 Iniciando download...")
        
        if args.test_sample:
            duration = args.duration or 60
            audio_file = self.downloader.download_sample(url, args.filename, duration)
        else:
            audio_file = self.downloader.download(url, args.filename)
        
        if not audio_file:
            logger.error("Falha no download")
            return False
        
        # Transcrição
        logger.info("🎤 Iniciando transcrição...")
        text = self.transcriber.transcribe(
            audio_file, 
            include_timestamps=args.timestamps,
            enhance_with_ai=not args.no_ai_enhance
        )
        
        if not text:
            logger.error("Falha na transcrição")
            return False
        
        # Gerar arquivo markdown formatado
        if not args.test_sample or (args.test_sample and not args.quiet):
            self._generate_markdown_report(url, audio_file, text, args)
        
        # Mostrar resultado
        if not args.quiet:
            self._show_results(audio_file, text, args.timestamps)
        
        logger.info("✅ Processo concluído com sucesso!")
        return True
    
    def _get_url_from_user(self) -> str:
        """Solicita URL do usuário via input."""
        try:
            print("\n" + "=" * 50)
            print("🎬 BAIXAR E TRANSCREVER ÁUDIO DO YOUTUBE")
            print("=" * 50)
            print("\nCole a URL do vídeo do YouTube:")
            print("Exemplos válidos:")
            print("  • https://www.youtube.com/watch?v=XXXXXXXXX")
            print("  • https://youtu.be/XXXXXXXXX")
            print()
            
            url = input("URL: ").strip()
            print()
            return url
            
        except KeyboardInterrupt:
            print("\n\n❌ Operação cancelada pelo usuário")
            sys.exit(0)
    
    def _show_video_info(self, url: str):
        """Mostra informações do vídeo antes do download."""
        info = self.downloader.get_video_info(url)
        
        if info:
            print("\n📋 INFORMAÇÕES DO VÍDEO:")
            print(f"   Título: {info['title']}")
            print(f"   Canal: {info['uploader']}")
            print(f"   Duração: {format_duration(info['duration'])}")
            print(f"   Visualizações: {info['view_count']:,}")
            print()
    
    def _show_results(self, audio_file: Path, text: str, with_timestamps: bool):
        """Mostra os resultados finais."""
        print("\n" + "=" * 50)
        print("📊 RESULTADOS:")
        print("=" * 50)
        print(f"Arquivo de áudio: {audio_file.name}")
        print(f"Arquivo de texto: {audio_file.with_suffix('.txt').name}")
        print(f"Caracteres transcritos: {len(text):,}")
        
        # Preview do texto
        preview_length = 200 if with_timestamps else 300
        preview = text[:preview_length]
        if len(text) > preview_length:
            preview += "..."
        
        print(f"\n📝 PREVIEW DA TRANSCRIÇÃO:")
        print("-" * 30)
        print(preview)
        print("-" * 30)
        
        print(f"\n📂 Arquivos salvos em: {OUTPUT_DIR}")
    
    def _generate_markdown_report(self, url: str, audio_file: Path, text: str, args):
        """Gera um relatório markdown formatado da transcrição."""
        try:
            # Obter informações do vídeo
            info = self.downloader.get_video_info(url)
            
            # Nome do arquivo markdown
            base_name = audio_file.stem
            md_file = OUTPUT_DIR / f"{base_name}_transcricao.md"
            
            # Gerar conteúdo markdown
            content = self._format_markdown_content(url, info, text, args)
            
            # Salvar arquivo
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"📝 Relatório markdown salvo: {md_file.name}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar markdown: {str(e)}")
    
    def _format_markdown_content(self, url: str, info: dict, text: str, args) -> str:
        """Formata o conteúdo do markdown."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# Transcrição de Áudio - YouTube

## Informações do Vídeo

**URL:** {url}

**Título:** {info.get('title', 'Desconhecido') if info else 'Não disponível'}

**Canal:** {info.get('uploader', 'Desconhecido') if info else 'Não disponível'}

**Duração:** {format_duration(info.get('duration', 0)) if info else 'Não disponível'}

**Visualizações:** {info.get('view_count', 0):,} if info else 'Não disponível'

## Detalhes da Transcrição

**Data da Transcrição:** {now}

**Modelo Whisper:** {args.model}

**Inclui Timestamps:** {'Sim' if args.timestamps else 'Não'}

**Modo:** {'Teste ({} segundos)'.format(args.duration or 60) if args.test_sample else 'Completo'}

## Transcrição

"""
        
        # Adicionar a transcrição com formatação
        if args.timestamps:
            # Se tem timestamps, já está formatado
            content += text
        else:
            # Quebrar texto em parágrafos para melhor legibilidade
            paragraphs = text.split('. ')
            formatted_text = ""
            
            for i, paragraph in enumerate(paragraphs):
                # Adicionar ponto se não for o último
                if i < len(paragraphs) - 1:
                    paragraph += '.'
                
                # Quebrar linhas a cada ~3-4 sentenças para melhor legibilidade
                if i > 0 and i % 3 == 0:
                    formatted_text += "\n\n"
                
                formatted_text += paragraph + " "
            
            content += formatted_text.strip()
        
        content += f"""

## Estatísticas

**Caracteres:** {len(text):,}

**Palavras:** {len(text.split()):,}

---
*Transcrito automaticamente com OpenAI Whisper*
"""
        
        return content

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Baixa áudio do YouTube e faz transcrição automatizada",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s
  %(prog)s --url "https://www.youtube.com/watch?v=EXEMPLO"
  %(prog)s --model large --timestamps
  %(prog)s --filename "minha_palestra" --quiet

Modelos disponíveis:
  tiny   - Muito rápido, qualidade básica (~72 MB)
  base   - Rápido, boa qualidade (~142 MB)  
  small  - Moderado, muito boa qualidade (~483 MB)
  medium - Lento, excelente qualidade (~1.4 GB) [PADRÃO]
  large  - Muito lento, máxima qualidade (~3.1 GB)
        """
    )
    
    parser.add_argument(
        '--url', '-u',
        help='URL do vídeo do YouTube'
    )
    
    parser.add_argument(
        '--model', '-m',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='medium',
        help='Modelo Whisper para transcrição (padrão: medium)'
    )
    
    parser.add_argument(
        '--filename', '-f',
        help='Nome customizado para o arquivo (sem extensão)'
    )
    
    parser.add_argument(
        '--timestamps', '-t',
        action='store_true',
        help='Incluir timestamps na transcrição'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Modo silencioso (menos output)'
    )
    
    parser.add_argument(
        '--test-sample', '-s',
        action='store_true',
        help='Baixar apenas uma amostra para teste'
    )
    
    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=60,
        help='Duração da amostra em segundos (padrão: 60)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Modo interativo (solicita URL do usuário)'
    )
    
    parser.add_argument(
        '--no-ai-enhance',
        action='store_true',
        help='Desabilitar pós-processamento com IA'
    )
    
    args = parser.parse_args()
    
    # Executar aplicação
    try:
        app = YouTubeTranscriptionApp()
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
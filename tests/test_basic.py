"""
Testes básicos para o projeto de transcrição de áudio do YouTube.
Execute com: python -m pytest tests/
"""

import pytest
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.utils import sanitize_filename, format_duration, validate_url
from src.config import OUTPUT_DIR

class TestUtils:
    """Testes para funções utilitárias."""
    
    def test_sanitize_filename(self):
        """Testa sanitização de nomes de arquivo."""
        assert sanitize_filename("Test<>File|Name") == "Test__File_Name"
        assert sanitize_filename("Normal File.mp3") == "Normal File.mp3"
        assert sanitize_filename("File/with\\slashes") == "File_with_slashes"
    
    def test_format_duration(self):
        """Testa formatação de duração."""
        assert format_duration(65) == "1:05"
        assert format_duration(3661) == "1:01:01"
        assert format_duration(30) == "0:30"
    
    def test_validate_url(self):
        """Testa validação de URLs."""
        assert validate_url("https://www.youtube.com/watch?v=test")
        assert validate_url("http://youtu.be/test")
        assert not validate_url("not-a-url")
        assert not validate_url("")

class TestConfig:
    """Testes para configuração."""
    
    def test_output_dir_exists(self):
        """Verifica se o diretório de saída existe."""
        assert OUTPUT_DIR.exists()
        assert OUTPUT_DIR.is_dir()

def test_project_structure():
    """Verifica estrutura básica do projeto."""
    project_root = Path(__file__).parent.parent
    
    # Verificar arquivos essenciais
    assert (project_root / "main.py").exists()
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "README.md").exists()
    
    # Verificar diretórios
    assert (project_root / "src").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "output").exists()
    
    # Verificar módulos src
    assert (project_root / "src" / "__init__.py").exists()
    assert (project_root / "src" / "config.py").exists()
    assert (project_root / "src" / "utils.py").exists()

if __name__ == "__main__":
    pytest.main([__file__])
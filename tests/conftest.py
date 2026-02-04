"""Configuration pytest pour les tests."""
import sys
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH pour les imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import sys
from pathlib import Path

# This ensures that the PYTHONPATH is correct on any environment when running pytest
project_path = Path(__file__).resolve().parent
if str(project_path) not in sys.path:
    sys.path.insert(0, str(project_path))

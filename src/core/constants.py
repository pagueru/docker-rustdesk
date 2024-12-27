"""
Define constantes baseadas nos caminhos do sistema de arquivos, 
facilitando o acesso a diretórios e arquivos frequentemente utilizados no projeto.

- Constantes de pastas
- Constantes de arquivos
"""

from pathlib import Path

# Atribui as constantes raízes
FILE_PATH = Path(__file__).resolve()
PROJECT_PATH = FILE_PATH.parents[2]

# Atribui as constantes de pastas
LOGS_PATH = PROJECT_PATH / "logs"
SRC_PATH = PROJECT_PATH / "src"
CONFIG_PATH = PROJECT_PATH / "config"
CORE_PATH = SRC_PATH / "core"
SCRIPTS_PATH = PROJECT_PATH / "scripts"
OUTPUT_PATH = SCRIPTS_PATH / "output"

# Atribui as constantes de arquivos
LOG_FILE = LOGS_PATH / "app.log"
JSON_FILE = CONFIG_PATH / "firewall_rules.json"

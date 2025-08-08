import json
from pathlib import Path
from typing import Dict, Any, Optional

def load_json_data(file_name: str) -> Optional[Dict[str, Any]]:
    """
    Carrega dados de um arquivo JSON do diretório 'data'.
    Retorna None se o arquivo não for encontrado ou estiver mal formatado.
    """
    from core.colors import GameColors as C
    
    path = Path(__file__).parent.parent / "data" / file_name
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{C.DANGER}Erro: Arquivo '{file_name}' não encontrado em {path}.")
        return None
    except json.JSONDecodeError:
        print(f"{C.DANGER}Erro: Arquivo '{file_name}' mal formatado. Por favor, verifique a sintaxe JSON.")
        return None

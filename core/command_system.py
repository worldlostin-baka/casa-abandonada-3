from colorama import Style
from core.colors import GameColors as C

class CommandSystem:
    """Sistema avançado de interpretação de comandos"""
    
    VERBS = {
        'mover': 'move', 'ir': 'move', 'andar': 'move', 'navegar': 'move',
        'inspecionar': 'examine', 'examinar': 'examine',
        'ver': 'look', 'olhar': 'look',
        'pegar': 'take', 'coletar': 'take',
        'usar': 'use',
        'combinar': 'combine', 'juntar': 'combine',
        'inventario': 'inventory', 'inv': 'inventory',
        'sair': 'quit', 'terminar': 'quit',
        'ajuda': 'help'
    }

    @staticmethod
    def parse(cmd):
        """Interpreta o comando do jogador"""
        cmd = cmd.lower().strip()
        if not cmd:
            return None
            
        parts = cmd.split()
        action = CommandSystem.VERBS.get(parts[0])
        
        if not action:
            return {'action': 'unknown', 'original': cmd}
            
        if action in {'inventory', 'quit', 'help'}:
            return {'action': action}
        
        elif action in {'move', 'examine', 'look', 'take', 'use'}:
            if len(parts) > 1:
                return {'action': action, 'target': ' '.join(parts[1:])}
            
        elif action == 'combine':
            if len(parts) >= 3:
                return {'action': action, 'items': [parts[1], parts[2]]}
                
        return {'action': action, 'target': None} # Retorna o comando mesmo sem target
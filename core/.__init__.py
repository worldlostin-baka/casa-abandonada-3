# Package initialization
from .character import Character
from .game_state import GameState
from .items import Item, Inventory
from .world import Room, World
from .quizzes import QuizSystem
from .puzzles import PuzzleSystem
from .colors import GameColors # Adicionado para consistência, embora já importado diretamente
from .command_system import CommandSystem # Adicionado para consistência

__all__ = ['Character', 'GameState', 'Item', 'Inventory', 'Room', 'World', 
           'QuizSystem', 'PuzzleSystem', 'GameColors', 'CommandSystem']

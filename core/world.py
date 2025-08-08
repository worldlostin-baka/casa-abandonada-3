import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from core.utils import load_json_data
from core.colors import GameColors as C

class Room:
    """
    Classe que representa uma sala no jogo.
    Cada sala tem um nome, descrição, itens e conexões com outras salas.
    """
    def __init__(self, name: str, description: str, items: List[str] = None, quiz_id: str = None, puzzle_id: str = None):
        self.name = name
        self.description = description
        self.items = items if items is not None else []
        self.quiz_id = quiz_id
        self.puzzle_id = puzzle_id
        self.connections: Dict[str, str] = {}  # Direções: {'norte': 'sala1', 'sul': 'sala2'}

class World:
    """
    Classe que gerencia todas as salas e conexões do jogo.
    É responsável por carregar a estrutura do mundo a partir de um arquivo JSON.
    """
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
    
    @staticmethod
    def load_from_json(file_name: str = "world.json") -> Optional['World']:
        """
        Carrega as salas e conexões do arquivo JSON e retorna um objeto World.
        Retorna None se houver um erro.
        """
        world = World()
        world_data = load_json_data(file_name)
        if not world_data:
            print(f"{C.DANGER}Não foi possível carregar os dados do mundo. O jogo não pode continuar.{C.RESET}")
            return None
            
        # Carrega cada sala
        for room_name, room_config in world_data.items():
            new_room = Room(
                name=room_config.get('name'),
                description=room_config.get('description'),
                items=room_config.get('items', []),
                quiz_id=room_config.get('quiz_id'),
                puzzle_id=room_config.get('puzzle_id')
            )
            world.rooms[room_name] = new_room
            
        # Estabelece as conexões entre as salas
        for room_name, room_config in world_data.items():
            current_room = world.get_room(room_name)
            if current_room:
                for direction, target_room_name in room_config.get('connections', {}).items():
                    current_room.connections[direction] = target_room_name
        
        return world

    def add_room(self, room: Room) -> None:
        """Adiciona uma sala ao mundo."""
        self.rooms[room.name] = room
    
    def get_room(self, room_name: str) -> Optional[Room]:
        """Retorna uma sala pelo nome."""
        return self.rooms.get(room_name)
    
    def get_connected_room(self, current_room_name: str, direction: str) -> Optional[str]:
        """
        Retorna o nome da sala conectada a partir de uma direção.
        """
        room = self.get_room(current_room_name)
        if room:
            return room.connections.get(direction)
        return None

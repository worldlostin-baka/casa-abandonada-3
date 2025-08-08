import json
import random
from typing import Dict, List, Optional, Any
from core.items import Item, Inventory
from core.world import World, Room
from core.character import Character
from core.quizzes import QuizSystem
from core.puzzles import PuzzleSystem
from core.colors import GameColors as C
from core.utils import load_json_data
from pathlib import Path

# Configurações do jogo - podem ser movidas para um arquivo de configuração
GAME_CONFIG = {
    "start_room": "hall_entrada",
    "inventory_limit": 5,
    "max_health": 100,
    "max_fear": 100,
    "max_sanity": 100,
    "time_per_cycle": 10,
    "fear_night_increase": 10
}

class GameState:
    """Classe principal que gerencia todo o estado do jogo"""
    
    def __init__(self):
        # Configuração básica do jogo
        self.player = Character(
            name="Investigador",
            description="Um destemido explorador paranormal",
            dialog="Preciso descobrir a verdade..."
        )
        
        self.inventory = Inventory(limit=GAME_CONFIG["inventory_limit"])
        
        # O mundo é carregado usando o novo método estático
        self.world = World.load_from_json()
        
        self.quiz_system = QuizSystem()
        self.puzzle_system = PuzzleSystem()
        
        # Estado do jogo
        self.current_room = GAME_CONFIG["start_room"]
        self.health = GAME_CONFIG["max_health"]
        self.fear = 0
        self.sanity = GAME_CONFIG["max_sanity"]
        self.luck = random.randint(1, 100)  # Atributo de sorte
        self.is_night = False
        self.game_time = 0
        
        # Progresso
        self.completed_events = []
        self.ending_flags = {
            "good": False,
            "bad": False
        }

    def get_current_room_data(self) -> Optional[Room]:
        """Retorna a instância da sala atual"""
        if self.world:
            return self.world.get_room(self.current_room)
        return None
        
    def move_to_room(self, direction: str) -> bool:
        """Move o jogador para uma nova sala se a direção for válida"""
        if not self.world:
            return False
            
        current_room_obj = self.get_current_room_data()
        if not current_room_obj:
            return False
            
        next_room_name = current_room_obj.connections.get(direction)
        if next_room_name and self.world.get_room(next_room_name):
            self.current_room = next_room_name
            self.update_game_time()
            return True
        return False
        
    def get_current_room_connections(self) -> List[str]:
        """Retorna uma lista de direções possíveis da sala atual"""
        current_room_obj = self.get_current_room_data()
        if not current_room_obj:
            return []
        return list(current_room_obj.connections.keys())

    def trigger_random_event(self):
        """Gatilho para eventos aleatórios baseados no medo e sorte"""
        if random.randint(1, 100) > (100 - self.fear):
            print(f"{C.FEAR}Você sente uma presença fria por perto...")
            events = [
                {"desc": "Uma sombra se move rapidamente no canto do olho.", "effect": {"fear": 15}},
                {"desc": "Sussurros ininteligíveis ecoam pelas paredes.", "effect": {"fear": 20, "sanity": -5}}
            ]
            event = random.choice(events)
            self.apply_effects(event["effect"])
            return event["desc"]
        return None

    def apply_effects(self, effects: Dict[str, int]):
        """Aplica múltiplos efeitos ao jogador"""
        if "health" in effects:
            self.health = max(0, min(100, self.health + effects["health"]))
        if "fear" in effects:
            self.fear = max(0, min(100, self.fear + effects["fear"]))
        if "sanity" in effects:
            self.sanity = max(0, min(100, self.sanity + effects["sanity"]))

    def update_game_time(self):
        """Avança o tempo do jogo e controla ciclo dia/noite"""
        self.game_time += 1
        
        # A cada 10 ciclos troca entre dia e noite
        if self.game_time % GAME_CONFIG["time_per_cycle"] == 0:
            self.is_night = not self.is_night
            if self.is_night:
                self.fear = min(100, self.fear + GAME_CONFIG["fear_night_increase"])

    def check_ending_conditions(self) -> Optional[str]:
        """Verifica se alguma condição de final foi atingida"""
        if self.health <= 0:
            return "bad"
        if self.sanity <= 0:
            return "bad"
        
        # Condições de final bom (exemplo: ter um item específico)
        # if any(item.name == "artefato_completo" for item in self.inventory.items):
        #    return "good"
            
        return None

    def save_game(self, file_name: str = "save_game.json"):
        """Salva o estado atual do jogo em um arquivo"""
        save_data = {
            "player": self.player.__dict__,
            "inventory": [item.__dict__ for item in self.inventory.items],
            "current_room": self.current_room,
            "health": self.health,
            "fear": self.fear,
            "sanity": self.sanity,
            "luck": self.luck,
            "is_night": self.is_night,
            "game_time": self.game_time,
            "completed_events": self.completed_events,
            "ending_flags": self.ending_flags
        }
        path = Path(__file__).parent.parent / "saves" / file_name
        path.parent.mkdir(parents=True, exist_ok=True) # Garante que o diretório 'saves' exista
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=4)
        return f"Jogo salvo com sucesso em {path}"

    @classmethod
    def load_game(cls, file_name: str = "save_game.json"):
        """Carrega um estado de jogo de um arquivo"""
        path = Path(__file__).parent.parent / "saves" / file_name
        try:
            with open(path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            game = cls() # Cria uma nova instância e sobrescreve o estado
            
            game.player = Character(**save_data["player"])
            game.inventory.items = [Item(**item_data) for item_data in save_data["inventory"]]
            game.current_room = save_data["current_room"]
            game.health = save_data["health"]
            game.fear = save_data["fear"]
            game.sanity = save_data["sanity"]
            game.luck = save_data["luck"]
            game.is_night = save_data["is_night"]
            game.game_time = save_data["game_time"]
            game.completed_events = save_data["completed_events"]
            game.ending_flags = save_data["ending_flags"]
            
            return game
        except FileNotFoundError:
            print(f"Erro: Arquivo de save '{file_name}' não encontrado.")
            return None
        except json.JSONDecodeError:
            print(f"Erro: Arquivo de save '{file_name}' mal formatado.")
            return None
        except KeyError as e:
            print(f"Erro: Arquivo de save '{file_name}' está faltando uma chave: {e}")
            return None

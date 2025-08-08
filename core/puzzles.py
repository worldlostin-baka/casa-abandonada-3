import json
from typing import Dict, Any, List, Optional
from core.utils import load_json_data # Importação da nova função

class PuzzleSystem:
    def __init__(self):
        # Utiliza a função auxiliar centralizada para carregar
        self.puzzles: Dict[str, Dict[str, Any]] = load_json_data("puzzles.json") or {}
    
    def get_puzzle(self, puzzle_id: str) -> Optional[Dict[str, Any]]:
        """Obtém um puzzle pelo ID"""
        return self.puzzles.get(puzzle_id)

    def check_solution(self, puzzle_id: str, player_solution: str) -> bool:
        """Verifica se a solução do jogador está correta"""
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return False
            
        correct_solution = puzzle['solution']
        if isinstance(correct_solution, list):
            return player_solution.lower() in [s.lower() for s in correct_solution]
        return player_solution.lower() == correct_solution.lower()

    def get_puzzle_reward(self, puzzle_id: str) -> Optional[Dict[str, Any]]:
        """Retorna a recompensa do puzzle"""
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return None
        return {
            'item': puzzle.get('reward_item'),
            'effect': puzzle.get('reward_effect'),
            'unlocks': puzzle.get('unlocks')
        }
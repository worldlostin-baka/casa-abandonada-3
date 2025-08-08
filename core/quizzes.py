import json
from typing import Dict, Any, List, Optional
from core.utils import load_json_data # Importação da nova função

class QuizSystem:
    def __init__(self):
        # Utiliza a função auxiliar centralizada para carregar
        self.quizzes: Dict[str, Dict[str, Any]] = load_json_data("quizzes.json") or {}
    
    def get_quiz(self, quiz_id: str) -> Optional[Dict[str, Any]]:
        """Obtém um quiz pelo ID"""
        return self.quizzes.get(quiz_id)

    def validate_answer(self, quiz_id: str, answer_index: int) -> bool:
        """Valida a resposta do jogador"""
        quiz = self.get_quiz(quiz_id)
        if quiz:
            return 0 <= answer_index < len(quiz['options']) and answer_index == quiz['correct']
        return False

    def get_quiz_reward(self, quiz_id: str) -> Optional[Dict[str, Any]]:
        """Retorna a recompensa do quiz"""
        quiz = self.get_quiz(quiz_id)
        return {
            'item': quiz.get('reward_item'),
            'effect': quiz.get('reward_effect')
        } if quiz else None

    def get_quiz_penalty(self, quiz_id: str) -> Optional[Dict[str, Any]]:
        """Retorna a penalidade do quiz"""
        quiz = self.get_quiz(quiz_id)
        return quiz.get('penalty') if quiz else None
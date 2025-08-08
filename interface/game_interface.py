import os
import sys
from core.game_state import GameState
from interface.hud import HUD
from interface.menu import MainMenu
from core.colors import GameColors as C
from core.command_system import CommandSystem
from core.world import Room
from core.items import Item
from typing import Dict, List, Optional

class GameInterface:
    
    def __init__(self):
        self.game = GameState()
        self.hud = HUD()
        self.commands = CommandSystem()
        
        self.running = self.game.world is not None
        if not self.running:
            self.clear_screen()
            print(f"\n{C.DANGER}Erro fatal: O mundo do jogo não pôde ser carregado. O programa será encerrado.{C.RESET}")
            input("\nPressione ENTER para sair...")
            sys.exit()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_status(self):
        self.hud.show_status(self.game)

    def show_room(self, room_data: Room):
        if room_data is None:
            print(f"{C.DANGER}Erro: A sala atual não pôde ser carregada.{C.RESET}")
            return

        print(f"\n{C.LOCATION}{room_data.name}{C.RESET}")
        print(f"{C.DESCRIPTION}{room_data.description}{C.RESET}")
        
        if room_data.puzzle_id:
            print(f"\n{C.WARNING}Você sente a presença de um enigma. Talvez 'examinar' o ambiente o ajude.{C.RESET}")
        
        if room_data.quiz_id:
            print(f"\n{C.WARNING}Uma voz misteriosa ecoa na sala. Você pode tentar 'responder' ao desafio.{C.RESET}")

    def _get_available_actions(self) -> Dict[str, str]:
        actions = {}
        key_index = 0
        current_room = self.game.get_current_room_data()
        
        keys = "abcdefghijklmnopqrstuvwxyz"
        
        actions[keys[key_index]] = 'olhar'
        key_index += 1
        actions[keys[key_index]] = 'inventario'
        key_index += 1
        
        if current_room.connections:
            for direction in current_room.connections:
                actions[keys[key_index]] = f'mover {direction}'
                key_index += 1
        
        if current_room.items:
            for item in current_room.items:
                actions[keys[key_index]] = f'pegar {item}'
                key_index += 1
                
        if self.game.inventory.items:
            for item in self.game.inventory.items:
                actions[keys[key_index]] = f'examinar {item.name}'
                key_index += 1
                
        actions[keys[key_index]] = 'ajuda'
        key_index += 1
        actions[keys[key_index]] = 'sair'
        
        return actions

    def _display_actions(self, actions: Dict[str, str]):
        print(f"\n{C.INFO}Opções disponíveis:{C.RESET}")
        for key, command in actions.items():
            print(f"  ({C.BRIGHT}{key}{C.NORMAL}) {command.title()}")

    def handle_command(self, cmd: str) -> bool:
        parsed = self.commands.parse(cmd)
        
        if not parsed:
            print(f"\n{C.WARNING}Comando inválido. Tente 'ajuda' para ver os comandos disponíveis.{C.RESET}")
            return True
            
        action = parsed.get('action')
        target = parsed.get('target')
        
        if action == 'move':
            if self.game.move_to_room(target):
                print(f"\nVocê se move para o {target}.")
            else:
                print(f"{C.WARNING}Não é possível ir para lá!{C.RESET}")
        
        elif action == 'look':
            print("\nVocê olha ao redor e percebe que as sombras dançam na periferia de sua visão.")
            event_desc = self.game.trigger_random_event()
            if event_desc:
                print(f"{C.WARNING}{event_desc}{C.RESET}")

        elif action == 'examine':
            if not target:
                print(f"{C.WARNING}O que você quer examinar? Por favor, especifique um item ou objeto.{C.RESET}")
            else:
                current_room = self.game.get_current_room_data()
                item_in_inventory = next((item for item in self.game.inventory.items if item.name.lower() == target.lower()), None)
                if item_in_inventory:
                    print(f"\n{C.INFO}Você examina o {item_in_inventory.name}. {item_in_inventory.description}{C.RESET}")
                elif target.lower() in [item.lower() for item in current_room.items]:
                    item_in_room = self.game.get_item_from_room(target)
                    print(f"\n{C.INFO}Você examina o {target}. {item_in_room.description if item_in_room else 'É um item comum.'}{C.RESET}")
                else:
                    print(f"{C.WARNING}Não há {target} para examinar aqui.{C.RESET}")

        elif action == 'take':
            if not target:
                print(f"{C.WARNING}O que você quer pegar? Por favor, especifique um item.{C.RESET}")
            else:
                current_room = self.game.get_current_room_data()
                if target in current_room.items:
                    if self.game.inventory.add_item(Item(name=target, description=f"A {target} que você pegou.")):
                        current_room.items.remove(target)
                        print(f"{C.SUCCESS}Você pegou a {target} e a colocou no seu inventário.{C.RESET}")
                    else:
                        print(f"{C.WARNING}O seu inventário está cheio. Não pode pegar a {target}.{C.RESET}")
                else:
                    print(f"{C.WARNING}Não há {target} aqui para pegar.{C.RESET}")
        
        elif action == 'use':
            if not target:
                print(f"{C.WARNING}O que você quer usar? Por favor, especifique um item.{C.RESET}")
            else:
                item_in_inventory = next((item for item in self.game.inventory.items if item.name.lower() == target.lower()), None)
                if item_in_inventory:
                    print(f"{C.INFO}Você tentou usar o {target}, mas nada aconteceu... ainda.{C.RESET}")
                else:
                    print(f"{C.WARNING}Você não tem {target} no seu inventário.{C.RESET}")

        elif action == 'combine':
            print(f"{C.INFO}A funcionalidade de combinar itens ainda não está disponível.{C.RESET}")

        elif action == 'inventory':
            self.hud.show_inventory([item.name for item in self.game.inventory.items])
            
        elif action == 'quit':
            self.running = False
            return False
        
        elif action == 'help':
            print(f"\n{C.INFO}Comandos disponíveis:{C.RESET}")
            print(f"- {C.BRIGHT}mover [direção]{C.NORMAL} (ex: 'mover norte' para mudar de sala)")
            print(f"- {C.BRIGHT}olhar{C.NORMAL} (para inspecionar a sala)")
            print(f"- {C.BRIGHT}examinar [item]{C.NORMAL} (ex: 'examinar chave')")
            print(f"- {C.BRIGHT}pegar [item]{C.NORMAL} (ex: 'pegar chave' para adicionar ao inventário)")
            print(f"- {C.BRIGHT}usar [item]{C.NORMAL} (para usar um item do inventário)")
            print(f"- {C.BRIGHT}inventario{C.NORMAL} (para ver o que você tem)")
            print(f"- {C.BRIGHT}combinar [item1] com [item2]{C.NORMAL} (placeholder)")
            print(f"- {C.BRIGHT}sair{C.NORMAL} (para fechar o jogo)")
        
        else:
            print(f"{C.WARNING}Comando '{action}' não reconhecido. Tente 'ajuda'.{C.RESET}")
            
        return True

    def game_loop(self):
        self.clear_screen()
        print(C.format("=== CASA ABANDONADA - ECOS DO MEDO ===", C.TITLE))
        
        while self.running:
            self.show_status()
            room = self.game.get_current_room_data()
            self.show_room(room)
            
            available_actions = self._get_available_actions()
            self._display_actions(available_actions)
            
            cmd_key = input(f"\n{C.INFO}Escolha sua ação: {C.RESET}").strip().lower()
            
            if cmd_key in available_actions:
                command_to_execute = available_actions[cmd_key]
                if not self.handle_command(command_to_execute):
                    break
            else:
                print(f"{C.WARNING}Opção inválida. Por favor, escolha uma das teclas listadas.{C.RESET}")

            if self.running and not command_to_execute.startswith('sair'):
                input(f"\n{C.WARNING}Pressione ENTER para continuar...{C.RESET}")

if __name__ == "__main__":
    try:
        game = GameInterface()
        game.game_loop()
    except Exception as e:
        print(f"\n{C.DANGER}Ocorreu um erro fatal durante a execução do jogo: {e}{C.RESET}")
        print("O programa será encerrado. Pressione ENTER para sair.")
        input()

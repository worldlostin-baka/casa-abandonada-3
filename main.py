import os
import sys
from colorama import init, Fore, Back, Style

# Inicializa o colorama para que as cores funcionem no Windows
init(autoreset=True)

class MainGame:
    """Classe principal para iniciar e gerir o fluxo do jogo."""
    
    def __init__(self):
        # A importação aqui garante que GameInterface só é carregado se o programa começar
        try:
            from interface.game_interface import GameInterface
            self.game_interface = GameInterface()
        except ImportError as e:
            print(f"{Fore.RED}Erro: Não foi possível importar os módulos necessários. Verifique se todos os arquivos estão na estrutura correta.")
            print(f"{Fore.RED}Detalhes do erro: {e}")
            sys.exit(1)
        
        self.running = True
    
    def clear_screen(self):
        """Limpa a tela de forma cross-platform."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self):
        """Exibe o menu principal do jogo."""
        self.clear_screen()
        print(f"{Fore.YELLOW}\n{'='*23}")
        print(f"{Fore.GREEN}=== CASA ABANDONADA ===")
        print(f"{Fore.CYAN}{'Um jogo de terror psicológico':^23}\n")
        print(f"{Fore.WHITE}1. Iniciar nova aventura")
        print(f"{Fore.WHITE}2. Carregar jogo salvo")
        print(f"{Fore.WHITE}3. Sair do jogo")
        print(f"{Fore.YELLOW}\n{'='*23}\n")
    
    def handle_menu_choice(self, choice):
        """Processa a escolha do menu do jogador."""
        if choice == '1':
            print(f"{Fore.GREEN}Iniciando uma nova aventura...")
            self.game_interface.game_loop()
        elif choice == '2':
            # Implementação futura: carregar jogo salvo
            print(f"{Fore.YELLOW}Funcionalidade de carregar jogo ainda não implementada.")
            input("Pressione ENTER para voltar ao menu...")
        elif choice == '3':
            print(f"{Fore.RED}Saindo do jogo. Até a próxima!")
            self.running = False
        else:
            print(f"{Fore.RED}Opção inválida. Tente novamente.")
            input("Pressione ENTER para continuar...")

    def run(self):
        """Loop principal do menu do jogo."""
        while self.running:
            self.show_main_menu()
            choice = input("Escolha uma opção: ").strip()
            self.handle_menu_choice(choice)
            
if __name__ == "__main__":
    try:
        game = MainGame()
        game.run()
    except Exception as e:
        print(f"{Fore.RED}\nOcorreu um erro fatal durante a execução do jogo: {e}")
        input("O programa será encerrado. Pressione ENTER para sair.")

from core.colors import GameColors as C
import time
import os

class MainMenu:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show():
        MainMenu.clear_screen()
        print(C.format("\n" + "="*50, C.DARK_AREA))
        print(C.format(f"{'CASA ABANDONADA':^50}", C.BLOOD))
        print(C.format("="*50, C.DARK_AREA))
        print("")
        print(C.format("         1. »» Novo Jogo ««          ", C.TITLE))
        print(C.format("         2. »» Carregar Jogo ««     ", C.LOCATION))
        print(C.format("         3. »» Configurações ««     ", C.ITEM))
        print(C.format("         4. »» Créditos ««         ", C.INFO))
        print(C.format("         5. ━━━ Sair ━━━           ", C.DANGER))
        print("")
        print(C.format("="*50, C.DARK_AREA))

    @staticmethod
    def show_credits():
        MainMenu.clear_screen()
        credits = [
            "",
            "="*50,
            f"{'CRÉDITOS':^50}",
            "="*50,
            "",
            f"{'Desenvolvido por:':^50}",
            f"{'Philipe Enggist':^50}",
            "",
            f"{'Efeitos Sonoros:':^50}",
            f"{'Freesound.org':^50}",
            "",
            f"{'Música:':^50}",
            f"{'Pixabay':^50}",
            "",
            "="*50,
            ""
        ]
        
        for line in credits:
            if "Philipe" in line:
                print(C.format(line, C.BLOOD))
            elif line.strip() and not "=" in line:
                print(C.format(line, C.WARNING))
            else:
                print(C.format(line, C.DARK_AREA))
        
        input(C.format("\nPressione ENTER para voltar...", C.WARNING))

    @staticmethod
    def typewriter(text, color=C.NORMAL, delay=0.03):
        for char in text:
            print(C.format(char, color), end='', flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def show_intro():
        MainMenu.clear_screen()
        print("\n")
        MainMenu.typewriter("A casa aguarda...", C.DANGER)
        time.sleep(1)
        MainMenu.typewriter("Os corredores sussurram segredos...", C.DARK_AREA)
        time.sleep(1)
        MainMenu.typewriter("Você está preparado para a verdade?", C.BLOOD)
        time.sleep(2)
        input(C.format("\nPressione ENTER para entrar...", C.WARNING))
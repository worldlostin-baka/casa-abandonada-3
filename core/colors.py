from colorama import Fore, Back, Style, init

init(autoreset=True)

class GameColors:
    """Configurações de cores para o jogo"""
    
    # Cores principais
    TITLE = Fore.LIGHTBLUE_EX + Style.BRIGHT
    INFO = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    DANGER = Fore.RED + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    
    # Elementos do jogo
    ITEM = Fore.LIGHTCYAN_EX + Style.BRIGHT
    LOCATION = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
    DESCRIPTION = Fore.LIGHTWHITE_EX
    
    # Status do jogador
    HEALTH = Fore.LIGHTRED_EX + Style.BRIGHT
    FEAR = Fore.MAGENTA + Style.BRIGHT
    LUCK = Fore.LIGHTYELLOW_EX + Style.BRIGHT
    
    # Efeitos especiais
    BLOOD = Fore.RED + Back.LIGHTYELLOW_EX + Style.BRIGHT
    DARK_AREA = Fore.LIGHTWHITE_EX + Back.BLACK + Style.BRIGHT
    FIRE = Fore.YELLOW + Back.RED + Style.BRIGHT
    
    # Estilos de texto
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM          # Adicionando o estilo DIM
    NORMAL = Style.NORMAL
    
    # Adicionando o atributo RESET
    RESET = Style.RESET_ALL  # Reseta todos os estilos

    @staticmethod
    def format(text, *styles):
        """Formata texto com múltiplos estilos"""
        return ''.join(styles) + text + Style.RESET_ALL

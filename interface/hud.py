from core.colors import GameColors as C

class HUD:
    """Interface do usuário (Head-Up Display)"""
    
    @staticmethod
    def show_status(game_state):
        print(f"""{C.HEALTH}❤ Saúde: {game_state.health}  
{C.FEAR}😨 Medo: {game_state.fear}  
{C.LUCK}🍀 Sorte: {game_state.luck}""")
    
    @staticmethod
    def show_inventory(items):
        if items:
            print(f"\n{C.ITEM}Seu inventário:")
            for item in items:
                print(f" - {item}")
        else:
            print("\nSeu inventário está vazio.")
            
    @staticmethod
    def show_alert(message, alert_type="info"):
        colors = {
            "danger": C.DANGER,
            "warning": C.WARNING,
            "info": C.INFO
        }
        print(f"\n{colors.get(alert_type, C.INFO)}⚠ {message} ⚠")

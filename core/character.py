from dataclasses import dataclass

@dataclass
class Character:
    name: str
    description: str
    dialog: str
    quirks: str = ""

from typing import List, Optional, Dict, Any

class Item:
    def __init__(self, name: str, description: str, effects: Optional[Dict[str, Any]] = None, use_message: Optional[str] = None):
        self.name = name
        self.description = description
        self.effects = effects if effects is not None else {}
        self.use_message = use_message

    def use(self):
        if self.use_message:
            return self.use_message
        return f"Você não pode usar o item {self.name} aqui."

class Inventory:
    def __init__(self, limit: int = 5):
        self.items: List[Item] = []
        self.limit = limit
    
    def add_item(self, item: Item) -> bool:
        if len(self.items) < self.limit:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item_name: str) -> Optional[Item]:
        item_to_remove = next((item for item in self.items if item.name.lower() == item_name.lower()), None)
        if item_to_remove:
            self.items.remove(item_to_remove)
            return item_to_remove
        return None
    
    def has_item(self, item_name: str) -> bool:
        return any(item.name.lower() == item_name.lower() for item in self.items)

    def get_item(self, item_name: str) -> Optional[Item]:
        return next((item for item in self.items if item.name.lower() == item_name.lower()), None)

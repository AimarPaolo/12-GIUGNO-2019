from dataclasses import dataclass

@dataclass
class Condiment:
    condiment_code: int
    display_name: str
    condiment_calories: float

    def __hash__(self):
        return hash(self.condiment_code)
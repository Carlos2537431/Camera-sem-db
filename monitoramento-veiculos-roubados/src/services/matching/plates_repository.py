from typing import List, Optional

class PlatesRepository:
    def __init__(self):
        self.plates = []

    def add_plate(self, plate: str) -> None:
        if plate not in self.plates:
            self.plates.append(plate)

    def remove_plate(self, plate: str) -> None:
        if plate in self.plates:
            self.plates.remove(plate)

    def get_all_plates(self) -> List[str]:
        return self.plates

    def find_plate(self, plate: str) -> Optional[str]:
        if plate in self.plates:
            return plate
        return None

    def clear_plates(self) -> None:
        self.plates.clear()
"""Машинист — тестовая обёртка, которая управляет кротом на языке предметной области."""


class Driver:
    def __init__(self, mole):
        self.mole = mole

    def drive(self, distance_km):
        """Ехать по поверхности."""
        return self.mole.move(distance_km, "surface")

    def dig(self, distance_km):
        """Копать в грунте."""
        return self.mole.move(distance_km, "soil")

    def drill_rock(self, distance_km):
        """Бурить скалу."""
        return self.mole.move(distance_km, "rock")

    def swim(self, distance_km):
        """Попытка заехать в воду."""
        return self.mole.move(distance_km, "water")

    def check(self, obstacle):
        return self.mole.can_overcome(obstacle)

    def plan(self, distance_km, terrain):
        return self.mole.calculate_fuel(distance_km, terrain)

    def refuel(self, amount):
        return self.mole.refuel(amount)

    def change_drill(self):
        return self.mole.replace_drill()

    def status(self):
        return self.mole.get_status()

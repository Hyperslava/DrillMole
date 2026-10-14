"""Сценарные тесты DrillMole (Given-When-Then) через машиниста Driver."""

import unittest

from drill_mole import (
    DrillMole,
    DrillMoleCannotSwim,
    DrillMoleDrillWorn,
    DrillMoleNoFuel,
    DrillMoleNotOnSurface,
)
from tests.driver import Driver


def state(mole):
    return (mole.position_km, mole.fuel, mole.drill_wear, mole.is_underground)


class TestScenarios(unittest.TestCase):
    def test_tc23_dig_under_fortress(self):
        """TC-23: Подкоп под крепость."""
        # Given
        mole = DrillMole("Копатель", drill_diameter_m=1.2, max_speed_kmh=20, fuel=100)
        driver = Driver(mole)
        # When: едет к реке по поверхности
        hours = driver.drive(2)
        # Then
        self.assertAlmostEqual(hours, 0.1)
        self.assertEqual(state(mole), (2, 98, 0, False))
        self.assertIs(driver.check("river"), False)
        # When: зарывается в грунт
        hours = driver.dig(4)
        # Then
        self.assertAlmostEqual(hours, 0.4)
        self.assertEqual(state(mole), (6, 90, 4, True))
        self.assertIs(driver.check("river"), True)
        # When: проходит под рекой
        driver.dig(3)
        # Then
        self.assertEqual(state(mole), (9, 84, 7, True))
        self.assertIs(driver.check("wall"), True)
        # When: выезжает внутри крепости
        driver.drive(2)
        # Then
        self.assertEqual(state(mole), (11, 82, 7, False))

    def test_tc24_rock_and_worn_drill(self):
        """TC-24: Скальный пласт и сломанный бур."""
        # Given
        mole = DrillMole("Копатель", drill_diameter_m=1.2, max_speed_kmh=20, fuel=100)
        driver = Driver(mole)
        # When
        hours = driver.drill_rock(10)
        # Then
        self.assertAlmostEqual(hours, 2.0)
        self.assertEqual(state(mole), (10, 70, 50, True))
        # When
        driver.drill_rock(10)
        # Then
        self.assertEqual(state(mole), (20, 40, 100, True))
        self.assertIs(driver.check("wall"), False)
        # When: пытается копать дальше
        with self.assertRaises(DrillMoleDrillWorn):
            driver.dig(1)
        # Then
        self.assertEqual(state(mole), (20, 40, 100, True))
        # When: пытается сменить бур под землёй
        with self.assertRaises(DrillMoleNotOnSurface):
            driver.change_drill()
        # When: выезжает и меняет бур
        driver.drive(1)
        driver.change_drill()
        # Then
        self.assertEqual(state(mole), (21, 39, 0, False))
        # When
        driver.dig(2)
        # Then
        self.assertEqual(state(mole), (23, 35, 2, True))

    def test_tc25_river_and_empty_tank(self):
        """TC-25: Река и пустой бак."""
        # Given
        mole = DrillMole("Копатель", drill_diameter_m=0.8, max_speed_kmh=20, fuel=10)
        driver = Driver(mole)
        # When
        driver.drive(5)
        # Then
        self.assertEqual(state(mole), (5, 5, 0, False))
        self.assertIs(driver.check("boulder"), False)
        # When: пробует переплыть реку
        with self.assertRaises(DrillMoleCannotSwim):
            driver.swim(1)
        # Then
        self.assertEqual(state(mole), (5, 5, 0, False))
        # When: пробует пройти под рекой без топлива
        with self.assertRaises(DrillMoleNoFuel):
            driver.dig(3)
        # Then
        self.assertEqual(mole.fuel, 5)
        # When: заправляется
        driver.refuel(200)
        # Then
        self.assertEqual(mole.fuel, 100)
        self.assertEqual(driver.plan(3, "soil"), 6)
        self.assertEqual(state(mole), (5, 100, 0, False))
        # When
        driver.dig(3)
        # Then
        self.assertEqual(state(mole), (8, 94, 3, True))

    def test_tc26_planned_route(self):
        """TC-26: Маршрут по плану."""
        # Given
        mole = DrillMole("Копатель", drill_diameter_m=1.0, max_speed_kmh=20, fuel=50)
        driver = Driver(mole)
        # When: считает расход
        plan = [driver.plan(5, "surface"), driver.plan(5, "soil"), driver.plan(5, "rock")]
        # Then
        self.assertEqual(plan, [5, 10, 15])
        self.assertEqual(mole.fuel, 50)
        # When: проходит маршрут
        driver.drive(5)
        driver.dig(5)
        driver.drill_rock(5)
        # Then
        self.assertEqual(state(mole), (15, 20, 30, True))
        self.assertIs(driver.check("boulder"), True)
        self.assertEqual(driver.status(), {"name": "Копатель", "fuel": 20.0, "drill_wear": 30.0,
                                           "position_km": 15.0, "is_underground": True})


if __name__ == "__main__":
    unittest.main()

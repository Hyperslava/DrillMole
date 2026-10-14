# Test Case Specification: Крот-бур «Копатель»

Базовый крот (если не сказано иное): `DrillMole("Копатель", drill_diameter_m=1.2, max_speed_kmh=20, fuel=100)`.

Соотношение: 22 модульных / 4 сценарных (~85 / 15).

## Модульные тесты

| ID | Тип | Источник | Предусловие | Вход | Ожидание | Приоритет |
|---|---|---|---|---|---|---|
| TC-01 | module | SPEC 3.2 | — | name=""; drill_diameter_m=0 / -1; max_speed_kmh=0 | ValueError | high |
| TC-02 | module | SPEC 3.2 | — | fuel=-1 / 101; fuel=0 / 100; fuel не передан | -1 и 101 → ValueError; 0 и 100 принимаются; без fuel → fuel == 100.0 | high |
| TC-03 | module | SPEC 3.2, 6.2 | — | name=5; drill_diameter_m="1"; max_speed_kmh=None; fuel=True | TypeError | medium |
| TC-04 | module | SPEC 3.4.1 | — | move(10, "surface") | 0.5; position_km=10, fuel=90, drill_wear=0, is_underground=False | high |
| TC-05 | module | SPEC 3.4.1, 4.1 сц. 1 | — | move(10, "soil") | 1.0; position_km=10, fuel=80, drill_wear=10, is_underground=True | high |
| TC-06 | module | SPEC 3.4.1 | — | move(4, "rock") | 0.8; position_km=4, fuel=88, drill_wear=20, is_underground=True | high |
| TC-07 | module | SPEC 3.4.1, 6.2 | — | move(1, "water") | DrillMoleCannotSwim; состояние не меняется | high |
| TC-08 | module | SPEC 3.4.1, 4.1 сц. 2 | fuel=10 | move(4, "rock") | DrillMoleNoFuel; состояние не меняется | high |
| TC-09 | module | SPEC 3.4.1, 5 | fuel=12 | move(4, "rock") | успешно; fuel=0, drill_wear=20 | high |
| TC-10 | module | SPEC 3.4.1, 5 | move(10, "rock") ×2 | move(1, "soil"); затем move(1, "surface") | после подготовки drill_wear=100; soil → DrillMoleDrillWorn, состояние не меняется; surface успешно | high |
| TC-11 | module | SPEC 3.4.1, 6.2 | — | move(0, "soil"); move(-1, "soil"); move(1, "lava"); move("1", "soil"); move(1, 5) | ValueError, ValueError, ValueError, TypeError, TypeError; состояние не меняется | medium |
| TC-12 | module | SPEC 3.5 | fuel=0 / fuel=60 + move(10, "rock") ×2 | move(1, "water"); move(0, "water"); move(1, "soil") | CannotSwim (а не NoFuel); ValueError (а не CannotSwim); DrillWorn (а не NoFuel) | medium |
| TC-13 | module | SPEC 3.5, 5 | fuel=0.3 | move(0.1, "surface") ×3 | все три успешны; fuel == 0.0, position_km == 0.3 | medium |
| TC-14 | module | SPEC 3.4.2, 4.1 сц. 3 | новый / move(1, "soil") / move(1, "soil") + move(1, "surface") | can_overcome("river") | False / True / False | high |
| TC-15 | module | SPEC 3.4.2 | новый / move(10, "rock") ×2 | can_overcome("wall") | True / False | high |
| TC-16 | module | SPEC 3.4.2, 5 | drill_diameter_m=1.0 / 0.99 | can_overcome("boulder") | True / False | high |
| TC-17 | module | SPEC 3.4.2 | — | can_overcome("tree"); can_overcome(1) | ValueError; TypeError | medium |
| TC-18 | module | SPEC 3.4.3 | fuel=100 и fuel=0 | calculate_fuel(5, "surface" / "soil" / "rock"); calculate_fuel(1, "water") | 5.0 / 10.0 / 15.0 при любом fuel; вода → DrillMoleCannotSwim; состояние не меняется | high |
| TC-19 | module | SPEC 3.4.4, 5 | fuel=20 / fuel=50 | refuel(50); refuel(1000); refuel(0); refuel(-1) | None, fuel=70; fuel=100; ValueError; ValueError | high |
| TC-20 | module | SPEC 3.4.5, 4.1 сц. 4 | move(10, "rock") | replace_drill() под землёй; затем move(1, "surface") и replace_drill() | DrillMoleNotOnSurface, drill_wear=50; на поверхности drill_wear=0, fuel=69 | high |
| TC-21 | module | SPEC 3.4.6 | — | get_status() | {"name": "Копатель", "fuel": 100.0, "drill_wear": 0.0, "position_km": 0.0, "is_underground": False} | medium |
| TC-22 | module | SPEC 6.1 | — | проверка наследования | все 4 доменных исключения — подклассы DrillMoleError, DrillMoleError — CrazyVehicleError | medium |

## Сценарные тесты

| ID | Тип | Источник | Вход | Ожидание | Приоритет |
|---|---|---|---|---|---|
| TC-23 | scenario | SPEC 4.2 «Подкоп под крепость» | все шаги сценария | position_km=11, fuel=82, drill_wear=7, is_underground=False | high |
| TC-24 | scenario | SPEC 4.2 «Скальный пласт и сломанный бур» | все шаги сценария | position_km=23, fuel=35, drill_wear=2, is_underground=True | high |
| TC-25 | scenario | SPEC 4.2 «Река и пустой бак» | все шаги сценария | position_km=8, fuel=94, drill_wear=3, is_underground=True | high |
| TC-26 | scenario | SPEC 4.2 «Маршрут по плану» | все шаги сценария | get_status() == {"name": "Копатель", "fuel": 20.0, "drill_wear": 30.0, "position_km": 15.0, "is_underground": True} | medium |

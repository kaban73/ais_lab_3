import time
import random
from neo4j_manager import Neo4jManager
from fuzzy_logic import InferenceEngine


class StreetLightSimulator:
    def __init__(self):
        self.neo4j_manager = Neo4jManager()
        self.engine = InferenceEngine(self.neo4j_manager)
        self.time = 18  # начальное время
        self.weather_states = ["clear", "cloudy", "rainy"]
        self.current_weather = "clear"

    def simulate_hour(self):
        """Симуляция одного часа"""
        self.time = (self.time + 1) % 24

        # Изменяем погоду (случайно)
        if random.random() < 0.2:  # 20% chance to change weather
            self.current_weather = random.choice(self.weather_states)

        # Рассчитываем освещенность на основе времени
        if 6 <= self.time <= 18:  # день
            base_light = 0.7 + random.uniform(-0.2, 0.2)
        else:  # ночь
            base_light = 0.2 + random.uniform(-0.1, 0.1)

        # Корректируем освещенность в зависимости от погоды
        if self.current_weather == "rainy":
            light_level = max(0.1, base_light - 0.3)
        elif self.current_weather == "cloudy":
            light_level = max(0.1, base_light - 0.2)
        else:
            light_level = base_light

        light_level = min(1.0, max(0.0, light_level))

        # Обрабатываем данные
        activated_rules = self.engine.process_sensors(
            time=self.time,
            light=light_level,
            weather=self.current_weather
        )

        # Применяем действия
        if activated_rules:
            # Берем правило с наивысшим приоритетом
            main_rule = min(activated_rules, key=lambda x: x['priority'])
            print(f"🚦 Применяем действие: {main_rule['action_name']} (из правила: {main_rule['rule_name']})")
        else:
            print("🚦 Действие: сохранять текущее состояние")

        print("-" * 50)

    def run_simulation(self, hours=24):
        """Запуск симуляции на указанное количество часов"""
        print("🚀 ЗАПУСК СИМУЛЯТОРА УЛИЧНОГО ОСВЕЩЕНИЯ")
        print("=" * 50)

        for hour in range(hours):
            print(f"🕐 Час {hour + 1}/24 | Время: {self.time}:00")
            self.simulate_hour()
            time.sleep(1)  # Пауза для наглядности

        self.neo4j_manager.close()


# Запуск симуляции
if __name__ == "__main__":
    simulator = StreetLightSimulator()
    simulator.run_simulation(hours=6)  # Тестируем 6 часов для начала
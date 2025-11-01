import numpy as np
from config import LIGHT_RANGES, TIME_RANGES, WEATHER_CATEGORIES


class FuzzyLogic:
    @staticmethod
    def triangular_mf(x, a, b, c):
        """Треугольная функция принадлежности"""
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x < c:
            return (c - x) / (c - b)
        return 0.0

    @staticmethod
    def fuzzify_light(light_value):
        """Фаззификация уровня освещенности"""
        return {
            'dark': FuzzyLogic.triangular_mf(light_value, *LIGHT_RANGES['dark']),
            'twilight': FuzzyLogic.triangular_mf(light_value, *LIGHT_RANGES['twilight']),
            'light': FuzzyLogic.triangular_mf(light_value, *LIGHT_RANGES['light'])
        }

    @staticmethod
    def fuzzify_time(time_value):
        """Фаззификация времени суток"""
        return {
            'night': FuzzyLogic.triangular_mf(time_value, *TIME_RANGES['night']),
            'morning': FuzzyLogic.triangular_mf(time_value, *TIME_RANGES['morning']),
            'day': FuzzyLogic.triangular_mf(time_value, *TIME_RANGES['day']),
            'evening': FuzzyLogic.triangular_mf(time_value, *TIME_RANGES['evening'])
        }

    @staticmethod
    def fuzzify_weather(weather_value):
        """Фаззификация погоды (четкие категории)"""
        result = {category: 0.0 for category in WEATHER_CATEGORIES}
        if weather_value in WEATHER_CATEGORIES:
            result[weather_value] = 1.0
        return result

    @staticmethod
    def evaluate_condition(condition, fuzzy_values):
        """Оценка условия правила с нечеткой логикой"""
        try:
            # Берем реальные значения
            time_val = fuzzy_values['time']
            light_val = fuzzy_values['light']
            weather_val = fuzzy_values['weather']

            # Преобразуем SQL-подобный синтаксис в Python
            condition = condition.replace('BETWEEN', '>=')
            condition = condition.replace('AND', 'and')
            condition = condition.replace('OR', 'or')

            # Обрабатываем сравнение строк для погоды
            condition = condition.replace('weather = "', 'weather_val == "')
            condition = condition.replace("weather = '", "weather_val == '")

            # Создаем безопасное пространство для eval
            safe_dict = {
                'time': time_val,
                'light': light_val,
                'weather_val': weather_val
            }

            # Вычисляем условие
            result = eval(condition, {"__builtins__": {}}, safe_dict)
            return bool(result)

        except Exception as e:
            print(f"❌ Ошибка в условии '{condition}': {e}")
            return False


class InferenceEngine:
    def __init__(self, neo4j_manager):
        self.neo4j_manager = neo4j_manager
        self.fuzzy_logic = FuzzyLogic()

    def process_sensors(self, time, light, weather):
        """Обработка данных сенсоров и принятие решений"""
        print(f"\n📊 Данные сенсоров: время={time}, освещенность={light}, погода={weather}")

        # Фаззификация
        fuzzy_light = self.fuzzy_logic.fuzzify_light(light)
        fuzzy_time = self.fuzzy_logic.fuzzify_time(time)
        fuzzy_weather = self.fuzzy_logic.fuzzify_weather(weather)

        print(f"🔹 Нечеткая освещенность: {fuzzy_light}")
        print(f"🔹 Нечеткое время: {fuzzy_time}")
        print(f"🔹 Нечеткая погода: {fuzzy_weather}")

        # Получаем правила из базы
        rules = self.neo4j_manager.get_all_rules()

        # Проверяем условия правил
        activated_rules = []
        sensor_values = {'time': time, 'light': light, 'weather': weather}

        for rule in rules:
            if self.fuzzy_logic.evaluate_condition(rule['condition'], sensor_values):
                activated_rules.append(rule)
                print(f"✅ Сработало правило: {rule['rule_name']}")

        return activated_rules


# Тестируем нечеткую логику
if __name__ == "__main__":
    from neo4j_manager import Neo4jManager

    manager = Neo4jManager()
    engine = InferenceEngine(manager)

    # Тестовые сценарии
    print("🧪 Тест 1: Ночь, темно, ясно")
    engine.process_sensors(time=22, light=0.1, weather="clear")

    print("\n🧪 Тест 2: Утро, облачно")
    engine.process_sensors(time=7.5, light=0.4, weather="cloudy")

    print("\n🧪 Тест 3: День, светло")
    engine.process_sensors(time=14, light=0.8, weather="clear")

    manager.close()
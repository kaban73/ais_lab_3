# Настройки подключения к Neo4j
NEO4J_URI = "bolt://54.237.144.252"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "accomplishments-amperes-bypasses"
NEO4J_DATABASE = "neo4j"

# Настройки нечеткой логики
LIGHT_RANGES = {
    'dark': [0, 0, 0.3],
    'twilight': [0.2, 0.4, 0.6],
    'light': [0.5, 1, 1]
}

TIME_RANGES = {
    'night': [0, 0, 6],
    'morning': [5, 7, 9],
    'day': [8, 13, 18],
    'evening': [17, 20, 24]
}

WEATHER_CATEGORIES = ["clear", "cloudy", "rainy"]

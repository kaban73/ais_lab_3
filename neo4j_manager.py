from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE


class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def get_all_rules(self):
        """Получить все правила из базы"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Rule)-[:TRIGGERS]->(a:ActionType)
                RETURN r.name as rule_name, 
                       r.description as description,
                       r.condition as condition, 
                       r.priority as priority,
                       a.name as action_name,
                       a.intensity as intensity
                ORDER BY r.priority
            """)
            return [dict(record) for record in result]

    def test_connection(self):
        """Проверка подключения к Neo4j"""
        try:
            rules = self.get_all_rules()
            print("✅ Подключение к Neo4j Aura успешно!")
            print(f"📋 Найдено правил: {len(rules)}")
            for rule in rules:
                print(f"  🎯 {rule['rule_name']}: {rule['condition']} → {rule['action_name']}")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False


# Тестируем подключение
if __name__ == "__main__":
    manager = Neo4jManager()

    if manager.test_connection():
        print("\n🎉 Система готова к работе!")
        print("Можем переходить к нечеткой логике!")

    manager.close()


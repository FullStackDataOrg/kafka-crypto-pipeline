import json
import psycopg2
from kafka import KafkaConsumer

# Kafka settings
KAFKA_TOPIC = "binance_trades"
KAFKA_BROKER = "localhost:9092"

# PostgreSQL settings
conn = psycopg2.connect(
    dbname="binance_stream",
    user="postgres",
    password="******",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest"
)

for message in consumer:
    data = message.value
    cursor.execute("""
        INSERT INTO trades (trade_id, event_time, symbol, price, quantity, is_buyer_maker, event_type)
        VALUES (%s, to_timestamp(%s / 1000.0), %s, %s, %s, %s, %s)
        ON CONFLICT (trade_id) DO NOTHING
    """, (
        data["t"], data["E"], data["s"], data["p"], data["q"], data["m"], data["e"]
    ))
    conn.commit()
    print(f"Inserted trade {data['t']} into DB")

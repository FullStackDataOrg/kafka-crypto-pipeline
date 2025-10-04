import json
import websocket
from kafka import KafkaProducer

KAFKA_TOPIC = "binance_trades"
KAFKA_BROKER = "localhost:9092"
BINANCE_STREAM = "wss://stream.binance.com:9443/ws/btcusdt@trade"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def on_message(ws, message):
    data = json.loads(message)
    producer.send(KAFKA_TOPIC, value=data)
    print(f"Sent trade ID {data['t']} to Kafka")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket closed")

ws = websocket.WebSocketApp(BINANCE_STREAM, on_message=on_message, on_error=on_error, on_close=on_close)
ws.run_forever()

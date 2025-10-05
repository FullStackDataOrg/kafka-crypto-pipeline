# 🪙 Real-Time Cryptocurrency Streaming Pipeline (Kafka + Binance + PostgreSQL)

This project demonstrates a real-time data streaming pipeline using:
Binance WebSocket API for live cryptocurrency price data
Apache Kafka (KRaft mode) for distributed event streaming
PostgreSQL for structured data storage
Python producers and consumers for data ingestion and persistence
The project continuously listens to Binance trade streams, sends the data into Kafka topics, and then consumes and stores it into a PostgreSQL database for further analytics or visualization.

## 🚀 Architecture Overview
```
          Binance WebSocket Stream
                    ↓
             [Python Producer]
                    ↓
         ┌────────────────────────┐
         │     Apache Kafka       │
         │   (running in KRaft)   │
         └────────────────────────┘
                    ↓
             [Python Consumer]
                    ↓
             PostgreSQL Database
```

## 🧩 Project Structure
```
kafkaproject/
│
├── binance_producer.py      # Connects to Binance WebSocket & pushes data to Kafka
├── binance_consumer.py      # Consumes data from Kafka & stores into PostgreSQL
├── requirements.txt          # Python dependencies
├── kafkaenv/                 # Virtual environment
├── kafka_2.13-3.8.0/         # Kafka installation (KRaft mode)
└── README.md
```
## ⚙️ Prerequisites

Make sure the following are installed on your WSL Ubuntu:
```
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-17-jdk python3 python3-venv python3-pip postgresql -y
```

### 🧱 Step 1: Setup Project & Virtual Environment
```
mkdir kafkaproject && cd kafkaproject
python3 -m venv kafkaenv
source kafkaenv/bin/activate
```


Install required Python libraries:

```
pip install kafka-python websocket-client psycopg2-binary requests
```

Save dependencies:
```
pip freeze > requirements.txt
```

### 🦈 Step 2: Install & Configure Apache Kafka (KRaft Mode)

Download and extract Kafka (version 3.8.0):
```
wget https://archive.apache.org/dist/kafka/3.8.0/kafka_2.13-3.8.0.tgz
tar -xzf kafka_2.13-3.8.0.tgz
cd kafka_2.13-3.8.0
```

Format and start the KRaft server:

# Format storage

```
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```

## Start Kafka
```
bin/kafka-server-start.sh config/kraft/server.properties
```
### 🪣 Step 3: Create Kafka Topic

Open a new terminal, activate your env, and run:
```
cd ~/kafkaproject/kafka_2.13-3.8.0
bin/kafka-topics.sh --create \
  --topic binance_stream \
  --partitions 1 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```
### 💹 Step 4: Binance WebSocket Producer

run binance_producer.py

### 🧠 Step 5: PostgreSQL Setup

Start PostgreSQL and enter the shell:
CREATE DATABASE binance_db;

### 🗃️ Step 6: Kafka Consumer (PostgreSQL Sink)

run binance_consumer.py

### ✅ Step 7: Verify the Data

In PostgreSQL:
```
sudo -u postgres psql -d binance_db
SELECT * FROM trades LIMIT 10;
```
### 🧰 Troubleshooting
Issue	Fix
KafkaProducer import error,	Ensure pip install kafka-python inside your virtual env
WebSocket AttributeError,	Install correct package: pip uninstall websocket && pip install websocket-client
PostgreSQL auth failed,	Check username/password and ensure PostgreSQL is running
Kafka broker not found,	Make sure bin/kafka-server-start.sh is running in a terminal


# 🧠 Key Concepts

How to connect to a live WebSocket API (Binance)
How to stream and buffer messages in Apache Kafka
How to persist data into PostgreSQL
How to run a KRaft-mode Kafka cluster locally
How to build an end-to-end real-time data pipeline


💡 Next Steps
Add Grafana or Power BI for real-time visualization
Containerize the setup using Docker Compose
Extend to multiple Binance streams (e.g., ETHUSDT, BNBUSDT)

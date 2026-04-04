# Teardown — Kafka Crypto Stream

A real-time data streaming pipeline that ingests live cryptocurrency trade data from the Binance WebSocket API, publishes it to Apache Kafka running in KRaft mode, and persists it to PostgreSQL for analytics or visualisation.

---

## Stack Choices & Rationale

| Component | Decision Rationale |
|---|---|
| **Apache Kafka (KRaft mode)** | The industry-standard distributed event streaming platform. KRaft mode (Kafka without ZooKeeper) is the modern deployment model as of Kafka 3.3 — production-ready and operationally simpler. |
| **Binance WebSocket API** | Provides a continuous, low-latency stream of real-world trade events. WebSocket is the correct protocol for push-based real-time data vs polling REST endpoints. |
| **kafka-python** | Pure Python Kafka client. Sufficient for a single-producer, single-consumer pipeline at this scale. No JVM dependency required on the producer/consumer side. |
| **psycopg2 + PostgreSQL** | Direct PostgreSQL insertion from the consumer. PostgreSQL handles structured trade data well and is queryable by standard analytics tools. |
| **Python virtual environment** | Isolates dependencies, prevents conflicts with system Python packages, and is standard practice for Python projects. |

---

## Key Design Decisions

- **KRaft mode, not ZooKeeper.** ZooKeeper is deprecated in Kafka 3.x and removed in Kafka 4.0 — using KRaft is the correct modern approach, not the tutorial default.
- **Single partition** for simplicity. Scaling to multiple symbols or higher TPS would require multiple partitions and a deliberate partition key strategy (e.g. symbol as key).
- **PostgreSQL as the terminal sink** — appropriate for a portfolio demonstration. A production system at scale would write to a columnar store (ClickHouse, BigQuery) for analytical queries.
- **Separate producer and consumer processes** correctly model the decoupled architecture that Kafka is designed to enable — they could run on different machines without code changes.

---

## Trade-offs

| Decision | Benefit | Cost |
|---|---|---|
| `kafka-python` over Confluent Kafka client | Simpler installation, no C library dependencies | Confluent client has better performance, librdkafka-backed, preferred in production |
| PostgreSQL as terminal sink | Simple, queryable, supports SQL analytics | Row-oriented; for time-series analytics, TimescaleDB or ClickHouse would be more efficient |
| Single Kafka topic | Simple to reason about and monitor | Cannot fan-out to multiple consumers with different interests without topic replication |
| KRaft (no ZooKeeper) | Simpler ops, modern architecture | Fewer community examples compared to ZooKeeper-based setups; some tooling not yet fully KRaft-aware |

---

## Extensions & Real-World Use Cases

- Add **Avro schema enforcement** via Confluent Schema Registry — the natural next step and exactly the pattern used in Phase 1 of the Fraud Detection Platform.
- Replace PostgreSQL with **ClickHouse** for the consumer sink. ClickHouse handles time-series append-only trade data at much higher ingestion rates with better compression.
- **Containerise with Docker Compose** to eliminate the manual Kafka installation step and make the project reproducible on any machine.
- Extend to **multiple trading pairs** (ETHUSDT, BNBUSDT) by adding partitions and using the symbol as a partition key, enabling parallel consumption per symbol.
- Add a **Grafana + Prometheus** stack to visualise trade volume, price spread, and consumer lag in real time — a natural bridge to Phase 5 of the Fraud Detection Platform.

---

## Portfolio Signal

Using KRaft mode (not ZooKeeper) signals awareness of the current state of Kafka architecture. Most tutorials still default to ZooKeeper — choosing KRaft demonstrates that the implementation follows the technology's direction, not legacy documentation.

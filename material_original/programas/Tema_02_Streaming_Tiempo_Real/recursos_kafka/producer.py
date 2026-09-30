"""
Sports telemetry producer for soccer matches.

Reads sensor data from a CSV file and publishes each row as an
event to an Apache Kafka topic, simulating a real-time data stream.
"""

from kafka import KafkaProducer
import pandas as pd
import json
import time
import uuid
from datetime import datetime


def random_delay(index: int, base_delay: float) -> float:
    """Simulate occasional sensor delays.

    Deterministic: uses prime numbers to generate an irregular
    but reproducible pattern across executions.

    Args:
        index (int): Current message index.
        base_delay (float): Base delay in seconds between messages.

    Returns:
        float: Delay in seconds (base_delay or base_delay + 15).
    """
    if index % 97 == 7 or index % 131 == 23:
        return base_delay + 15
    return base_delay


def create_producer() -> KafkaProducer:
    """Create and return a KafkaProducer instance.

    Configured to connect to the local broker (localhost:9092)
    and serialize message values as JSON encoded in UTF-8.

    Returns:
        KafkaProducer: Configured producer instance.
    """
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def stream_csv_to_kafka(producer: KafkaProducer, topic_name: str, csv_file: str) -> None:
    """Read the telemetry CSV and publish each row as a Kafka event.

    Each CSV row is transformed into a message with:
    - Key: player_id (preserves ordering per player within partitions)
    - Timestamp: event time from CSV (not the send time)
    - Value: JSON with measurement fields and metadata

    Args:
        producer (KafkaProducer): KafkaProducer instance.
        topic_name (str): Target Kafka topic name.
        csv_file (str): Path to the sensor data CSV file.
    """
    print("Starting match simulation...")

    df = pd.read_csv(csv_file)

    print(f"Match ready - {len(df)} readings to stream")
    print(f"Streaming telemetry data to topic '{topic_name}'...\n")

    # Group by match and time to simulate event order within each match
    grouped = df.groupby(["partido_id", "time"], sort=True)

    for idx, (group_key, batch) in enumerate(grouped, start=1):
        match_id, time_str = group_key
        event_time = datetime.fromisoformat(time_str)
        event_timestamp_ms = int(event_time.timestamp() * 1000)
        session_id = f"match_{int(match_id)}"

        for _, row in batch.iterrows():
            # Extract data from each event
            player_id = f"player_{int(row['jugador_id'])}"
            bpm = int(row['frecuencia_cardiaca_bpm'])
            pos_x = float(row['pos_x'])
            pos_y = float(row['pos_y'])
            speed_kmh = float(row['velocidad_kmh'])
            acceleration_ms2 = float(row['aceleracion_m_s2'])

            # TODO: Build kafka message

            # TODO: Send message to Kafka

        print(f"Sent {idx}/{grouped.ngroups}")
        time.sleep(random_delay(idx - 1, base_delay=5))

    print(f"Match simulation complete! Streamed {len(df)} readings")


if __name__ == "__main__":
    # Path to the CSV file containing the telemetry data
    csv_file = "sensores_deportivos_fatiga.csv"

    # TODO: Define the topic name for Kafka producer
    topic = ""

    print("Starting Kafka Producer")
    producer = create_producer()

    # Handle graceful Kafka producer when running the script
    try:
        stream_csv_to_kafka(producer, topic, csv_file)
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        producer.close()
        print("Producer closed")

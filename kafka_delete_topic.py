import argparse
from pykafka import KafkaClient


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Avro Producer")

    parser.add_argument('--brokers', type=str, help="The host:port of the broker", required=True)
    parser.add_argument('--zookeeper', type=str, help="The host:port of zookeper", required=True)
    parser.add_argument('--topic', type=str, help="The name of the topic", required=True)

    args = parser.parse_args()

    client = KafkaClient(hosts=args.brokers, zookeeper_hosts=args.zookeeper)
    topic = str.encode(args.topic)

    for b in client.brokers.values():
        try:
            b.delete_topics([topic], 10)
        except:
            pass

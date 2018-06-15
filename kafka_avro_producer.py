from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import argparse
import json
import sys


class KafkaAvroMessageProducer(object):
    def __init__(self, args):
        self.args = args

        self.avro_producer = AvroProducer(
            {
                'bootstrap.servers': self.args.brokers,
                'schema.registry.url': self.args.registry
            },
            default_key_schema=avro.loads(self.args.keyschema),  # key schema
            default_value_schema=avro.loads(self.args.schema)  # value schema
        )

    def produce(self):
        if self.args.input is None:
            # interactive
            for line in sys.stdin:
                clean_line = line.strip()
                if not clean_line:
                    break
                self.produce_one(clean_line, flush=True)
        else:
            with open(self.args.input, 'r') as f:
                for line in f:
                    self.produce_one(line)
            self.avro_producer.flush()

    def produce_one(self, line, flush=False):
        key, value = line.split(self.args.separator)
        self.avro_producer.produce(topic=self.args.topic, key=json.loads(key), value=json.loads(value))
        if flush:
            self.avro_producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Avro Producer")

    parser.add_argument('--schema', type=str, help="The Avro Schema to use for the payload", required=True)
    parser.add_argument('--keyschema', type=str, help="The Avro Schema to use for the key", required=True)
    parser.add_argument('--topic', type=str, help="The name of the topic", required=True)
    parser.add_argument('--brokers', type=str, help="The host:port of the broker", required=True)
    parser.add_argument('--registry', type=str, help="The host:port of the schema registry", required=True)
    parser.add_argument('--separator', type=str, help="The key/value separator", default="|")
    parser.add_argument('--input', type=str, help="The file to use as input")

    arguments = parser.parse_args()

    KafkaAvroMessageProducer(arguments).produce()

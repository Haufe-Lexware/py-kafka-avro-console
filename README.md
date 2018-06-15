Simple utilities to 
- write messages with arbitrary key and value schemas on Kafka and encoded with Avro
- delete Kafka topics

Setup:
```bash
pip3 install -r requirements.txt
```

To produce messages:
```bash
python3 kafka_avro_producer.py \
    --keyschema '{"name":"key","type":"record","fields":[{"name":"service_name","type":"string"},{"name":"tenant_id","type":"string"},{"name":"identity_id","type":"string"},{"name":"entity_id","type":"string"},{"name":"timestamp","type":"long","logicalType":"timestamp-millis"}]}' \
    --schema '{"type":"record","name":"myrecord","fields":[{"name":"f1","type":"string"},{"name":"f2","type":"int"}]}' \
    --brokers 'localhost:9091' \
    --registry 'http://localhost:8081' \
    --topic 'haufe-umantis.avro-producer.1000.v1.cqrs.testavromessage' \
    --input example_scripts/script1_events
```

If the `--input` parameter is not used, it will read events from stdin.

To delete a topic:
```bash
python3 kafka_delete_topic.py \
    --brokers 'localhost:9091' \
    --zookeeper 'localhost:2181' \
    --topic 'haufe-umantis.avro-producer.1000.v1.cqrs.testavromessage'
```

#!/usr/bin/env bash
# تشغيل بعد ما Kafka يبقى healthy:  bash infra/kafka/create_topics.sh
set -e
TOPICS="sensor.readings camera.frames citizen.reports events.perceived incidents.updates verification.requests"
for t in $TOPICS; do
  docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
    --create --if-not-exists --topic "$t" --partitions 1 --replication-factor 1
  docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
    --create --if-not-exists --topic "$t.dlq" --partitions 1 --replication-factor 1
done
echo "topics ready"

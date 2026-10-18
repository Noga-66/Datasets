#!/usr/bin/env bash
set -e
source .env
docker run --rm --network host --entrypoint sh minio/mc -c "
  mc alias set local http://localhost:9000 $MINIO_ACCESS_KEY $MINIO_SECRET_KEY &&
  mc mb --ignore-existing local/camera-frames local/citizen-reports local/incident-evidence"
echo "buckets ready (private by default)"

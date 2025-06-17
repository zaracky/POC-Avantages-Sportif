#!/bin/bash

echo "⏳ En attente que l'API Debezium soit prête..."
until curl -s http://localhost:8083/connectors; do
  sleep 5
done

echo "🔌 Enregistrement du connecteur Debezium..."
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @/docker-entrypoint-initdb.d/connector-config.json

echo "✅ Connecteur enregistré"
tail -f /dev/null

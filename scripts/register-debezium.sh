#!/bin/sh

echo "⏳ En attente que l'API Debezium soit prête..."
until curl -s http://debezium:8083/ > /dev/null; do
  sleep 2
done

echo "🔌 Enregistrement du connecteur Debezium..."
curl -s -X POST http://debezium:8083/connectors \
  -H "Content-Type: application/json" \
  -d @/scripts/connector-config.json

echo "✅ Connecteur Debezium enregistré."

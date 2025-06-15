#  Supervision Grafana + Prometheus pour Airflow & PostgreSQL

Ce dossier contient la configuration de Grafana pour superviser :

- les DAGs Airflow
- les exécutions de tâches
- les métriques de la base PostgreSQL (via `postgres-exporter`)
- l'état global des données

---

##  Contenu

- `provisioning/`: configuration automatique de datasources et dashboards
- `dashboards/`: fichiers JSON des dashboards importés automatiquement
- `grafana.ini`: (optionnel) config statique de Grafana

---

##  Fonctionnement

Grafana est intégré à la stack Docker et connecté à Prometheus via la datasource `Prometheus`.

Prometheus scrape :

- les métriques d’Airflow via `airflow-exporter`
- celles de PostgreSQL via `postgres-exporter`

Les dashboards utilisent les métriques suivantes :

- `airflow_dag_status`
- `airflow_dag_run_status`
- `pg_stat_database_*` (pour PostgreSQL)

---

## Importer un dashboard

1. Aller sur http://localhost:3000
2. Se connecter avec `admin / admin`
3. Menu “+” → “Import” → Coller l’ID ou JSON → Sélectionner la datasource Prometheus

---

## Sécurité

Par défaut, Grafana est exposé en `http://localhost:3000` avec login `admin/admin`. Il est recommandé de changer ce mot de passe.

---

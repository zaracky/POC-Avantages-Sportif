# Sport Avantages — POC Technique

Ce projet est le **Proof of Concept** pour une solution de **suivi d'activité sportive des employés** de Sport Data Solution. L'objectif est de mettre en place un pipeline de données robuste et monitoré, afin de tester l'attribution d'avantages à ceux ayant une pratique sportive régulière.

##  Contexte

> *Objectif :* Favoriser la pratique sportive des collaborateurs via des incitations :
>
> -  Prime de 5% pour les trajets domicile-travail actifs
> -  5 jours "bien-être" pour une activité sportive soutenue
> 
> Le système doit permettre :
> - L'intégration de fichiers d'activité
> - Le monitoring continu (Airflow, PostgreSQL)
> - Capture des changements en base (CDC) avec Debezium + Kafka
> - Déclenchement automatique de DAGs Airflow selon les changements
> - Calcul de l’éligibilité à un remboursement
> - Génération des indemnités
> - Validation de la qualité des données avec Soda
> - Envoi de notifications personnalisées sur Slack

---

## Stack technique

| Composant       | Rôle                                                                 |
|----------------|----------------------------------------------------------------------|
| **PostgreSQL** | Base de données relationnelle pour stocker les données RH et sport  |
| **Airflow**     | Orchestrateur de pipelines pour automatiser le traitement           |
| **Great Expectations** | Contrôle qualité automatisé des fichiers chargés              |
| **Prometheus**  | Collecte de métriques des services (Airflow, PostgreSQL, système)   |
| **Grafana**     | Visualisation des indicateurs via dashboards                        |
| **Debezium + Redpanda**     | Visualisation des indicateurs via dashboards                        |

---

## Architecture actuelle du projet

     p12-project/
        ├── dags/ → DAG Airflow
        ├── data/ → Fichiers de données 
        ├── soda/ →  Configurations de qualité de données
        ├── grafana/
            │ ├── dashboards/ → JSON des dashboards PostgreSQL & Airflow
            │ └── provisioning/ → Datasources & dashboards auto-provisionnés
        ├── monitoring/
            │ └── prometheus.yml → Scraping config pour Prometheus
        ├── kafka-listener/ → Consommateur Kafka avec Slack
        ├── airflow_exporter.py → Exporter Prometheus custom pour Airflow
        ├── Dockerfile.airflow
        ├── Dockerfile.exporter 
        ├── docker-compose.yml
        ├── init.sql → Initialisation de la BDD PostgreSQL
        ├── .env → Secrets d'environnement 
        └── .gitignore


##  Lancer le projet

###  Prérequis

- Docker & Docker Compose

###  Démarrage

    docker compose up --build -d


## Interfaces disponibles

| Outil       | URL                                                                 |
|----------------|----------------------------------------------------------------------|
| **Airflow** | http://localhost:8081	admin / admin  |
| **Adminer**     | http://localhost:8080	PostgreSQL login           |
| **Grafana** | http://localhost:3000	admin / admin             |
| **Prometheus**  | http://localhost:9090   |
| **Redpanda**     |  http://localhost:8082                        |


## Tests
- Insérer une activité manuellement dans PostgreSQL.

- Vérifier que les DAGs sont déclenchés.

- Confirmer l'envoi Slack si l'activité est valide.

- Exécuter validate_data_quality pour checker les données.

##  Sécurité
Ajoutez un fichier .env à la racine :

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX

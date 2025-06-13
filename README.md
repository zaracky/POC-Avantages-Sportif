# Sport Data Monitoring — POC Technique

Ce projet est le **Proof of Concept** pour une solution de **suivi d'activité sportive des employés** de Sport Data Solution. L'objectif est de mettre en place un pipeline de données robuste et monitoré, afin de tester l'attribution d'avantages à ceux ayant une pratique sportive régulière.

##  Contexte

> *Objectif :* Favoriser la pratique sportive des collaborateurs via des incitations :
>
> -  Prime de 5% pour les trajets domicile-travail actifs
> -  5 jours "bien-être" pour une activité sportive soutenue
> 
> Le système doit permettre :
> - L'intégration de fichiers d'activité
> - L'automatisation des calculs
> - Le contrôle qualité des données
> - Le monitoring continu (Airflow, PostgreSQL)

---

## Stack technique

| Composant       | Rôle                                                                 |
|----------------|----------------------------------------------------------------------|
| **PostgreSQL** | Base de données relationnelle pour stocker les données RH et sport  |
| **Airflow**     | Orchestrateur de pipelines pour automatiser le traitement           |
| **Great Expectations** | Contrôle qualité automatisé des fichiers chargés              |
| **Prometheus**  | Collecte de métriques des services (Airflow, PostgreSQL, système)   |
| **Grafana**     | Visualisation des indicateurs via dashboards                        |

---

## Architecture actuelle du projet

📦 p12-project/
├── dags/ → DAG Airflow de validation
├── data/ → Fichiers de données (volumés, ignorés par Git)
├── great_expectations/ → Configuration de GE
├── grafana/
│ ├── dashboards/ → JSON des dashboards PostgreSQL & Airflow
│ └── provisioning/ → Datasources & dashboards auto-provisionnés
├── monitoring/
│ └── prometheus.yml → Scraping config pour Prometheus
├── airflow_exporter.py → Exporter Prometheus custom pour Airflow
├── Dockerfile.airflow
├── Dockerfile.greatexp
├── Dockerfile.exporter → Dockerfile pour l'exporter Airflow
├── docker-compose.yml
├── init.sql → Initialisation de la BDD PostgreSQL
├── .env → Secrets d'environnement (non versionnés)
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
| **Grafana**     | Visualisation des indicateurs via dashboards                        |




# Business problem

Bike-sharing operators need to maintain a high level of service by ensuring that bicycles and docking stations remain available throughout the day. However, demand fluctuates depending on factors such as time of day, weather conditions and location, making it difficult to anticipate when a station will become empty or full.

This project aims to predict these situations one hour in advance in order to support operational decision-making.

```text
Current situation

        ↓

Stations publish their current status through a GBFS feed.

        ↓

Operators need to anticipate stations at risk of becoming empty or full in order to improve redistribution planning and service availability.

        ↓

Our objective is to anticipate these situations.
```
The project is considered successful if it can reliably estimate the probability that a station becomes empty or full within the next hour using publicly available data.

# Project goals

The project has three main objectives:

- Build a reusable and maintainable data platform.
- Predict the probability that a bike-sharing station becomes empty or full within the next hour.
- Demonstrate an end-to-end Machine Learning workflow using modern Data Engineering and MLOps practices.

# Stakeholders

The primary stakeholders are:

- Bike-sharing operators responsible for station availability.
- Operations teams planning bike redistribution.
- Data Scientists developing predictive models.
- Machine Learning Engineers maintaining the production pipeline.

# Scope

### In Scope

- Collect real-time GBFS data.
- Build an historical dataset.
- Enrich operational data with external sources.
- Train and evaluate predictive models.
- Track experiments with MLflow.
- Orchestrate the pipeline with Airflow.

### Out of Scope

- Mobile applications.
- Route optimisation.
- Fleet redistribution optimisation.
- User demand forecasting.

# Data Sources

| Source | Purpose | Status |
|:---------|:---------|:--------|
| GBFS | Real-time bike station status | Planned |
| Weather API | Weather conditions | Planned |
| Calendar | Weekdays, holidays and seasons | Planned |

# High-Level Architecture

```text
          GBFS API
              │
              ▼
      Data Ingestion
              │
              ▼
      Historical Storage
              │
              ▼
    Feature Engineering
              │
              ▼
     Model Training
              │
              ▼
          MLflow
              │
              ▼
        Prediction
```

# Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Package manager | uv |
| Version control | Git |
| Repository | GitHub |
| Data platform | Databricks |
| Storage | Delta Lake |
| Orchestration | Apache Airflow |
| Experiment tracking | MLflow |
| Testing | Pytest |
| Linting | Ruff |

# Roadmap

### v0.1 - Project Initialization

- [x] Create GitHub repository
- [x] Initialize project with uv
- [x] Write project documentation

### v0.2 - Data Ingestion

- [ ] Explore GBFS feeds
- [ ] Implement GBFS client
- [ ] Store raw snapshots

### v0.3 - Data Engineering

- [ ] Build historical dataset
- [ ] Add weather data
- [ ] Implement Bronze / Silver / Gold layers

### v0.4 - Machine Learning

- [ ] Train baseline model
- [ ] Evaluate model performance
- [ ] Track experiments with MLflow

### v0.5 - Pipeline Orchestration

- [ ] Build Airflow DAG
- [ ] Automate the complete pipeline

### v1.0 - Production-like Platform

- [ ] End-to-end reproducible pipeline
- [ ] Documentation
- [ ] CI/CD

# Assumptions and Limitations

* Only publicly available data are considered.
* The prediction horizon is limited to one hour.
* The project focuses on station availability rather than user demand.
* Historical data must be built by periodically collecting GBFS snapshots
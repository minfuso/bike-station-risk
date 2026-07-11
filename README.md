# bike-station-risk
Predict the risk of bike-sharing stations becoming empty or full using real-time data and machine learning.

## Overview

This project aims to build a production-inspired machine learning platform that predicts whether a bike-sharing station will become empty or full within the next hour.

The project focuses on the complete machine learning lifecycle, from data ingestion to model deployment, following modern Data Engineering and MLOps best practices.

## Objectives
* Build a reusable and maintainable data pipeline.
* Collect and store historical bike station data.
* Enrich operational data with external sources such as weather.
* Train and compare multiple machine learning models.
* Track experiments using MLflow.
* Orchestrate workflows with Apache Airflow.
* Develop the project using Databricks and Delta Lake.

## Tech Stack
* Python
* Databricks
* Delta Lake
* Apache Airflow
* MLflow
* Pandas
* Pydantic
* Typer
* Pytest
* Ruff
* Docker (later)
* GitHub Actions

## Project Status

This project is currently under active development.

The first milestone focuses on building a robust data ingestion pipeline using the GBFS standard before introducing machine learning models.

## Repository Structure

```text
bike-station-risk/
├── src/
├── tests/
├── notebooks/
├── configs/
├── data/
├── docs/
└── README.md
```

## Roadmap

### v0.1 - Project initialization

- [x] Create repository
- [x] Initialize with uv
- [x] Configure Ruff
- [x] Configure Pytest

### v0.2 - Data ingestion

- [ ] Explore GBFS API
- [ ] Download station information
- [ ] Download station status
- [ ] Store raw snapshots

### v0.3 - Feature engineering

- [ ] Build historical dataset
- [ ] Add weather data

### v0.4 - Machine Learning

- [ ] Train baseline model
- [ ] Track experiments with MLflow

### v0.5 - Orchestration

- [ ] Build Airflow DAG
- [ ] Schedule daily pipeline

## License

This project is released under the MIT License.

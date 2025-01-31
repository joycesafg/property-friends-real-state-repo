# property-friends-real-state

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

The goal of the project is to build a pipeline to train and deploy a ML Model ensuring reproducibility and scalability

## Project Organization

# FastAPI Model Deployment

This repository contains a FastAPI-based API to serve a trained machine learning model. The training and deployment process is automated using GitHub Actions and Docker.

## Repository Structure

```
/
├── property_friends_real_state/
│   ├── modeling/
│   │   ├── get_data.py  # Downloads data from S3
│   │   ├── train.py     # Trains the model
│   │   ├── predict.py   # Evaluates the model
│   ├── app/
│   │   ├── app.py      # FastAPI app
├── Dockerfile           # Dockerfile to build the API
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt  # Dependencies
├── .github/workflows/
│   ├── ci_cd.yml  # GitHub Actions workflow for training and deployment
├── README.md
```

## Running Locally

### 1. Clone the Repository

```bash
git https://github.com/joycesafg/property-friends-real-state-repo.git
cd property-friends-real-state-repo
```

### 2. Set Up and Run the API Locally

#### Using Python (Without Docker)

```bash
pip install -r requirements.txt
uvicorn property_friends_real_state.app.app:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

#### Using Docker Compose

```bash
docker-compose up
```

## Automated Training and Deployment Workflow (GitHub Actions)

### Overview

1. When pushing to the `main` branch, GitHub Actions executes the `ci_cd.yml` workflow.
2. The workflow:
   - Downloads data from S3
   - Trains the model
   - Saves the model as `model.pkl`
   - Packages the API into a Docker image
   - Pushes the image to GitHub Container Registry (GHCR)

### GitHub Actions Configuration

In the GitHub repository, add the following **secrets**:

- `AKI` (AWS Access Key ID)
- `SAK` (AWS Secret Access Key)
- `GHCR_PAT` (Personal Access Token for GHCR authentication)

The workflow (`.github/workflows/ci_cd.yml`) automates this process.

## Accessing API Logs in MongoDB

The API stores prediction logs in MongoDB. To run locally:

1. Start MongoDB with Docker:

   ```bash
   docker-compose up -d
   ```

2. Access the database:

   ```
    client = MongoClient("mongodb://localhost:27017")
    db = client["logs_db"]
    logs_collection = db.api_logs

    logs = logs_collection.find()
    for log in logs:
        print(log)
   ```

---

**Author:** Joyce Maria do Carmo de Sa
**Contact:** joycesafg@gmail.com


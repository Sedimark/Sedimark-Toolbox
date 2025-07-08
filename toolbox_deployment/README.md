# DP/AI Pipelines Toolbox Docker Compose README

This Docker Compose setup defines a multi-service environment with components for machine learning experimentation, data storage, and orchestration. It includes services for MLflow, PostgreSQL, MinIO, MageAI, Mage API, and an orchestrator, connected via a shared network. Each component is configured for persistence, network connectivity, and port exposure.

## Services

### 1. **MLflow Server (`mlflow`)**
   - **Purpose**: Hosts the MLflow tracking server for logging and managing ML experiments.
   - **Application Repository** [MLFlow](https://github.com/mlflow/mlflow)
   - **Build Context**: `.` (current directory), using `MLflow` Dockerfile.
   - **Ports**: Exposed on port `5000`.
   - **Authentication**: Using the credentials specified in the .env file (`MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD`), defaults to username: `admin`, password: `password`
   - **Depends On**: PostgreSQL service for backend storage.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.
   
### 2. **PostgreSQL Database (`postgres`)**
   - **Purpose**: Provides database storage for MLflow metadata.
   - **Application Repository** [Postgres](https://github.com/postgres/postgres)
   - **Image**: `postgres:latest`
   - **Ports**: Exposed on port `10100` (mapped to PostgreSQL's default `5432`).
   - **Volume**: Mounts `./postgres-data` to persist database data at `/var/lib/postgresql/data`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.

### 3. **MinIO Object Storage (`minio`)**
   - **Purpose**: Object storage for ML artifacts, useful for MLflow experiment logs.
   - **Application Repository** [Minio](https://github.com/minio/minio)
   - **Image**: `minio/minio:latest`
   - **Ports**: Exposed on ports `9000` (API) and `9001` (web console).
   - **Volume**: Persists storage at `/data` within a Docker-managed `minio-data` volume.
   - **Command**: Starts MinIO in server mode at `/data` and web console at `9001`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.

### 4. **MageAI (`magic`)**
   - **Purpose**: Data pipeline tool for data transformation and ML workflows.
   - **Application Repository** [Mage AI](https://github.com/mage-ai/mage-ai)
   - **Image**: `mageai/mageai:latest`
   - **Ports**: Exposed on port `6789`.
   - **Volume**: Maps `./mage` to `home/src/default_repo` within the container.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

### 5. **Mage API (`mageapi`)**
   - **Purpose**: API service for interacting with MageAI.
   - **Application Repository**: [Mage API](https://github.com/Sedimark/MageAPI)
   - **Image**: `ghcr.io/sedimark/mageapi/mage-api:development`
   - **Ports**: Exposed on port `8085`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

### 6. **Orchestrator UI (`orchestrator`)**
   - **Purpose**: Manages workflows and tasks across services.
   - **Application Repository**: [Orchestrator UI](https://github.com/Sedimark/Sedimark-Orchestration-UI)
   - **Image**: `ghcr.io/sedimark/sedimark-orchestration-ui/orchestrator:development`
   - **Ports**: Exposed on port `3000`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

### 6. **MLFlow API (`mlflowapi`)**
   - **Purpose**: Communicates with the MLFlow instances in order to provide information about models to the Orchestrator.
   - **Application Repository**: [MLFlow API](https://github.com/Sedimark/mlflow_api)
   - **Image**: `ghcr.io/sedimark/mlflow_api/mlflow-api:development`
   - **Ports**: Exposed on port `8001`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

## Network

- **shared_network**: A custom Docker network used to allow services to communicate internally.

## Volumes

- **minio-data**: Local Docker volume for MinIO data persistence.
- **postgres-data**: Local Docker volume for Postgres data persistence.

## Usage

1. **Environment Variables**: All `.env` files in `./envs/` are preconfigured and the deployment can be dones as is
2. **Create Shared Network**: 
   ```bash
   docker network create shared_network
   ```
3. **Starting Services**: Run the following command to build and start all services:
   ```bash
   docker-compose up -d
   ```
4. **Accessing Services**:
   - **MLflow**: http://localhost:5000
   - **PostgreSQL**: Exposed on localhost at port `10100`.
   - **MinIO Console**: http://localhost:9001
   - **MageAI**: http://localhost:6789
   - **Mage API**: http://localhost:8085
   - **Orchestrator**: http://localhost:3000
   - **MLFlow API**: http://localhost:8001

5. **Stopping Services**: Use the following to stop and remove containers:
   ```bash
   docker-compose down
   ```
6. **Viewing Logs**:
   ```bash
   docker-compose logs -f
   ```

## Notes
- Modify environment variables as needed for each service in `./envs`.
- Ensure `docker-compose` and Docker are installed on your system.

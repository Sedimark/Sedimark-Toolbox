# DP/AI Pipelines Toolbox Docker Compose README

This Docker Compose setup defines a multi-service environment with components for machine learning experimentation, data storage, and orchestration. It includes services for MLflow, PostgreSQL, MinIO, MageAI, Mage API, and an orchestrator, connected via a shared network. Each component is configured for persistence, network connectivity, and port exposure.

## Services

### 1. **MLflow Server (`mlflow`)**
   - **Purpose**: Hosts the MLflow tracking server for logging and managing ML experiments.
   - **Build Context**: `.` (current directory), using `MLflow` Dockerfile.
   - **Environment File**: `./envs/mlflow.env`
   - **Ports**: Exposed on port `5000`.
   - **Depends On**: PostgreSQL service for backend storage.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.
   
### 2. **PostgreSQL Database (`postgres`)**
   - **Purpose**: Provides database storage for MLflow metadata.
   - **Image**: `postgres:latest`
   - **Environment File**: `./envs/postgres.env`
   - **Ports**: Exposed on port `10100` (mapped to PostgreSQL's default `5432`).
   - **Volume**: Mounts `./postgres-data` to persist database data at `/var/lib/postgresql/data`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.

### 3. **MinIO Object Storage (`minio`)**
   - **Purpose**: Object storage for ML artifacts, useful for MLflow experiment logs.
   - **Image**: `minio/minio:latest`
   - **Environment File**: `./envs/minio.env`
   - **Ports**: Exposed on ports `9000` (API) and `9001` (web console).
   - **Volume**: Persists storage at `/data` within a Docker-managed `minio-data` volume.
   - **Command**: Starts MinIO in server mode at `/data` and web console at `9001`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure.

### 4. **MageAI (`magic`)**
   - **Purpose**: Data pipeline tool for data transformation and ML workflows.
   - **Image**: `mageai/mageai:latest`
   - **Environment File**: `./envs/mage.env`
   - **Ports**: Exposed on port `6789`.
   - **Volume**: Maps `./mage` to `home/src/default_repo` within the container.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

### 5. **Mage API (`mageapi`)**
   - **Purpose**: API service for interacting with MageAI.
   - **Image**: `ghcr.io/jarcaucristian/mage-api:latest`
   - **Environment File**: `./envs/mageapi.env`
   - **Ports**: Exposed on port `8000`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

### 6. **Orchestrator (`orchestrator`)**
   - **Purpose**: Manages workflows and tasks across services.
   - **Image**: `ghcr.io/daniels01ss/orchestrator:latest`
   - **Environment File**: `./envs/orchestrator.env`
   - **Ports**: Exposed on port `3000`.
   - **Network**: `shared_network`
   - **Restart Policy**: On failure, up to 5 retries.

## Network

- **shared_network**: A custom Docker network used to allow services to communicate internally.

## Volumes

- **minio-data**: Local Docker volume for MinIO data persistence.

## Usage

1. **Environment Variables**: All `.env` files in `./envs/` are preconfigured and the deployment can be dones as is
2. **Starting Services**: Run the following command to build and start all services:
   ```bash
   docker-compose up -d
   ```
3. **Accessing Services**:
   - **MLflow**: http://localhost:5000
   - **PostgreSQL**: Exposed on localhost at port `10100`.
   - **MinIO Console**: http://localhost:9001
   - **MageAI**: http://localhost:6789
   - **Mage API**: http://localhost:8000
   - **Orchestrator**: http://localhost:3000

4. **Stopping Services**: Use the following to stop and remove containers:
   ```bash
   docker-compose down
   ```
5. **Viewing Logs**:
   ```bash
   docker-compose logs -f
   ```

## Notes
- Modify environment variables as needed for each service in `./envs`.
- Ensure `docker-compose` and Docker are installed on your system.
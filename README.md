# Sedimark Toolbox

This repository contains all the necessary files to deploy a working instance of the Sedimark Toolbox.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Deployment](#deployment)
- [Component Repositories](#component-repositories)
- [Configuration](#configuration)

## Architecture Overview

This architecture is composed of several key components that together provide a full-stack solution. The toolbox deploys and links each component, ensuring that they work together seamlessly. A high-level diagram of the architecture is provided below:
![High Level Architecuter](images/main-architecture.png)

*Each component is described in further detail in the sections below.*

## Prerequisites

- **Docker & Docker Compose**: Ensure you have Docker installed on your machine.
- **Git**: To clone the repositories.
- **Bash/Shell Environment**: The deployment scripts are written in Bash.

## Installation

Clone the toolbox repository:

```bash
git clone https://github.com/Sedimark/Sedimark-Toolbox.git
cd Sedimark-Toolbox
chmod +x deploy.sh
```

## Deployment

To deploy the entire architecture, simply run:

```bash
./deploy.sh full
```

This script will:
1. Pull the latest images or source code from the individual component repositories.
2. Configure network and volume settings.
3. Launch the containers/services in correct order.

If only parts of the toolbox want to be deployed run:
```bash
./deploy.sh
```

This will prompt the user to tell which parts are to be installed.

## Component Repositories

To learn more about each component follow the links below:

**Mage API**: [https://github.com/Sedimark/MageAPI](https://github.com/Sedimark/MageAPI)
**Orchestrator UI**: [https://github.com/Sedimark/Sedimark-Orchestration-UI](https://github.com/Sedimark/Sedimark-Orchestration-UI)
**MLFlow API**: [https://github.com/Sedimark/mlflow_api](https://github.com/Sedimark/mlflow_api)

## Configuration
 
To configure each container go into the individual folders and follow the READMEs.

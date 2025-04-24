
## Run the broker locally :    

You can find a docker-compose in the stellio repository : https://github.com/stellio-hub/stellio-context-broker

So you can run the broker by cloning the repository then launching the docker compose.
```bash
   git clone https://github.com/stellio-hub/stellio-context-broker.git
   cd stellio-context-broker 
   docker-compose up -d
```
The  will bind itself to the port 8080.

The broker use of multiple services on multiple ports : 
8080 -> api-gateway
8083 -> search-service
8084 -> subscription-service
5432 -> postgres
29092 -> kafka

You can rebind them by setting those variables:
- API_GATEWAY_PORT=
- SEARCH_SERVICE_PORT=
- SUBSCRIPTION_SERVICE_PORT=
- POSTGRES_PORT=
- KAFKA_PORT=

### Some documentation about the API
https://stellio.readthedocs.io/en/latest/API_walkthrough.html

### Link to the NGSILD Specification
https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/gs_cim009v010801p.pdf

### NGSILD additionnal resources
https://ngsild.org/

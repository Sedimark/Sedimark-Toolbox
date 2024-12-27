## Run the broker

### With Docker
```bash   
   docker-compose up -d
```
It will bind itself to the port 8080.

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

### In Kubernetes

You can deploy an instance of the broker with all its dependencies and services in a 
Kubernetes cluster by first setting the necessary environment variables (adjust to your
needs!):

| Name | Example (in clear text) | base64 |
| --- | --- | --- |
| STELLIO_NAMESPACE | stellio | ❌ |
| STELLIO_APP_NAME | stellio | ❌ |
| STELLIO_KAFKA_IMAGETAG | 7.6.0 | ❌ |
| STELLIO_POSTGRES_IMAGETAG | 14-2.11.1-3.3 | ❌ |
| STELLIO_API_IMAGETAG | latest-dev | ❌ |
| STELLIO_SEARCH_IMAGETAG | latest-dev | ❌ |
| STELLIO_SUB_IMAGETAG | latest-dev | ❌ |
| STELLIO_AUTHENTICATION_ENABLED | false | ❌ |
| STELLIO_TENANTS_0_ISSUER | https://keycloak.sedimark.ari-energy.eu/auth/realms/stellio | ❌ |
| STELLIO_TENANTS_0_NAME | urn:ngsi-ld:tenant:default | ❌ |
| STELLIO_TENANTS_0_DBSCHEMA | public | ❌ |
| STELLIO_PAGINATION_LIMIT_DEFAULT | 30 | ❌ |
| STELLIO_PAGINATION_LIMIT_MAX | 100 | ❌ |
| STELLIO_PAGINATION_TEMPORAL_LIMIT | 10000 | ❌ |
| STELLIO_SUBSCRIPTION_ENTITY_SERVICE_URL | http://search-service:8083 | ❌ |
| STELLIO_SUBSCRIPTION_URL | http://localhost:8080 | ❌ |
| STELLIO_KAFKA_URL | stellio-kafka:9092 | ❌ |
| STELLIO_POSTGRES_USER | user | ✅ |
| STELLIO_POSTGRES_PASS | changeme | ✅ |
| STELLIO_SEARCH_DB | stellio_search | ❌ |
| STELLIO_SUBSCRIPTION_DB | stellio_subscription | ❌ |

Then, apply the Kubernetes manifests:

```bash
cat ./kubernetes/0*.yaml | envsubst | kubectl apply -f -
```

No ingress is provided, but you can access the API Gateway service via port-forwarding:

```bash
kubectl port-forward -n $STELLIO_NAMESPACE svc/$STELLIO_APP_NAME-api 8080:8080
```

or internally in the cluster using kubernetes DNS (e.g. `http://${STELLIO_APP_NAME}-api.${STELLIO_NAMESPACE}.svc.cluster.local:8080`).

### Some documentation about the API
https://stellio.readthedocs.io/en/latest/API_walkthrough.html

### Link to the NGSILD Specification
https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/gs_cim009v010801p.pdf

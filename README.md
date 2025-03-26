# Rick and Morty API

The Rick and Morty API allows you to access information about characters, locations from the Rick and Morty show.

## Running directly with Docker (for local development)

```bash
# Navigate to the project directory
cd rick-morty-api

# Build the Docker image
docker build -t rick-morty-api:1.0 .

# Run the container, mapping port 5000 from the container to your local machine
docker run --name rick-morty-api -p 5000:5000 rick-morty-api:1.0
```

## Deploying to Kubernetes with Minikube (for container orchestration)

```bash
# Start Minikube if not already running
minikube start

# Configure terminal to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the Docker image directly in Minikube's environment
docker build -t rick-morty-api:1.0 .

# Apply the Kubernetes manifests
kubectl apply -f yamls/Deployment.yaml
kubectl apply -f yamls/Service.yaml
kubectl apply -f yamls/Ingress.yaml
```

### Verifying the Deployment

```bash
# Check if pods are running
kubectl get pods

# Check the service
kubectl get svc flask-service

# Check the ingress
kubectl get ingress flask-ingress
```

## Deploying with Helm chart

<p>The Rick and Morty API can be deployed using the included Helm chart for more customizable deployments.</p>

```bash
# Install the Helm chart
helm install rick-morty-api Helm/

# Create network routes to services deployed with LoadBalancer type and Ingress
minikube tunnel 
```
<p>We're running `minikube tunnel` for the Ingress because we're using LoadBalancer type in Helm</p>

### Helm Chart Configuration
The following table lists the configurable parameters for the Helm chart and their default values:

| Parameter | Description | Default |
|-----------|-------------|---------|
| appName | Application name | flask |
| replicasCount | Number of replicas | 2 |
| container.image | Container image | rick-morty-api:1.0 |
| container.port | Container port | 5000 |
| service.port | Service port | 5000 |
| service.targetPort | Target port | 5000 |
| service.type | Service type | LoadBalancer |
| ingress.path | Ingress path | / |
| ingress.port | Ingress port | 5000 |

## Accessing the Application

### Method 1: Using minikube service

```bash
# This command will automatically open the service URL in your browser
minikube service flask-service --url
```
<p>This will output a URL (something like http://192.168.49.2:30000) that you can use to access your API.</p>

### Method 2: Using port-forwarding

```bash
# Forward the service port to your local machine
kubectl port-forward service/flask-service 5000:5000
```

### Method 3: Using a Ingress (only with Helm)

```bash
# Get the ingress IP
minikube service --url flask-service
```
<p>Then access the API at http://{flask-service}/api/</p>

### API Endpoints

The API typically includes endpoints such as:

- **GET** /api/characters - Get all characters
- **GET** /api/characters/{name} - Get a specific character by name
- **GET** /api/locations/{location} - Get a specific character by location
- **POST** /api/refresh-data - Refresh Character data
- **GET** /api/healthcheck - Check the health of the API
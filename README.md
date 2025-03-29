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
# Navigate to the project directory
cd rick-morty-api

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
# Navigate to the project directory
cd rick-morty-api

# Start Minikube if not already running
minikube start

# Configure terminal to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the Docker image directly in Minikube's environment
docker build -t rick-morty-api:1.0 .

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


## CI/CD Workflow

This project uses GitHub Actions for continuous integration and deployment. The workflow automates building, testing, and validating the Rick and Morty API.

### Workflow Overview

**Name:** Test and Deploy

**Trigger:** The workflow runs after the CodeQL Advanced security scan completes successfully on the main branch.

### Job: test-deploy

This job handles the entire CI/CD pipeline in a single workflow to maintain state between steps:

#### Setup Steps:
1. **Checkout code** - Retrieves the latest code from the repository
2. **Install kind** - Sets up a Kubernetes in Docker (KinD) environment
3. **Install cluster** - Creates a local Kubernetes cluster named "rick-morty-cluster"

#### Build and Deploy Steps:
4. **Build Docker image** - Creates a Docker image for the Rick and Morty API
5. **Load image into kind** - Makes the Docker image available in the Kubernetes cluster
6. **Deploy to Kubernetes** - Applies the Kubernetes manifests:
   - Deployment - Manages the API container instances
   - Service - Creates internal network endpoint
   - Ingress - Sets up external access rules

#### Testing Steps:
7. **Wait for deployment** - Ensures the API is fully deployed before testing
8. **Install jq** - Adds JSON processing capability for testing
9. **Test API endpoints** - Validates all API endpoints are working:
   - POST /api/refresh-data - Tests data refresh functionality
   - GET /api/healthcheck - Confirms API health status
   - GET /api/characters - Verifies character data retrieval
   - GET /api/characters/Rick - Tests character filtering capability

### Security Integration

The workflow only runs after the CodeQL Advanced security scan completes successfully, ensuring that:
1. No security vulnerabilities are introduced
2. Code quality standards are maintained
3. The deployment process only proceeds with secure code

### Workflow Benefits

- **Automated Testing:** Every change is automatically tested
- **Consistent Environments:** Uses the same Kubernetes setup for testing as production
- **Security First:** Integrates security scanning before deployment
- **Full API Validation:** Tests all critical endpoints to ensure functionality
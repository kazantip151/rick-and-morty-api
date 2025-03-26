# Rick and Morty API

The Rick and Morty API allows you to access information about characters, locations from the Rick and Morty show.

### Running directly with Docker (for local development)

```bash
# Navigate to the project directory
cd rick-morty-api

# Build the Docker image
docker build -t rick-morty-api:1.0 .

# Run the container, mapping port 5000 from the container to your local machine
docker run --name rick-morty-api -p 5000:5000 rick-morty-api:1.0
```

### Deploying to Kubernetes with Minikube (for container orchestration)

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
<p>Then access the API at http://localhost:5000/api/</p>

### Method 3: Using Ingress (if enabled)
<p>If you've enabled the Ingress addon in Minikube:</p>

```bash
# Enable ingress if not already enabled
minikube addons enable ingress

# Get the Minikube IP
minikube ip
```
<p>Then you can access your API at http://[minikube-ip]/ or add an entry to your hosts file.</p>

### API Endpoints

The API typically includes endpoints such as:

- **GET** /api/characters - Get all characters
- **GET** /api/characters/{name} - Get a specific character by name
- **GET** /api/locations/{location} - Get a specific character by location
- **POST** /api/refresh-data - Refresh Character data
- **GET** /api/healthcheck - Check the health of the API
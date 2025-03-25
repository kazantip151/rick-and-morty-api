# Rick and Morty API

The Rick and Morty API allows you to access information about characters, locations from the Rick and Morty show.

### Building the Docker Image

```bash
# Navigate to the project directory
cd rick-morty-api

# Build the Docker image
docker build -t rick-morty-api:1.0 .
```

### Running the Docker Container

```bash
# Run the container, mapping port 5000 from the container to your local machine
docker run --name rick-morty-api -p 5000:5000 rick-morty-api:1.0
```

### Accessing the API
Once the container is running, you can access the API at:
http://localhost:5000/api/

### API Endpoints

The API typically includes endpoints such as:

- **GET** /api/characters - Get all characters
- **GET** /api/characters/{name} - Get a specific character by name
- **GET** /api/locations/{location} - Get a specific character by location
- **POST** /api/refresh-data - Refresh Character data
- **GET** /api/healthcheck - Check the health of the API
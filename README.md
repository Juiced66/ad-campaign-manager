# Ad Campaign Management Platform

## Overview

This project is a full-stack web application designed for managing advertising campaigns in an Ad Tech context. It enables users to create, view, update, delete, and toggle the activation status of campaigns. The backend is built with FastAPI, and the frontend is developed using Vue.js (Vue 3 with the Composition API). A JWT-based authentication system secures the API endpoints, and interactive API documentation is provided via Swagger/Redoc.

## Technical Architecture & Design Patterns

### Domain-Driven Design (DDD)

Our project adheres to DDD principles by keeping business logic central. The **Domain** layer encapsulates key entities (e.g., Campaign and User) along with business rules, ensuring that the system remains easy to maintain and evolve as requirements change.

### Hexagonal Architecture (Ports and Adapters)

We leverage Hexagonal Architecture to decouple our core business logic from external services. The core (domain and application layers) interacts with the outside world through defined ports (interfaces), while adapters (e.g., FastAPI controllers, SQLAlchemy repositories) handle actual communication. This architecture:

- Enhances testability by isolating business logic.
- Simplifies maintenance and future integration with alternative frameworks or databases.

### Repository Pattern

Data persistence is managed using the Repository Pattern. Repositories are defined as interfaces in the domain layer and implemented using SQLAlchemy in the infrastructure layer. This abstraction:

- Isolates business logic from database-specific concerns.
- Facilitates switching between different storage solutions.
- Simplifies unit testing through the use of mocks or stubs.

### Additional Patterns & Practices

- **Service Layer:** Coordinates business operations between repositories and domain entities.
- **Factory Pattern:** Standardizes object creation through dedicated factory methods.
- **Dependency Injection:** Decouples components, streamlining testing and maintenance.

## Main Project Launch Using Docker

Docker is the primary method for launching and deploying the project. This ensures consistency across environments and simplifies both development and production deployments.

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Launching the Project

1.  **Build and Start Containers:**
    - From the root directory, run:
      ```bash
      docker-compose up --build
      ```
    - This command builds the Docker images and starts the containers for the backend and frontend services.

2.  **Access the Application:**
    - The FastAPI backend will be available at [http://localhost:8000](http://localhost:8000).
    - The Vue.js frontend will be accessible at [http://localhost:5173](http://localhost:5173).
    - API documentation is available via Swagger/Redoc at [http://localhost:8000/docs](http://localhost:8000/docs) or [http://localhost:8000/redoc](http://localhost:8000/redoc).

3.  **Container Management:**
    - To stop the containers, run:
      ```bash
      docker-compose down
      ```

## Deployment with Minikube

As an alternative to Docker Compose, you can deploy the application to a local Kubernetes cluster using Minikube. This is useful for testing Kubernetes manifests and behavior locally.

### Prerequisites

-   [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed.
-   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) installed.
-   Docker installed (Minikube often uses it as a driver).

### Steps

1.  **Start Minikube:**
    Open your terminal and start a Minikube cluster:
    ```bash
    minikube start
    ```
    Verify the cluster is running:
    ```bash
    minikube status
    ```

2.  **Point Docker CLI to Minikube's Docker Daemon:**
    This is crucial so that Docker builds images directly into Minikube's environment, allowing the `imagePullPolicy: IfNotPresent` in the Kubernetes manifest to work correctly.

    -   On Linux/macOS (bash/zsh):
        ```bash
        eval $(minikube -p minikube docker-env)
        ```
    -   On Windows (PowerShell):
        ```bash
        minikube -p minikube docker-env | Invoke-Expression
        ```
    *Note: This command configures Docker for the current terminal session only. If you open a new terminal, you'll need to run it again.*

3.  **Build Docker Images:**
    Now, build the backend and frontend images. Because your Docker CLI points to Minikube's daemon, these images will be available within the Minikube cluster.
    ```bash
    # From the project root directory
    docker build -t fastapi-ad-app:latest ./backend
    docker build -t vue-ad-app:latest ./frontend
    ```

4.  **Apply Kubernetes Manifests:**
    Deploy the application components using the provided manifest file:
    ```bash
    kubectl apply -f k8s-deployment.yaml
    ```
    This will create the Deployments, Services, ConfigMaps, and the PersistentVolumeClaim.

5.  **Check Deployment Status:**
    Wait for the pods to be created and become ready. You can check their status:
    ```bash
    kubectl get pods -w
    # Press Ctrl+C when pods are 'Running'
    ```
    You can also check the services and PVC:
    ```bash
    kubectl get services
    kubectl get pvc
    ```

6.  **Access the Frontend:**
    The frontend service (`frontend-service`) is exposed using `NodePort`. Find the URL to access it:
    ```bash
    minikube service frontend-service --url
    ```
    Open the URL provided by this command in your web browser. It will look something like `http://192.168.X.X:YYYYY`.

7.  **Accessing the Backend (Optional):**
    The backend service (`fastapi-service`) is of type `ClusterIP` by default, meaning it's only directly reachable *within* the Minikube cluster (the frontend accesses it using the service name `fastapi-service`). If you need direct access from your host machine (e.g., for API testing with tools like `curl` or Postman), you can use port-forwarding:
    ```bash
    # Forward host port 8000 to the service's port 8000
    kubectl port-forward service/fastapi-service 8000:8000
    ```
    While this command is running, you can access the backend API at `http://localhost:8000`.

### Cleanup

1.  **Delete Kubernetes Resources:**
    ```bash
    kubectl delete -f k8s-deployment.yaml
    ```
    This removes the Deployments, Services, ConfigMaps, but usually *not* the PersistentVolume associated with the PVC by default (to prevent accidental data loss).

2.  **Stop Minikube:**
    ```bash
    minikube stop
    ```

3.  **(Optional) Delete Minikube Cluster:**
    If you want to completely remove the cluster and its data (including the persistent volume):
    ```bash
    minikube delete
    ```

4.  **Unset Docker Environment (Optional):**
    To point your Docker CLI back to your host's default daemon (if you didn't close the terminal):
    -   On Linux/macOS (bash/zsh):
        ```bash
        eval $(minikube docker-env -u)
        ```
    -   On Windows (PowerShell):
        ```bash
        minikube docker-env -u | Invoke-Expression
        ```

## Technologies

-   **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
-   **Frontend:** Vue.js (Vue 3 with Composition API), Vue Router, Pinia, Tailwind CSS, Vue Toastification
-   **Database:** SQLite (development/Minikube)
-   **Authentication:** JWT for secure API access (with refresh tokens)
-   **Testing:** Pytest (backend), Vitest (frontend)
-   **Containerization:** Docker and Docker Compose
-   **Orchestration (Local):** Kubernetes (via Minikube)

## ✨ Features

-   Create / edit / duplicate / delete ad campaigns
-   Toggle campaign activation status
-   Filter and paginate campaign list
-   JWT-based authentication with refresh tokens and protected routes
-   User profile settings update (email/password)
-   Responsive UI with Vue 3 + Tailwind CSS
-   API documentation via Swagger/Redoc
-   Docker Compose setup for easy local development
-   Minikube deployment option for local Kubernetes testing

## Setup & Installation (Without Containers)

### Backend Setup

1.  **Prerequisites:** Python 3.10+
2.  Navigate to the `backend` directory.
3.  Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Copy `backend/.env.example` to `backend/.env.dev` and configure environment variables if needed (defaults should work for basic local run).
6.  Run the FastAPI server:
    ```bash
    # From the backend directory
    uvicorn app.presentation.api.v1.main:app --reload --env-file .env.dev
    ```
7.  Access the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Setup

1.  **Prerequisites:** Node.js 18+ and npm
2.  Navigate to the `frontend` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
5.  Start the development server:
    ```bash
    npm run dev
    ```
6.  Access the frontend at [http://localhost:5173](http://localhost:5173).

## Testing

-   **Backend:**
    -   Using Docker Compose: `docker-compose exec fastapi pytest`
    -   Locally (ensure virtual env is active): `pytest` from the `backend` directory.
-   **Frontend:**
    -   Navigate to the `frontend` directory.
    -   Run tests: `npm run test`

## Future Improvements

-   Enhanced logging and error monitoring integration.
-   More comprehensive end-to-end tests.
-   Database migrations (e.g., using Alembic) for easier schema evolution.
-   Role-based access control (RBAC).

## Conclusion

This project demonstrates modern full-stack development techniques tailored for an Ad Tech environment. By leveraging Domain-Driven Design, Hexagonal Architecture, and the Repository Pattern, we ensure a clean, scalable, and maintainable codebase that not only meets current requirements but is also primed for future enhancements.

![Build](https://img.shields.io/github/actions/workflow/status/Juiced66/ad-campaign-manager/ci.yml)
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

1. **Build and Start Containers:**

   - From the root directory, run:
     ```bash
     docker-compose up --build
     ```
   - This command builds the Docker images and starts the containers for the backend, frontend, and database services.

2. **Access the Application:**

   - The FastAPI backend will be available (e.g., at [http://localhost:8000](http://localhost:8000)).
   - The Vue.js frontend will be accessible (e.g., at [http://localhost:5173](http://localhost:5173)).
   - API documentation is available via Swagger/Redoc at [http://localhost:8000/docs](http://localhost:8000/docs). or [http://localhost:8000/redoc](http://localhost:8000/redoc) 

3. **Container Management:**

   - To stop the containers, run:
     ```bash
     docker-compose down
     ```

## Technologies

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** Vue.js (Vue 3 with Composition API), Vue Router, and a CSS framework (Tailwind CSS)
- **Database:** SQLite (development) with an option to switch to MySQL in production
- **Authentication:** JWT for secure API access
- **Testing:** Pytest for backend tests and Vitest for frontend tests
- **Containerization:** Docker and Docker Compose

## Setup & Installation

### Backend Setup

1. **Without Docker (optional):**
   - Create and activate a virtual environment.
   - Install the required Python packages:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - Copy `.env.example` to `.env` and configure your environment variables.
   - Run the FastAPI server:
     ```bash
     uvicorn app.presentation.api.v1.main:app --reload
     ```
   - Access the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Setup

1. **Without Docker (optional):**
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm run dev
     ```

## Testing

- **Backend:** Run tests using:
  ```bash
  docker-compose exec fastapi pytest
  ```
  You can also run tests locally if not using Docker, but you'll need to create a virtual environment and install dependencies as shown above.
- **Frontend:** Execute tests with:
  ```bash
  npm run test
  ```

## Future Improvements

- Enhanced logging and error handling.
- Advanced UI/UX features.
- Further automation through CI/CD pipelines.

## Conclusion

This project demonstrates modern full-stack development techniques tailored for an Ad Tech environment. By leveraging Domain-Driven Design, Hexagonal Architecture, and the Repository Pattern, we ensure a clean, scalable, and maintainable codebase that not only meets current requirements but is also primed for future enhancements.



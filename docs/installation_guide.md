# Installation Guide

## Prerequisites
-   **Docker** & **Docker Compose** (Recommended)
-   **Python 3.9+** (For manual setup)
-   **Node.js 16+** (For manual setup)
-   **Redis** (For manual setup)

## Option 1: Docker Setup (Recommended)
This is the easiest way to run the full stack (Backend, Frontend, Redis, Worker).

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/parallel-ecommerce-recommender.git
    cd parallel-ecommerce-recommender
    ```

2.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the App**:
    -   Frontend: [http://localhost:3000](http://localhost:3000)
    -   Backend API: [http://localhost:5000](http://localhost:5000)

## Option 2: Manual Setup

### 1. Backend Setup
1.  Navigate to the project root.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    pip install rq
    ```
4.  Start Redis (ensure it's running on localhost:6379).
5.  Start the Worker (in a separate terminal):
    ```bash
    python -m backend.api.tasks.worker
    ```
6.  Start the Flask API:
    ```bash
    python -m backend.api.app
    ```

### 2. Frontend Setup
1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```

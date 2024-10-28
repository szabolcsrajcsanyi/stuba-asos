# STUBA ASOS Project

This project is part of a school subject and focuses on creating a platform for buying and selling tickets. 

## Project Overview

The website is accessible at [http://46.101.254.37](http://46.101.254.37). For detailed API documentation, visit [http://46.101.254.37/api/docs](http://46.101.254.37/api/docs).

## Contributing

To contribute to this project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/stuba-asos.git
    ```
2. Navigate to the project directory:
    ```sh
    cd stuba-asos
    ```

## Running Locally

To run the project locally, use Docker Compose:

1. Build and start the containers:
    ```sh
    docker compose up --build -d
    ```
2. Navigate to the frontend directory:
    ```sh
    cd frontend
    ```
3. Install the dependencies:
    ```sh
    npm install
    ```
4. Start the frontend application:
    ```sh
    npm run
    ```

**Note:** Ensure that the backend URL in the React app is switched to the local backend URL.

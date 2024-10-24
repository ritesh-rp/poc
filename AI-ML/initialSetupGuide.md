## Setup and Activate flask-server / predictionModel Directories

- Checkout to flask-server/predictionModel directories
- Initiate venv
    ```bash
    python -m venv .venv
    ```

- Activate virtual environment
    - Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - Unix:
        ```bash
        source venv/bin/activate
        ```

- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Steps to run project
- To start backend server go to flask-server
    ```bash
    python3 server.py
    ```
- To start frontend go to client 
    ```bash
    npm start
    ```

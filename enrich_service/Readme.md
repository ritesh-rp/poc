## Enrich Service
Welcome to Enrich Service, this project is all about getting user and company's information from linkedin and other websites

### Python Version
`Python 3.11.6`

<<<<<<< HEAD
=======
### Table of Contents
- [`Docker Setup` ](Running with Docker)
- [`Run Locally`](Running without Docker)

>>>>>>> 439a6ea042853d464d860f6ef20a4fef9b6347d6
### Cloning
*  Clone the repository to your local machine.

   ```bash
   git clone https://github.com/CustomerCity/enrich_service.git
   cd enrich_service
   ```
    Set up your environment variables based on the `sample_env` file. Update the variables in your environment or `.env` file.
    
### Running with Docker
   ```bash
   docker-compose build
   ```
   ```bash
   docker-compose up
   ```
### Running without Docker
* Create Python virtual environment & activate it
```bash
python -m venv venv
./venv/bin/activate
```
* Install the required dependencies
```bash
pip install -r requirements.txt
```
* Run the server
```bash
python manage.py runserver
```

* Server will start running locally at `http://localhost:8000.`


`Run Celery` : celery -A celery_app.celery worker -l info

# Inventory Managment API

This project is an API REST developed with:
- docker
- docker compose
- python
- PostgreSQL

Below are the steps to set up and run the project on your local environment.

---

## Prerequisites

Before you get started, make sure you have the following installed on your machine:

- **docker**
- **docker compose**

---

## Installation

Follow these steps to set up your development environment:

### 1.  Clone repository
Clone this repository from GitHub.com to your local computer

```bash
git clone https://github.com/agamezr/inventory_managment.git
```

```bash
cd inventory_managment
```

### 2. Create the .env file at the root of the project

```bash
DB_NAME=               # Database name
DB_USER=               # PostgreSQL username
DB_PASSWORD=           # PostgreSQL password
DB_HOST=               # PostgreSQL host (e.g., localhost)
DB_PORT=               # PostgreSQL port (default: 5432)
DATABASE_URL=          # Database URL
```

### 3. Replace this line with the same value of DATABASE_URL in the .env in alembic.ini file

```bash
# alembic.ini
sqlalchemy.url =
```

### 4. Build the project
Docker must be running and your console must be in the project path

```bash
docker compose build
```

### 5. Run migrations 
This command creates the Database

```bash
docker compose run python-api alembic upgrade head
```


### 6. Run the project
This command runs the container

```bash
docker compose up
```


### 7. Create default data for database (only the first time)
This commands runs a script to charge default information.
- ```docker compose up``` must be running in another console/terminal

Start an interactive session inside the container using the shell
```bash
docker compose exec python-api sh
```

Inside the container run
```bash
PYTHONPATH=/app python app/db/seed.py
```


---

## Daily Work

### 1. Run the project
This command runs the container

```bash
docker compose up
```

### 2. Check Swagger Doc
Go to the next url to check the API documentation:

 [API](http://localhost:8000/docs)

### 3. Work with Postman

In the root path of the project you can find a postaman collection in json format


Open your Postman client and import a collection


```bash
file:  inventory managment API.postman_collection.json
```

When you need to stop the project, run:

```bash
docker compose down
```

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

## Notes
Using the ```docker compose``` or ```docker-compose``` command will depend on your version and configuration of docker compose.

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
**if you are setup the project in a EC2 instance you can copy your local .env file to your instance:**

```bash
sc -i "pem_file.pem" .env ec2-user@PUBLIC_IP:/home/ec2-user/YOUR/PATH/inventory_managment
```

### 3. Replace this line with the same value of DATABASE_URL in the .env in alembic.ini file

```bash
# alembic.ini
sqlalchemy.url =
```

**if you are setup the project in a EC2 instance you can use nano to update the file:**

```bash
nano alembic.ini
```


### 4. Build the project
Docker must be running and your console must be in the project path

```bash
docker compose build
```

### 5. Run migrations 
This command creates the Database

- ```docker compose up``` must be running in another console/terminal
- or ```docker compose up -d``` to run containers in the background

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
- or ```docker compose up -d``` to run containers in the background

Start an interactive session inside the container using the shell
```bash
docker compose exec python-api sh
```

Inside the container run
```bash
PYTHONPATH=/app python app/db/seed.py
```

```bash
exit
```

### 8.  Use the API

Run the project
```bash
docker compose up
```

or
```bash
docker compose up
```

Open the API in the local port 8000:
- http://localhost:8000/docs

If you are currently setup the project in a EC2 instance check:
- http://PUBLIC_IP:8000/docs

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

## AWS Deployment

Follow these steps to deploy :

### 1.  Create a EC2 Instance
- Go to AWS
- Search and open **EC2** service
  - [view image](https://drive.google.com/file/d/1cvPtXn8-ypxuPwDA1ClsKJyPXR6hjG5b/view)
 
- Go to dashboard
- Select the option **Launch instance**
  - [view image](https://drive.google.com/file/d/17uUDi10pFfbUlR0_HoDUJl8Vdyksd2bi/view?usp=drive_link)
 
  
- Name your instance
- Select **Amazon Linux**
  - [view image](https://drive.google.com/file/d/1e4EvrtQvMPQ0aeHnrUEpU5hGz_0t65ch/view?usp=sharing) 

- Create a new key pair (PEM FILE)
- **Launch Instance**
  - [view image](https://drive.google.com/file/d/1khgf5QjhW8WWxrIf2mVnZo0f_eOQDD3X/view?usp=sharing)

### 2.  Config port for the API
- Go to the instance page
- Go to secuirity and secuirity group
  - [view image](https://drive.google.com/file/d/1yn_byFibUEDVlWOz4nlvyL2mPNYz3xoU/view?usp=sharing)
 
- **Edit inbound rules**
- Add the port
  - [view image](https://drive.google.com/file/d/19f_F7415feMq4eV49A0Ciw6t10NGEtIr/view?usp=sharing)


### 3. Connect with the instance from local

Give the correct permissions to your pem file

```bash
chmod 400 pem_file
```

Connect to the instance

```bash
ssh -i "pem_file.pem" ec2-user@PUBLIC_IP
```

or

```bash
ssh -i "pem_file.pem" ec2-user@DNS
```

### 4. Setup the instance tools

Install docker

```bash
sudo yum install -y docker
```

Run docker service
```bash
sudo service docker start
```

Add ec2-user to docker group
```bash
sudo usermod -a -G docker ec2-user
```
Reload a Linux user's group assignments to docker w/o logout
```bash
newgrp docker
```
Enable automatic docker service
```bash
sudo chkconfig docker on
```

Install docker compose
```bash
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

Follow **Installation** steps into the EC2 instance


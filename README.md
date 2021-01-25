# My City - My Places

## Table of Contents
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Run](#run)
    - [Stop](#stop)
  - [Built With](#built-with)
  - [Architecture](#architecture)
  - [Authors](#authors)

## Getting Started

### Prerequisites

Create your secret files:

```bash
mkdir secrets
echo my_super_db             > secrets/database_db
echo my_super_user           > secrets/database_user
echo my_super_password       > secrets/database_password
echo my_super_email          > secrets/email_address
echo my_super_email_password > secrets/email_password
echo my_super_auth_jwt_key   > auth_jwt_key
```

You can also run ```secrets.sh``` script to generate those files:

```bash
./secrets.sh
```

In order to run this project, you must have installed [docker-compose](https://docs.docker.com/compose/install/).

### Run

To run the project on a local environment, use:
```bash
# run
docker-compose up

# run in detached mode (background)
docker-compose up -d

# rebuild images
docker-compose up --build
```

### Stop

To run the the docker stack, use:
```bash
# stop
docker-compose down

# stop and remove created volumes
docker-compose down -v
```

## Documentation

<img src="./images/paper-01.png">
<img src="./images/paper-02.png">
<img src="./images/paper-03.png">
<img src="./images/paper-04.png">
<img src="./images/paper-05.png">
<img src="./images/paper-06.png">
<img src="./images/paper-07.png">
<img src="./images/paper-08.png">
<img src="./images/paper-09.png">
<img src="./images/paper-10.png">
<img src="./images/paper-11.png">
<img src="./images/paper-12.png">
<img src="./images/paper-13.png">
<img src="./images/paper-14.png">
<img src="./images/paper-15.png">
<img src="./images/paper-16.png">
<img src="./images/paper-17.png">
<img src="./images/paper-18.png">
<img src="./images/paper-19.png">
<img src="./images/paper-20.png">
<img src="./images/paper-21.png">
<img src="./images/paper-22.png">
<img src="./images/paper-23.png">

## Authors

WIP

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

## Authors

WIP

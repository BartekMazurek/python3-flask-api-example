## Python3 - simple Flask REST API

## 1 - How to set up

#### 1.1 Run project docker container
> docker-compose up

#### 1.2 Set up virtual environments module
> python3.10 -m venv .venv

***

## 2 - Set up database
#### 2.1 Create database & run migrations
> flask db init

> flask db upgrade

#### 2.2 Create new migration file after model changes
> flask db migrate

***

## 3 - Get documentation
> http://localhost:5000/swagger-ui
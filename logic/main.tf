terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_network" "internal" {
  name = "internal_network"
}

resource "docker_image" "mysql" {
  name         = "mysql:latest"
  keep_locally = false
}

# Contenedor MySQL
resource "docker_container" "mysql" {
  image   = docker_image.mysql.image_id
  name    = "mysql_container"
  command = ["--init-file", "/docker-entrypoint-initdb.d/init.sql" ]
  ports {
    internal = 3306
    external = 3306
  }
  restart = "always"
  volumes {
    host_path      = "/home/ubuntu/FinalTelematica/logic/db/init.sql"
    container_path = "/docker-entrypoint-initdb.d/init.sql"
  }
  env = ["MYSQL_ROOT_PASSWORD=1234", "MYSQL_DATABASE=users"]
  must_run = true
  networks_advanced {
    name = docker_network.internal.name
  }
}

resource "docker_image" "fastapi_app" {
  name         = "python:3.8-slim"
  keep_locally = false
}

# Contenedor FastAPI App
resource "docker_container" "fastapi_app" {
  image   = docker_image.fastapi_app.image_id
  name    = "fastapi_app_container"
  command = ["sh", "/app/setup.sh"]
  ports {
    internal = 8000
    external = 8000
  }
  volumes {
    host_path      = "/home/ubuntu/FinalTelematica/logic/app"
    container_path = "/app/"
  }
  must_run = true
  networks_advanced {
    name = docker_network.internal.name
  }
}

resource "docker_image" "fastapi_api" {
  name         = "python:3.8-slim"
  keep_locally = false
}

resource "docker_container" "fastapi_api" {
  image = docker_image.fastapi_api.image_id
  name  = "fastapi_api_container"
  command = [
    "sh", "/api/setup.sh"
  ]
  ports {
    internal = 8001
    external = 8001
  }
  volumes {
    host_path      = "/home/ubuntu/FinalTelematica/logic/api"
    container_path = "/api/"
  }
  must_run = true
  networks_advanced {
    name = docker_network.internal.name
  }
}
# environments/dev/main.tf
terraform {
  backend "s3" {
    bucket         = "tthau-mvs-tf-state"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tthau-mvs-tf-locks"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      Managed_by  = "terraform"
    }
  }
}

# Resource Groups
module "resource_groups" {
  source = "../../modules/resource-groups"

  project     = var.project
  environment = var.environment
}

# Network
module "network" {
  source = "../../modules/network"

  project     = var.project
  environment = var.environment
  vpc_cidr    = "10.0.0.0/16"
}

# ECR Repositories
module "ecr" {
  source = "../../modules/ecr"

  project      = var.project
  environment  = var.environment
  repositories = ["frontend", "backend"]
}

# CodeCommit Repositories
module "repositories" {
  source = "../../modules/repositories"

  project     = var.project
  environment = var.environment

  repositories = {
    frontend = {
      name        = "frontend"
      description = "Frontend React application"
      branch      = "master"
    }
    backend = {
      name        = "backend"
      description = "Backend Node.js API"
      branch      = "master"
    }
  }
}

# ECS Services
module "ecs" {
  source = "../../modules/ecs"

  project            = var.project
  environment        = var.environment
  vpc_id             = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
  public_subnet_ids  = module.network.public_subnet_ids

  services = {
    frontend = {
      container_image   = "${module.ecr.repository_urls["frontend"]}:latest"
      container_port    = 80
      desired_count     = 1
      health_check_path = "/health"
    }
    backend = {
      container_image   = "${module.ecr.repository_urls["backend"]}:latest"
      container_port    = 3000
      desired_count     = 1
      health_check_path = "/api/health"
    }
  }
}

# MongoDB
module "mongodb" {
  source = "../../modules/mongodb"

  project         = var.project
  environment     = var.environment
  vpc_id          = module.network.vpc_id
  subnet_id       = module.network.private_subnet_ids[0]
  ecs_tasks_sg_id = module.ecs.security_group_ids.ecs_tasks
  key_name        = var.key_name
}

# CI/CD Pipeline
module "pipeline" {
  source = "../../modules/pipeline"

  project          = var.project
  environment      = var.environment
  ecs_cluster_name = module.ecs.cluster_name

  repository_configs = {
    frontend = {
      name           = module.repositories.repository_names["frontend"]
      service_name   = module.ecs.service_names["frontend"]
      ecr_repo_url   = module.ecr.repository_urls["frontend"]
      build_specfile = "buildspec.yml"
    }
    backend = {
      name           = module.repositories.repository_names["backend"]
      service_name   = module.ecs.service_names["backend"]
      ecr_repo_url   = module.ecr.repository_urls["backend"]
      build_specfile = "buildspec.yml"
    }
  }
}

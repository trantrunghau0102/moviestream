# modules/pipeline/variables.tf
variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "repository_configs" {
  type = map(object({
    name           = string
    service_name   = string
    ecr_repo_url   = string
    build_specfile = string
  }))
}

variable "ecs_cluster_name" {
  type = string
}

locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    Managed_by  = "terraform"
  }
}

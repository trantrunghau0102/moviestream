# modules/ecs/variables.tf
variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "services" {
  type = map(object({
    container_image   = string
    container_port    = number
    desired_count     = number
    health_check_path = string
  }))
}

locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    Managed_by  = "terraform"
  }
}

# modules/mongodb/main.tf
resource "aws_security_group" "mongodb" {
  name        = "${var.project}-${var.environment}-mongodb-sg"
  description = "Security group for MongoDB"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 27017
    to_port         = 27017
    protocol        = "tcp"
    security_groups = [var.ecs_tasks_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.tags
}

resource "aws_instance" "mongodb" {
  ami           = data.aws_ami.ubuntu.id # Using data source instead of hardcoded AMI
  instance_type = "t3.medium"
  subnet_id     = var.subnet_id
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.mongodb.id]

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update && apt-get install -y gnupg
              wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
              echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
              apt-get update
              apt-get install -y mongodb-org
              systemctl start mongod
              systemctl enable mongod
              EOF

  tags = merge(local.tags, {
    Name = "${var.project}-${var.environment}-mongodb"
  })
}

# Add data source for Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical owner ID
}

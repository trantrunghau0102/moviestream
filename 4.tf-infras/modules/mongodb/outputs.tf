# modules/mongodb/outputs.tf
output "mongodb_instance_id" {
  value = aws_instance.mongodb.id
}

output "mongodb_private_ip" {
  value = aws_instance.mongodb.private_ip
}

output "mongodb_security_group_id" {
  value = aws_security_group.mongodb.id
}

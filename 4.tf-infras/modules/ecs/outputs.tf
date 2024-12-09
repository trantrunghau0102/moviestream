# modules/ecs/outputs.tf
output "cluster_id" {
  value = aws_ecs_cluster.main.id
}

output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "service_names" {
  value = {
    for k, v in aws_ecs_service.services : k => v.name
  }
}

output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "security_group_ids" {
  value = {
    alb       = aws_security_group.alb.id
    ecs_tasks = aws_security_group.ecs_tasks.id
  }
}

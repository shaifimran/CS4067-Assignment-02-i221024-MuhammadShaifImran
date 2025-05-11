output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "The ID of the VPC"
}

output "load_balancer_dns" {
  value       = aws_lb.app_lb.dns_name
  description = "The DNS name of the load balancer"
}

output "asg_name" {
  value       = aws_autoscaling_group.app_asg.name
  description = "The name of the Auto Scaling Group"
}

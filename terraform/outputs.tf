data "aws_instances" "app" {
  filter {
    name   = "tag:Name"
    values = ["event-booking-app"]
  }
}

output "instance_ids" {
  description = "IDs of the EC2 instances"
  value       = aws_autoscaling_group.app_asg.instances[*].id
}

output "instance_ips" {
  description = "Public IPs of the app servers"
  value       = data.aws_instances.app.instances[*].public_ip_address
}

data "aws_instances" "app" {
  filter {
    name   = "tag:Name"
    values = ["event-booking-app"]
  }
}

output "instance_ips" {
  value = data.aws_instances.app.instances[*].public_ip_address
}

output "instance_ids" {
  value = aws_autoscaling_group.app.instances[*].id
}

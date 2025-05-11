# data source to discover all EC2s tagged Name=event-booking-app
data "aws_instances" "app" {
  filter {
    name   = "tag:Name"
    values = ["event-booking-app"]
  }
}

# Public IPs of all instances in your ASG
output "instance_ips" {
  description = "Public IPs of the app servers"
  value       = data.aws_instances.app.public_ips
}

# IDs of all instances in your ASG
output "instance_ids" {
  description = "IDs of the app servers"
  value       = data.aws_instances.app.ids
}

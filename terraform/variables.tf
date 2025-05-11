variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-west-2"
}

variable "admin_role_arn" {
  description = "IAM Role ARN for cluster admin"
  type        = string
  default     = "arn:aws:iam::561805236639:role/event-booking-cluster-cluster-20250510115416765200000002"
}

variable "friend_role_arn" {
  description = "IAM Role ARN for your friend"
  type        = string
  default     = ""
}

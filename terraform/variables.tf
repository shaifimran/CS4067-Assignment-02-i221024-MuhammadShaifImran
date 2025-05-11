variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-west-2"
}

variable "admin_role_arn" {
  description = "IAM Role ARN for cluster admin"
  type        = string
}

variable "friend_role_arn" {
  description = "IAM Role ARN for your friend"
  type        = string
  default     = ""
}

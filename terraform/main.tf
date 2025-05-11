terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"                # use the latest AWS provider
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Credentials will be read from the AWS CLI config or environment:
  #   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
}

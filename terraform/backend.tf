terraform {
  backend "s3" {
    bucket = "devops-project-fast2025-states"
    key    = "event-booking/terraform.tfstate"
    region = "us-east-1"
  }
}

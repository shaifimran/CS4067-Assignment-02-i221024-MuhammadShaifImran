terraform {
  backend "s3" {

    bucket = "devops-project-fast2025-bucket"
    key    = "event-booking/terraform.tfstate"
    region = "us-west-2"
  }
}

terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.34"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.8"
    }
  }
}

data "terraform_remote_state" "infra" {
  backend = "s3"
  config = {
    bucket = "devops-project-fast2025-states"
    key    = "event-booking/terraform.tfstate"
    region = var.aws_region
  }
}

data "aws_eks_cluster_auth" "auth" {
  name = data.terraform_remote_state.infra.outputs.cluster_name
}

provider "kubernetes" {
  host                   = data.terraform_remote_state.infra.outputs.cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.infra.outputs.cluster_ca_certificate)
  token                  = data.aws_eks_cluster_auth.auth.token
}

provider "helm" {
  kubernetes {
    host                   = data.terraform_remote_state.infra.outputs.cluster_endpoint
    cluster_ca_certificate = base64decode(data.terraform_remote_state.infra.outputs.cluster_ca_certificate)
    token                  = data.aws_eks_cluster_auth.auth.token
  }
}

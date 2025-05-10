output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS API endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_ca_certificate" {
  description = "Base64-encoded CA data"
  value       = module.eks.cluster_certificate_authority_data
}

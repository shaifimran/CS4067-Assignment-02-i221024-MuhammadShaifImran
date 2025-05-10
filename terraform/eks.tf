module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 19.0"

  cluster_name    = "event-booking-cluster"
  cluster_version = "1.27"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets

  # Allow the API server on the Internet
  cluster_endpoint_public_access = true
  # Restrict to your laptop's IP (replace with your actual public IP)
  cluster_endpoint_public_access_cidrs = ["154.192.1.45/32"] # this is my public IP
  # (you can leave private access on)
  cluster_endpoint_private_access = true

  eks_managed_node_groups = {
    default = {
      desired_capacity = 1
      min_size         = 1
      max_size         = 2
      instance_types   = ["t3.micro"]

      # CORRECT: map of name = ARN
      iam_role_additional_policies = {
        s3_read = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
      }
    }
  }
}

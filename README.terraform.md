# Event Booking EKS Cluster Setup Guide

## Prerequisites
1. AWS CLI installed and configured
2. Terraform (version 1.0.0 or later)
3. kubectl installed
4. AWS account with appropriate permissions

## Required Variables
Create a `terraform.tfvars` file with:
```hcl
aws_region     = "us-east-1"  # or your preferred region
admin_role_arn = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ADMIN_ROLE"
friend_role_arn = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_FRIEND_ROLE"
```

## Configuration Files Overview

### 1. VPC Configuration (`networking.tf`)
```hcl
# Current configuration:
- VPC CIDR: 10.0.0.0/16
- 2 Availability Zones
- Public subnets: 10.0.1.0/24, 10.0.2.0/24
- Private subnets: 10.0.3.0/24, 10.0.4.0/24
- NAT Gateway enabled
```
Update if needed:
- Change CIDR blocks if they conflict with existing VPCs
- Adjust number of AZs based on your region
- Modify subnet sizes if needed

### 2. EKS Configuration (`eks.tf`)
```hcl
# Key settings to update:
cluster_name    = "event-booking-cluster"  # Change if needed
cluster_version = "1.27"                   # Update if needed

# Update your public IP for cluster access
cluster_endpoint_public_access_cidrs = ["YOUR_PUBLIC_IP/32"]

# Node group configuration
eks_managed_node_groups = {
  default = {
    desired_capacity = 1
    min_size         = 1
    max_size         = 2
    instance_types   = ["t3.micro"]
  }
}
```

### 3. IAM Configuration (`iam.tf`)
- S3 read-only access policy is attached to node groups
- Admin and friend roles are configured for cluster access

### 4. ECR Configuration (`ecr.tf`)
- ECR repository for container images
- Review and update repository name if needed

## Deployment Steps

1. Initialize Terraform:
```bash
terraform init
```

2. Review the planned changes:
```bash
terraform plan
```

3. Apply the configuration:
```bash
terraform apply
```

4. Configure kubectl:
```bash
aws eks update-kubeconfig --name event-booking-cluster --region us-west-2
```

## Important Notes

1. **Cost Considerations**:
   - EKS cluster costs
   - NAT Gateway costs
   - ECR storage costs
   - Consider using `t3.micro` for development

2. **Security**:
   - Public endpoint restricted to your IP
   - Private endpoint enabled
   - IAM roles for admin and friend access
   - S3 read-only access for nodes

3. **Networking**:
   - VPC with public and private subnets
   - NAT Gateway for private subnet internet access
   - Proper subnet tagging for EKS

## Maintenance

1. **Regular Updates**:
   - Kubernetes version
   - Terraform provider versions
   - Node group configurations

2. **Monitoring**:
   - Node group scaling
   - ECR repository usage
   - VPC and subnet usage

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

## Troubleshooting

1. **VPC Issues**:
   - Check VPC limits in your AWS account
   - Verify CIDR block conflicts
   - Ensure proper subnet tagging

2. **EKS Issues**:
   - Verify IAM roles and policies
   - Check security group configurations
   - Ensure proper node group configuration

3. **Access Issues**:
   - Verify your public IP in `cluster_endpoint_public_access_cidrs`
   - Check IAM role configurations
   - Verify kubectl configuration

## Additional Resources

- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [Terraform EKS Module](https://registry.terraform.io/modules/terraform-aws-modules/eks/aws/latest)
- [AWS VPC Module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)

Remember to:
1. Replace placeholder values in `terraform.tfvars`
2. Update your public IP in the EKS configuration
3. Review all security settings before deployment
4. Consider costs and adjust resources accordingly

## Repository Management

### Files to NOT Push
1. **Sensitive Files**:
   - `*.tfvars` files (contain sensitive variables)
   - `terraform.tfstate` and `terraform.tfstate.backup` (contain sensitive infrastructure state)
   - Any files containing AWS credentials or secrets

2. **Local Development Files**:
   - `.terraform/` directory (contains downloaded providers)
   - `.terraform.lock.hcl` (local lock file)
   - Any local override files

3. **IDE and OS Files**:
   - `.vscode/` directory
   - `.DS_Store` (Mac)
   - `Thumbs.db` (Windows)

### Steps to Push to Repository

1. Initialize git in the terraform directory:
```bash
cd terraform
git init
```

2. Add your files:
```bash
git add .
```

3. Create initial commit:
```bash
git commit -m "Initial Terraform configuration for EKS cluster"
```

4. Add your remote repository:
```bash
git remote add origin <your-repository-url>
```

5. Push to repository:
```bash
git push -u origin main
```

### Important Security Notes
1. Never commit `terraform.tfvars` files containing sensitive data
2. Use environment variables or AWS Secrets Manager for sensitive values
3. Consider using a remote state backend (like S3) for team collaboration
4. Review the `.gitignore` file before pushing to ensure no sensitive data is included 
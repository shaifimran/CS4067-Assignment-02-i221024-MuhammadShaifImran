# Commented out since EKS cluster creation is disabled
resource "aws_iam_role_policy_attachment" "node_s3_read" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  # use the IAM role *name* from your managed node-group output:
  role = module.eks.eks_managed_node_groups["default"].iam_role_name
}

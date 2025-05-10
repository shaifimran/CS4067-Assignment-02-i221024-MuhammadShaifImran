# Required GitHub Repository Secrets

This document lists all the secrets required for the Terraform GitHub Actions workflow to run successfully.

## AWS Credentials
These are required for AWS authentication:

1. `AWS_ACCESS_KEY_ID`
   - Description: Your AWS access key ID
   - Format: `AKIAXXXXXXXXXXXXXXXX`
   - How to get it:
     1. Go to AWS Console > IAM
     2. Select your user
     3. Go to "Security credentials" tab
     4. Create new access key
     5. Copy the Access key ID

2. `AWS_SECRET_ACCESS_KEY`
   - Description: Your AWS secret access key
   - Format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - How to get it:
     1. Same as above, but copy the Secret access key
     2. Make sure to save this immediately as it won't be shown again

3. `AWS_REGION`
   - Description: AWS region where resources will be deployed
   - Format: `us-east-1` (or your preferred region)
   - Common values:
     - `us-east-1` (N. Virginia)
     - `us-west-2` (Oregon)
     - `eu-west-1` (Ireland)

## IAM Role ARNs
These are required for EKS cluster access:

1. `AWS_ADMIN_ROLE_ARN`
   - Description: ARN of the IAM role for cluster admin
   - Format: `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`
   - How to get it:
     1. Go to AWS Console > IAM
     2. Click "Roles" in the left sidebar
     3. Find your admin role
     4. Copy the ARN from role details
   - Example: `arn:aws:iam::123456789012:role/eks-admin-role`

2. `AWS_FRIEND_ROLE_ARN`
   - Description: ARN of the IAM role for your friend's access
   - Format: `arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME`
   - How to get it:
     1. Same as above, but for your friend's role
   - Example: `arn:aws:iam::123456789012:role/eks-friend-role`

## How to Add Secrets

1. Go to your GitHub repository
2. Click on "Settings"
3. In the left sidebar, click "Secrets and variables" > "Actions"
4. Click "New repository secret"
5. Enter the name and value for each secret
6. Click "Add secret"

## Security Best Practices

1. Never commit these values to your repository
2. Use the minimum required permissions for each role
3. Regularly rotate your AWS access keys
4. Use different roles for different environments (dev/prod)
5. Consider using AWS SSO for production environments

## Troubleshooting

If you get errors about missing secrets:
1. Verify all secrets are added correctly
2. Check the secret names match exactly
3. Ensure the values are correct and properly formatted
4. Check if the IAM roles have the necessary permissions

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [EKS IAM Roles](https://docs.aws.amazon.com/eks/latest/userguide/security-iam.html) 
# IAM role for EC2 instances
resource "aws_iam_role" "ec2_role" {
  name = "event-booking-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach S3 read policy to EC2 role
resource "aws_iam_role_policy_attachment" "ec2_s3_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# Create instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "event-booking-ec2-profile"
  role = aws_iam_role.ec2_role.name
}
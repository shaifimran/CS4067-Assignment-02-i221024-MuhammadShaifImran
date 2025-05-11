module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name               = "event-booking-vpc"
  cidr               = "10.0.0.0/16"
  azs                = ["${var.aws_region}a", "${var.aws_region}b"]
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets    = ["10.0.3.0/24", "10.0.4.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true

  public_subnet_tags  = { Name = "event-booking-public" }
  private_subnet_tags = { Name = "event-booking-private" }
  tags = {
    Environment = "production"
    Project     = "event-booking"
  }
}

resource "aws_launch_template" "app" {
  name_prefix   = "event-booking-"
  image_id      = "ami-0c7217cdde317cfec"
  instance_type = var.instance_type

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.app.id]
  }

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2.name
  }

  key_name = var.key_name

  tag_specifications {
    resource_type = "instance"
    tags          = { Name = "event-booking-app" }
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "event-booking-asg"
  desired_capacity    = var.desired_capacity
  max_size            = var.max_size
  min_size            = var.min_size
  vpc_zone_identifier = module.vpc.public_subnets
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  health_check_type         = "EC2"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "event-booking-app"
    propagate_at_launch = true
  }
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "app-sg" }
}

resource "aws_iam_role" "ec2" {
  name = "event-booking-ec2-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Action = "sts:AssumeRole", Effect = "Allow", Principal = { Service = "ec2.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_s3" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "event-booking-ec2-profile"
  role = aws_iam_role.ec2.name
}

resource "aws_ecr_repository" "services" {
  for_each = toset([
    "booking-service", "event-service", "notification-service", "payment-service", "user-service"
  ])
  name                 = each.key
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
}

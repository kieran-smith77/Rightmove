locals {
  ami = "ami-0fb391cce7a602d1f"
}

data "http" "myip" {
  url = "http://ifconfig.io"
}

resource "aws_security_group" "rightmove" {
  name        = "rightmove"
  description = "Allow SSH and HTTP"

  ingress {
    description = "Private SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${trimspace(data.http.myip.body)}/32", "0.0.0.0/0"]
  }

  ingress {
    description = "Private HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}

resource "aws_iam_role" "rightmove" {
  name = "rightmove_webserver"
  managed_policy_arns = [aws_iam_policy.rightmove_policy.arn]

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

}

resource "aws_iam_policy" "rightmove_policy" {
  name = "rightmove_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:HeadBucket",
          "s3:Get*",
          "s3:Put*",
          "s3:Delete*"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.code_store.arn,
          aws_s3_bucket.db_store.arn,
          "${aws_s3_bucket.code_store.arn}/*",
          "${aws_s3_bucket.db_store.arn}/*"
        ]
      },
      {
        Action = [
          "ssm:GetParameter",
          "ssm:DescribeParameters",
        ]
        Effect = "Allow"
        Resource = [
          aws_ssm_parameter.webhooks.arn,
          aws_ssm_parameter.searches.arn,
        ]
      },
            {
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
        ]
        Effect = "Allow"
        Resource = [
          "${aws_dynamodb_table.storage_table.arn}/*",
          "${aws_dynamodb_table.storage_table.arn}",
        ]
      },
    ]
  })
}

resource "aws_iam_instance_profile" "rightmove" {
  name = "rightmove_profile"
  role = "${aws_iam_role.rightmove.name}"
}

resource "aws_instance" "web_server" {
  ami                    = local.ami
  instance_type          = "t3a.nano"
  key_name               = "Rightmove"
  vpc_security_group_ids = [aws_security_group.rightmove.id]
  user_data              = file("../server_setup.sh")
  iam_instance_profile = "${aws_iam_instance_profile.rightmove.name}"
  tags = {
    Name = "RightmoveServer"
  }
}

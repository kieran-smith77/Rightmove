locals {
  db_bucket_name = "arn:aws:s3:::kieran-smith-rightmove-db"
}

resource "aws_ecr_repository" "rightmove_scraper" {
  name                 = "rightmove-scraper"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ssm_parameter" "search_url" {
  name  = "search_url"
  type  = "String"
  value = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94124&insId=1&radius=3.0&minPrice=275000&maxPrice=350000&minBedrooms=2&maxBedrooms=4&displayPropertyType=houses&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false"
}

resource "aws_iam_role" "scraper" {
  name                = "rightmove_scraper"
  assume_role_policy  = data.aws_iam_policy_document.instance_assume_role_policy.json
  managed_policy_arns = [aws_iam_policy.instance_policy.arn]

}

data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "instance_policy" {
  name = "rightmove-scraper-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:Get*", "s3:Put*"]
        Effect   = "Allow"
        Resource = local.db_bucket_name
      },
      {
        Action   = ["ssm:GetParameters"]
        Effect   = "Allow"
        Resource = aws_ssm_parameter.search_url.arn
      },
    ]
  })
}

resource "aws_ecs_task_definition" "rightmove_scraper" {
  family                   = "task_definition_name"
  task_role_arn            = "${var.ecs_task_role}"
  execution_role_arn       = "${var.ecs_task_execution_role}"
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "1024"
  requires_compatibilities = ["FARGATE"]
  container_definitions = jsonencode([
    {
      name      = "first"
      image     = "service-first"
      cpu       = 10
      memory    = 512
      essential = true
    }
  ])

  }
terraform {
  backend "s3" {
    profile        = "personal"
    bucket         = "kieran-smith-rightmove-tfstate"
    region         = "eu-west-2"
    key            = "terraform.tfstate"
    dynamodb_table = "tf-state"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region  = "eu-west-2"
  profile = "personal"
}

provider "aws" {
  alias   = "us_east_1"
  region  = "us-east-1"
  profile = "personal"
}
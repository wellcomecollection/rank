terraform {
  required_version = ">= 1.3"

  backend "s3" {
    role_arn = "arn:aws:iam::756629837203:role/catalogue-developer"

    bucket         = "wellcomecollection-catalogue-infra-delta"
    key            = "terraform/rank/rank.tfstate"
    dynamodb_table = "terraform-locktable"
    region         = "eu-west-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.13.1"
    }

    github = {
      source  = "integrations/github"
      version = ">= 6.0.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  assume_role {
    role_arn = "arn:aws:iam::756629837203:role/catalogue-developer"
  }

  default_tags {
    tags = {
      TerraformConfigurationURL = "https://github.com/wellcomecollection/rank/tree/main/infrastructure"
      Department                = "Digital Platform"
    }
  }
}


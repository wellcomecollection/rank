data "terraform_remote_state" "aws_account_infrastructure" {
  backend = "s3"

  config = {
    assume_role = {
      role_arn = "arn:aws:iam::760097843905:role/platform-read_only"
    }
    bucket = "wellcomecollection-platform-infra"
    key    = "terraform/aws-account-infrastructure/platform.tfstate"
    region = "eu-west-1"
  }
}

# Configure the GitHub Provider
# Create a fine-grained personal access token in Github:
# Go to your Github account > Settings > Developer settings > PAT > Fine-grained tokens
# Give it a name, description and a short (7 days) expiration
# In Organization permissions select Secret - Manage Actions organization secrets: read and write
# export TF_VAR_github_token=<your-token-here> before applying the tf
provider "github" {
  owner = "wellcomecollection"
  token = var.github_token
}

variable "github_token" {
  type = string
}

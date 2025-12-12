provider "aws" {
  region = "eu-west-1"

  assume_role {
    role_arn = "arn:aws:iam::756629837203:role/catalogue-developer"
  }
}

# Configure the GitHub Provider
# Create a fine-grained personal access token in Github:
# Go to your Github account > Settings > Developer settings > PAT > Fine-grained tokens
# Give it a name, description and a short (7 days) expiration
# In Organization permissions select:
#   - Secrets: Read and write (Actions secrets)
# export TF_VAR_github_token=<your-token-here> before applying the tf
provider "github" {
  owner = "wellcomecollection"
  token = var.github_token
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "github_oidc_provider_arn" {
  type        = string
  description = "ARN of the GitHub Actions OIDC provider in AWS (token.actions.githubusercontent.com)"
}

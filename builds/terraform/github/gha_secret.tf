// this is required here in the child module to ensure correct resolution

terraform {
  required_providers {
    github = {
      source = "integrations/github"
    }
  }
}

resource "github_actions_secret" "rank_ci" {
  repository      = "rank"
  secret_name     = "RANK_CI_ROLE_ARN"
  plaintext_value = module.gha_rank_ci_role.role_arn
}

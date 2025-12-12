module "gha_rank_ci_role" {
  source = "github.com/wellcomecollection/terraform-aws-gha-role?ref=v1.0.0"

  policy_document          = data.aws_iam_policy_document.gha_rank_ci.json
  github_repository        = "wellcomecollection/rank"
  role_name                = "rank-ci"
  github_oidc_provider_arn = local.github_oidc_provider_arn
}

data "aws_iam_policy_document" "gha_rank_ci" {
  statement {
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:BatchGetImage",
      "ecr:Describe*",
      "ecr:Get*",
      "ecr:List*",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
    ]

    resources = [
      "arn:aws:ecr:eu-west-1:756629837203:repository/weco/rank",
    ]
  }

  statement {
    actions = [
      "ecr:GetAuthorizationToken",
    ]

    resources = [
      "*",
    ]
  }
}

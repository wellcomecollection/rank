resource "aws_ecr_repository" "rank" {
  name = "weco/rank"

  lifecycle {
    prevent_destroy = true
  }
}

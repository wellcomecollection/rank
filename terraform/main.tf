data "ec_stack" "latest" {
  version_regex = "latest"
  region        = "us-east-1"
}


resource "ec_deployment" "rank_catalogue" {
  name                   = "rank_catalogue"
  region                 = "eu-west-1"
  version                = data.ec_stack.latest.version
  deployment_template_id = "aws-io-optimized-v2"

  elasticsearch {
    topology {
      id         = "hot_content"
      size       = "1g"
      zone_count = 1
    }
  }

  kibana {
    topology {
      size       = "1g"
      zone_count = 1
    }
  }
}

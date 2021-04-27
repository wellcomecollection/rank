data "ec_stack" "latest" {
  version_regex = "latest"
  region        = "us-east-1"
}


resource "ec_deployment" "rank_catalogue" {
  name                   = "rank_catalogue"
  region                 = "eu-west-1"
  version                = data.ec_stack.latest.version
  deployment_template_id = "aws-cross-cluster-search-v2"

  elasticsearch {
    topology {
      id         = "hot_content"
      size       = "1g"
      zone_count = 1
    }

    remote_cluster {
      deployment_id = local.catalogue_ec_cluster_id
      alias         = local.catalogue_ec_cluster_name
      ref_id        = local.catalogue_ec_cluster_ref_id
    }
  }

  kibana {
    topology {
      size       = "1g"
      zone_count = 1
    }
  }
}

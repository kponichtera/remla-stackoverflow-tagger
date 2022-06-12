data "google_project" "project" {}
data "google_client_config" "config" {}

locals {
  prometheus_values = templatefile("${path.module}/templates/values.yaml", {
    PROJECT_ID                = data.google_project.project.project_id,
    REGION                    = data.google_client_config.config.region,
    CLUSTER_NAME              = var.cluster_name
    STACKDRIVER_SIDECAR_IMAGE = var.stackdriver_sidecar_image
    STACKDRIVER_SIDECAR_TAG   = var.stackdriver_sidecar_tag
    SCRAPE_INTERVAL           = var.scrape_interval
    SCRAPE_TIMEOUT            = var.scrape_timeout
  })
}


resource "helm_release" "prometheus" {
  name       = "prometheus"
  chart      = "prometheus"
  version    = "15.10.1"
  repository = "https://prometheus-community.github.io/helm-charts"

  values = [local.prometheus_values]

  namespace        = "prometheus"
  create_namespace = true
  atomic           = true
}

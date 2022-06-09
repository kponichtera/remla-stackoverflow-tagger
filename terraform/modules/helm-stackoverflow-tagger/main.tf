locals {
  chart_values = templatefile("${path.module}/templates/values.yml", {
    STATIC_IP_NAME                   = var.ingress_static_ip_name
    HOSTNAME                         = var.ingress_host
    INGRESS_MANAGED_CERTIFICATE_NAME = var.ingress_managed_certificate_name
    INTERFACE_SERVICE_REPLICA_COUNT  = var.interface_service_replica_count
    FRONTEND_REPLICA_COUNT           = var.frontend_replica_count
  })
}

resource "helm_release" "release" {
  name         = var.name
  chart        = "stackoverflow-tagger"
  version      = var.chart_version
  repository   = "https://remla2022.github.io/stackoverflow-tagger"
  namespace    = var.namespace
  force_update = true

  values = [local.chart_values]

  # TODO: Consider changing to true if all services are able to startup immediately
  wait = false
}

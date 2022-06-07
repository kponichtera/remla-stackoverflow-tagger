resource "kubernetes_manifest" "certificate" {
  manifest = {
    apiVersion = "networking.gke.io/v1"
    kind       = "ManagedCertificate"
    metadata = {
      name : var.name
      namespace : var.namespace
    }
    spec = {
      domains : [var.domain]
    }
  }
}
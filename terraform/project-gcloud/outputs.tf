output "ingress_external_ip" {
  value = module.ingress_address.address
}

output "gke_cluster_endpoint" {
  value     = "https://${module.gke_cluster.cluster_endpoint}"
  sensitive = true
}

output "gke_cluster_ca_certificate" {
  value     = base64decode(module.gke_cluster.cluster_ca_certificate)
  sensitive = true
}

output "ingress_static_ip_name" {
  value = module.ingress_address.name
}
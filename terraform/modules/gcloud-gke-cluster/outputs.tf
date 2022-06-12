output "name" {
  value       = google_container_cluster.cluster.name
  description = "Cluster name."
}

output "cluster_endpoint" {
  value       = google_container_cluster.cluster.endpoint
  description = "Cluster endpoint."
}

output "cluster_ca_certificate" {
  value       = google_container_cluster.cluster.master_auth[0].cluster_ca_certificate
  description = "Base64 encoded public certificate that is the root of trust for the cluster."
}

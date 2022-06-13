output "ingress_external_ip" {
  value = module.ingress_address.address
}

output "gke_cluster_name" {
  value = module.gke_cluster.name
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

output "data_model_bucket_access_key" {
  value = module.data_model_bucket.access_key
  sensitive = true
}

output "data_model_bucket_secret_key" {
  value = module.data_model_bucket.secret_key
  sensitive = true
}

output "application_service_account_key" {
  value = module.application_service_account.private_key
  sensitive = true
}


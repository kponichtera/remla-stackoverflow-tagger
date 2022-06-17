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

output "ingress_external_ip" {
  value = module.ingress_address.address
}

output "ingress_static_ip_name" {
  value = module.ingress_address.name
}

# Data bucket

output "data_model_bucket_name" {
  value = module.data_model_bucket.name
}

output "data_model_bucket_access_key" {
  value     = module.data_model_bucket.access_key
  sensitive = true
}

output "data_model_bucket_secret_key" {
  value     = module.data_model_bucket.secret_key
  sensitive = true
}

# PubSub

output "pubsub_new_data_topic_name" {
  value = module.pubsub_new_data.name
}

output "pubsub_new_model_topic_name" {
  value = module.pubsub_new_model.name
}

# Application service account

output "application_service_account_key_base64" {
  value     = module.application_service_account.private_key_base64
  sensitive = true
}


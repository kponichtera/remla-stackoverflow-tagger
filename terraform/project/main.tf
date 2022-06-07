module "gcloud_services" {
  source                      = "../modules/gcloud-services"
  disable_services_on_destroy = var.disable_services_on_destroy
}

module "gke_cluster" {
  source = "../modules/gcloud-gke-cluster"
  name   = "main"

  primary_node_pool_enabled = false

  preemptible_node_pool_enabled = true
  preemptible_node_pool_size    = 2

  depends_on = [module.gcloud_services]
}

module "data_model_bucket" {
  source = "../modules/gcloud-bucket"
  name   = "data-model"
}

module "pubsub_feedback" {
  source                     = "../modules/gcloud-pubsub"
  name                       = "feedback"
  message_retention_duration = "432000s" # 5 days
}

module "pubsub_new_model" {
  source                     = "../modules/gcloud-pubsub"
  name                       = "new-model"
  message_retention_duration = "3600s" # 1 hour
}

module "ingress_address" {
  source = "../modules/gcloud-global-address"
  name   = "stackoverflow-tagger-ingress"
}

module "gke_namespace" {
  source = "../modules/gcloud-gke-namespace"
  name   = "stackoverflow-tagger"
}

module "managed_certificate" {
  source    = "../modules/gcloud-gke-managed-certificate"
  name      = "stackoverflow-tagger-cert"
  namespace = module.gke_namespace.name
  domain    = var.ingress_host
}

module "stackoverflow_tagger_helm_chart" {
  source                           = "../modules/helm-stackoverflow-tagger"
  namespace                        = module.gke_namespace.name
  ingress_static_ip_name           = module.ingress_address.name
  chart_version                    = var.chart_version
  ingress_host                     = var.ingress_host
  ingress_managed_certificate_name = module.managed_certificate.name
}
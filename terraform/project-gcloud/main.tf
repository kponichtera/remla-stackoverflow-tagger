module "gcloud_services" {
  source                      = "../modules/gcloud-services"
  disable_services_on_destroy = var.disable_services_on_destroy
}

module "gke_cluster" {
  source = "../modules/gcloud-gke-cluster"
  name   = "main"
  # TODO: Workaround to the bug with data.google_project.project_id not returning anything
  project_id = var.project_id

  primary_node_pool_enabled     = false
  preemptible_node_pool_enabled = true

  depends_on = [module.gcloud_services]
}

module "data_model_bucket" {
  source = "../modules/gcloud-bucket"
  name   = "${var.project_id}-data-model"

  depends_on = [module.gcloud_services]
}

module "pubsub_new_data" {
  source                     = "../modules/gcloud-pubsub"
  name                       = "new-data"
  message_retention_duration = "432000s" # 5 days

  depends_on = [module.gcloud_services]
}

module "pubsub_new_model" {
  source                     = "../modules/gcloud-pubsub"
  name                       = "new-model"
  message_retention_duration = "3600s" # 1 hour

  depends_on = [module.gcloud_services]
}

module "application_service_account" {
  source = "../modules/gcloud-application-service-account"
  name   = "stackoverflow-tagger-sa"

  new_data_topic_name  = module.pubsub_new_data.name
  new_model_topic_name = module.pubsub_new_model.name
}

module "ingress_address" {
  source = "../modules/gcloud-global-address"
  name   = "stackoverflow-tagger-ingress"

  depends_on = [module.gcloud_services]
}

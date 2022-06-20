# Output values from the gcloud infrastructure Terraform project
data "terraform_remote_state" "gcloud" {
  backend = "gcs"
  config = {
    bucket = "${var.project_id}-terraform"
    prefix = "gcloud"
  }
}

module "prometheus" {
  source       = "../modules/helm-prometheus"
  cluster_name = data.terraform_remote_state.gcloud.outputs.gke_cluster_name
}

module "stackoverflow_tagger_helm_chart" {
  source                           = "../modules/helm-stackoverflow-tagger"
  chart_version                    = var.chart_version
  ingress_host                     = var.ingress_host
  ingress_managed_certificate_name = module.managed_certificate.name

  gcloud_project_id                      = var.project_id
  ingress_static_ip_name                 = data.terraform_remote_state.gcloud.outputs.ingress_static_ip_name
  application_service_account_key_base64 = data.terraform_remote_state.gcloud.outputs.application_service_account_key_base64

  data_model_bucket_name       = data.terraform_remote_state.gcloud.outputs.data_model_bucket_name
  data_model_bucket_access_key = data.terraform_remote_state.gcloud.outputs.data_model_bucket_access_key
  data_model_bucket_secret_key = data.terraform_remote_state.gcloud.outputs.data_model_bucket_secret_key

  pubsub_new_data_topic_name  = data.terraform_remote_state.gcloud.outputs.pubsub_new_data_topic_name
  pubsub_new_model_topic_name = data.terraform_remote_state.gcloud.outputs.pubsub_new_model_topic_name

  learning_message_threshold = var.learning_message_threshold
}

module "managed_certificate" {
  source = "../modules/gcloud-gke-managed-certificate"
  name   = "stackoverflow-tagger-cert"
  domain = var.ingress_host
}


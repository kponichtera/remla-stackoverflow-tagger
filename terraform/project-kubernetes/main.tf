# Output values from the gcloud infrastructure Terraform project
data "terraform_remote_state" "gcloud" {
  backend = "gcs"
  config = {
    bucket = "${var.project_id}-terraform"
    prefix = "gcloud"
  }
}

module "stackoverflow_tagger_helm_chart" {
  source                           = "../modules/helm-stackoverflow-tagger"
  ingress_static_ip_name           = data.terraform_remote_state.gcloud.outputs.ingress_static_ip_name
  chart_version                    = var.chart_version
  ingress_host                     = var.ingress_host
  ingress_managed_certificate_name = module.managed_certificate.name
}

module "managed_certificate" {
  source    = "../modules/gcloud-gke-managed-certificate"
  name      = "stackoverflow-tagger-cert"
  domain    = var.ingress_host
}


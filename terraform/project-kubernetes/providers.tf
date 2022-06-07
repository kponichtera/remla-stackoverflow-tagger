data "google_client_config" "gcloud_config" {}

provider "kubernetes" {
  host                   = data.terraform_remote_state.gcloud.outputs.gke_cluster_endpoint
  token                  = data.google_client_config.gcloud_config.access_token
  cluster_ca_certificate = data.terraform_remote_state.gcloud.outputs.gke_cluster_ca_certificate
}

provider "helm" {
  kubernetes {
    host                   = data.terraform_remote_state.gcloud.outputs.gke_cluster_endpoint
    token                  = data.google_client_config.gcloud_config.access_token
    cluster_ca_certificate = data.terraform_remote_state.gcloud.outputs.gke_cluster_ca_certificate
  }
}

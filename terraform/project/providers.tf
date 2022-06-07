data "google_client_config" "gcloud_config" {}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "kubernetes" {
  host                   = "https://${module.gke_cluster.cluster_endpoint}"
  token                  = data.google_client_config.gcloud_config.access_token
  cluster_ca_certificate = base64decode(module.gke_cluster.cluster_ca_certificate)
}

provider "helm" {
  kubernetes {
    host                   = "https://${module.gke_cluster.cluster_endpoint}"
    token                  = data.google_client_config.gcloud_config.access_token
    cluster_ca_certificate = base64decode(module.gke_cluster.cluster_ca_certificate)
  }
}

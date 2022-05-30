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
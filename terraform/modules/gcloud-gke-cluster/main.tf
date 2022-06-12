data "google_project" "project" {}
data "google_client_config" "config" {}
data "google_container_engine_versions" "gke_versions" {
  location = local.zone
}

locals {
  zone = data.google_client_config.config.zone
}

resource "google_service_account" "cluster_account" {
  account_id   = "${var.name}-cluster-service-account"
  display_name = "${var.name} cluster service account"
}

resource "google_container_cluster" "cluster" {
  name               = "${var.name}-cluster"
  min_master_version = data.google_container_engine_versions.gke_versions.release_channel_default_version["STABLE"]
  location           = local.zone

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  vertical_pod_autoscaling {
    enabled = true
  }

  maintenance_policy {
    daily_maintenance_window {
      start_time = "05:00"
    }
  }

  lifecycle {
    ignore_changes = [min_master_version]
  }
}

# TODO: Remove after managed Prometheus toggle is implemented in google_container_cluster
module "cluster_enable_managed_prometheus" {
  source  = "terraform-google-modules/gcloud/google"
  version = "3.1.1"

  skip_download = true
  additional_components    = ["beta"]
  service_account_key_file = "${path.root}/../terraform-credentials.json"

  create_cmd_entrypoint = "gcloud"
  create_cmd_body       = "beta container clusters update ${google_container_cluster.cluster.name} --enable-managed-prometheus"
}

resource "google_container_node_pool" "primary" {
  count   = var.primary_node_pool_enabled ? 1 : 0
  version = data.google_container_engine_versions.gke_versions.release_channel_default_version["STABLE"]
  name    = "primary-pool"

  cluster    = google_container_cluster.cluster.name
  location   = local.zone
  node_count = var.primary_node_pool_size

  management {
    auto_repair  = true
    auto_upgrade = false
  }

  node_config {
    preemptible     = false
    machine_type    = var.primary_node_pool_machine_type
    disk_size_gb    = var.primary_node_pool_disk_size_gb
    disk_type       = "pd-ssd"
    service_account = google_service_account.cluster_account.email
  }

  lifecycle {
    ignore_changes = [version]
  }
}

resource "google_container_node_pool" "preemptible" {
  count   = var.preemptible_node_pool_enabled ? 1 : 0
  version = data.google_container_engine_versions.gke_versions.release_channel_default_version["STABLE"]
  name    = "preemptible-pool"

  cluster    = google_container_cluster.cluster.name
  location   = local.zone
  node_count = var.preemptible_node_pool_size

  management {
    auto_repair  = true
    auto_upgrade = false
  }

  node_config {
    preemptible     = true
    machine_type    = var.preemptible_node_pool_machine_type
    disk_size_gb    = var.preemptible_node_pool_disk_size_gb
    disk_type       = "pd-ssd"
    service_account = google_service_account.cluster_account.email
  }

  lifecycle {
    ignore_changes = [version]
  }
}

data "google_project" "project" {}
data "google_client_config" "config" {}
data "google_container_engine_versions" "gke_versions" {
  location = local.zone
}

locals {
  zone         = data.google_client_config.config.zone
  cluster_name = "${var.name}-cluster"

  service_account_roles = [
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/stackdriver.resourceMetadata.writer"
  ]
}

resource "google_service_account" "cluster_account" {
  account_id   = "${local.cluster_name}-service-account"
  display_name = "${local.cluster_name} GKE service account"
}

resource "google_project_iam_member" "service_account_roles" {
  for_each = toset(local.service_account_roles)

  project = data.google_project.project.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cluster_account.email}"
}

resource "google_container_cluster" "cluster" {
  name               = local.cluster_name
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

data "google_project" "project" {}
data "google_client_config" "config" {}

locals {
  project_name = data.google_project.project.project_id
  region       = data.google_client_config.config.region
  bucket_name  = "${local.project_name}-${var.name}"
}

resource "google_storage_bucket" "bucket" {
  name                        = local.bucket_name
  location                    = local.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# Service account with read/write permissions to the bucket
resource "google_service_account" "service_account" {
  account_id   = "${local.bucket_name}-sa"
  display_name = "${local.bucket_name} bucket service account"
}

resource "google_storage_bucket_iam_member" "service_account_member" {
  bucket = google_storage_bucket.bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.service_account.email}"
}

# HMAC key
resource "google_storage_hmac_key" "key" {
  service_account_email = google_service_account.service_account.email
}

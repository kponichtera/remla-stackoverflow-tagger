data "google_client_config" "config" {}

resource "google_service_account" "service_account" {
  account_id   = var.name
  display_name = "${var.name} application service account"
}

resource "google_project_iam_member" "service_account_roles" {
  project = data.google_client_config.config.project
  role    = "roles/pubsub.editor"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_pubsub_topic_iam_member" "new_data_topic_member" {
  topic  = var.new_data_topic_name
  role   = "roles/pubsub.editor"
  member = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_pubsub_topic_iam_member" "new_model_topic_name" {
  topic  = var.new_model_topic_name
  role   = "roles/pubsub.editor"
  member = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_key" "key" {
  service_account_id = google_service_account.service_account.id
}
terraform {
  required_version = "~> 1.2.0"

  required_providers {
    google = "~> 4.24.0"
    null   = "~> 3.1.1"
  }

  backend "gcs" {
    prefix = "gcloud"
  }
}
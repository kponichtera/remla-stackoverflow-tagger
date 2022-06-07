terraform {
  required_version = "~> 1.2.0"

  required_providers {
    google      = "~> 4.24.0"
    kubernetes  = "~> 2.11.0"
    helm        = "~> 2.5.1"
  }

  backend "gcs" {
    prefix = "state"
  }
}
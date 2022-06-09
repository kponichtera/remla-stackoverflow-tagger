resource "google_project_service" "cloudresourcemanager" {
  service                    = "cloudresourcemanager.googleapis.com"
  disable_on_destroy         = var.disable_services_on_destroy
  disable_dependent_services = var.disable_services_on_destroy
}

resource "google_project_service" "dns" {
  service                    = "dns.googleapis.com"
  disable_on_destroy         = var.disable_services_on_destroy
  disable_dependent_services = var.disable_services_on_destroy
}

resource "google_project_service" "compute" {
  service                    = "compute.googleapis.com"
  disable_on_destroy         = var.disable_services_on_destroy
  disable_dependent_services = var.disable_services_on_destroy
}

resource "google_project_service" "container" {
  service                    = "container.googleapis.com"
  disable_on_destroy         = var.disable_services_on_destroy
  disable_dependent_services = var.disable_services_on_destroy
}
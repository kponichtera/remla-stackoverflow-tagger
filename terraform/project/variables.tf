// Set by Task
variable "project_id" {}
variable "region" {}
variable "zone" {}

variable "disable_services_on_destroy" {
  default = false
}

variable "ingress_host" {
  default = "mock-hostname.local"
}

variable "chart_version" {
  default = ""
}
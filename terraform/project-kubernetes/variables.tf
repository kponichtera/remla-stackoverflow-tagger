// Set by Task
variable "project_id" {}
variable "region" {}
variable "zone" {}

variable "ingress_host" {
  default = "mock-hostname.local"
}

variable "chart_version" {
  default = ""
}
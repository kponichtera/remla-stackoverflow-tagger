variable "name" {
  default = "stackoverflow-tagger"
}

variable "namespace" {
  default = "stackoverflow-tagger"
}

variable "chart_version" {
  description = "If not provided then the latest version will be installed"
  default     = ""
}

variable "ingress_static_ip_name" {
}

variable "ingress_host" {
}

variable "ingress_managed_certificate_name" {
}

variable "interface_service_replica_count" {
  default = "3"
}

variable "frontend_replica_count" {
  default = "3"
}
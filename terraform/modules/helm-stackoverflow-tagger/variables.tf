variable "name" {
  default = "stackoverflow-tagger"
}

variable "namespace" {
  default = "default"
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

variable "gcloud_project_id" {
}

variable "application_service_account_key_base64" {
}

variable "data_model_bucket_name" {
}

variable "data_model_bucket_access_key" {
}

variable "data_model_bucket_secret_key" {
}

variable "pubsub_new_data_topic_name" {
}

variable "pubsub_new_model_topic_name" {
}

variable "learning_message_threshold" {
}


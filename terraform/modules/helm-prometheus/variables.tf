variable "cluster_name" {
  description = "GKE cluster name on which the Prometheus is meant to be deployed."
}

// Stackdriver Docker image

variable "stackdriver_sidecar_image" {
  description = "Google's Stackdriver Prometheus sidecar Docker image name."
  default     = "gcr.io/stackdriver-prometheus/stackdriver-prometheus-sidecar"
}

variable "stackdriver_sidecar_tag" {
  description = "Tag of the Google's Stackdriver Prometheus sidecar Docker image."
  default     = "0.10.1"
}

// Prometheus configuration

variable "scrape_interval" {
  description = "How often Prometheus is meant to scrape the endpoints."
  default     = "30s"
}

variable "scrape_timeout" {
  description = "How long is Prometheus meant to wait for response when scraping"
  default     = "10s"
}

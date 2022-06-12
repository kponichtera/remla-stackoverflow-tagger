variable "name" {
  description = "Name of the cluster"
}

variable "primary_node_pool_enabled" {
  default     = true
  description = "If true then a default (non-preemptible) node pool will be created."
}

variable "primary_node_pool_size" {
  default     = 3
  description = "The minimum number of nodes in the primary node pool."
}

variable "primary_node_pool_machine_type" {
  default     = "e2-small"
  description = "The machine type for nodes in the primary node pool."
}

variable "primary_node_pool_disk_size_gb" {
  default     = 50
  description = "The disk size for nodes in the cluster primary node pool."
}

variable "preemptible_node_pool_enabled" {
  default     = false
  description = "If true then a dedicated, preemptible node pool will be created."
}

variable "preemptible_node_pool_size" {
  default     = 3
  description = "The minimum number of nodes in the preemptible node pool."
}

variable "preemptible_node_pool_machine_type" {
  default     = "e2-small"
  description = "The machine type for nodes in the preemptible node pool."
}

variable "preemptible_node_pool_disk_size_gb" {
  default     = 50
  description = "The disk size for nodes in the cluster preemptible node pool."
}
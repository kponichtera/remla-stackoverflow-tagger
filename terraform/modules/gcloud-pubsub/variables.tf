variable "name" {}

variable "message_retention_duration" {
  description = "For how long the messages are going to be queued."
  # 24 hours
  default = "86400s"
}
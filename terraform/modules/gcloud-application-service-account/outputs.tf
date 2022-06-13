output "private_key" {
  value       = google_service_account_key.key.private_key
  description = "Private key of the application service account."
}
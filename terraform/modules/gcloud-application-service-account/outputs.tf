output "private_key_base64" {
  value       = google_service_account_key.key.private_key
  description = "Base64-encoded private key of the application service account."
}
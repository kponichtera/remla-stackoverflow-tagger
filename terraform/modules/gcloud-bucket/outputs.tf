output "id" {
  value       = google_storage_bucket.bucket.id
  description = "The ID of created bucket"
}

output "self_link" {
  value       = google_storage_bucket.bucket.self_link
  description = "The URI of created bucket"
}

output "url" {
  value       = google_storage_bucket.bucket.url
  description = "The URL of created bucket"
}

output "hmac_access_id" {
  value       = google_storage_hmac_key.key.access_id
  description = "HMAC access key of the bucket's service account"
}

output "hmac_secret" {
  value       = google_storage_hmac_key.key.secret
  description = "HMAC secret of the bucket's service account"
}

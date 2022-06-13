output "id" {
  value       = google_storage_bucket.bucket.id
  description = "The ID of created bucket"
}

output "name" {
  value       = google_storage_bucket.bucket.name
  description = "The name of created bucket"
}

output "self_link" {
  value       = google_storage_bucket.bucket.self_link
  description = "The URI of created bucket"
}

output "url" {
  value       = google_storage_bucket.bucket.url
  description = "The URL of created bucket"
}

output "access_key" {
  value       = google_storage_hmac_key.key.access_id
  description = "HMAC access key of the bucket's service account"
}

output "secret_key" {
  value       = google_storage_hmac_key.key.secret
  description = "HMAC secret of the bucket's service account"
}

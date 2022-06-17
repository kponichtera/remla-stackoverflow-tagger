locals {
  application_service_account_key_secret_name = "${var.name}-app-sa"

  chart_values = templatefile("${path.module}/templates/values.yml", {
    GCLOUD_PROJECT_ID                      = var.gcloud_project_id
    STATIC_IP_NAME                         = var.ingress_static_ip_name
    HOSTNAME                               = var.ingress_host
    INGRESS_MANAGED_CERTIFICATE_NAME       = var.ingress_managed_certificate_name
    INTERFACE_SERVICE_REPLICA_COUNT        = var.interface_service_replica_count
    FRONTEND_REPLICA_COUNT                 = var.frontend_replica_count
    DATA_MODEL_BUCKET_NAME                 = var.data_model_bucket_name
    DATA_MODEL_BUCKET_ACCESS_KEY           = var.data_model_bucket_access_key
    DATA_MODEL_BUCKET_SECRET_KEY           = var.data_model_bucket_secret_key
    APPLICATION_SERVICE_ACCOUNT_KEY_SECRET = local.application_service_account_key_secret_name
    PUBSUB_NEW_DATA_TOPIC_NAME             = var.pubsub_new_data_topic_name
    PUBSUB_NEW_MODEL_TOPIC_NAME            = var.pubsub_new_model_topic_name
  })
}

resource "kubernetes_secret" "application_service_account_key" {
  metadata {
    name = local.application_service_account_key_secret_name
  }
  data = {
    "sa.json" = base64decode(var.application_service_account_key_base64)
  }
}

resource "helm_release" "release" {
  name         = var.name
  chart        = "stackoverflow-tagger"
  version      = var.chart_version
  repository   = "https://remla2022.github.io/stackoverflow-tagger"
  namespace    = var.namespace
  force_update = true
  atomic       = true

  values = [local.chart_values]

  depends_on = [kubernetes_secret.application_service_account_key]
}

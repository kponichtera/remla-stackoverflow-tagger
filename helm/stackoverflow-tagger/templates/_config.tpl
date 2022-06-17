{{- define "stackoverflow-tagger.config.pubsub" -}}
REMLA_PUBSUB_PROJECT_ID: {{ .Values.config.pubsub.projectId | quote }}
REMLA_PUBSUB_DATA_TOPIC_ID: {{ .Values.config.pubsub.dataTopicId | quote }}
REMLA_PUBSUB_MODEL_TOPIC_ID: {{ .Values.config.pubsub.modelTopicId | quote }}
REMLA_PUBSUB_SUBSCRIPTION_ID: {{ .Values.config.pubsub.dataSubscriptionId | quote }}
{{- end }}

{{- define "stackoverflow-tagger.config.objectStorage" -}}
REMLA_OBJECT_STORAGE_ENDPOINT: {{ .Values.config.objectStorage.endpoint | quote }}
REMLA_OBJECT_STORAGE_TLS: {{ .Values.config.objectStorage.tls | quote }}
REMLA_BUCKET_NAME: {{ .Values.config.objectStorage.bucketName | quote }}
REMLA_MODEL_OBJECT_KEY: {{ .Values.config.objectStorage.modelObjectKey | quote }}
{{- end }}

{{- define "stackoverflow-tagger.config.objectStorage.credentials" -}}
REMLA_OBJECT_STORAGE_ACCESS_KEY: {{ .Values.config.objectStorage.accessKey | quote }}
REMLA_OBJECT_STORAGE_SECRET_KEY: {{ .Values.config.objectStorage.secretKey | quote }}
{{- end }}

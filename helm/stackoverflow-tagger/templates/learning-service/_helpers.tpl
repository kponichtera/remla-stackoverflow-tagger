{{/*
Expand the name of the chart.
*/}}
{{- define "stackoverflow-tagger.learningService.fullname" -}}
{{- printf "%s-learning-service" (include "stackoverflow-tagger.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "stackoverflow-tagger.learningService.selectorLabels" -}}
{{ include "stackoverflow-tagger.selectorLabels" . }}
stackoverflow-tagger/service: learning
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "stackoverflow-tagger.learningService.serviceAccountName" -}}
{{- if .Values.learningService.serviceAccount.create }}
{{- default (include "stackoverflow-tagger.learningService.fullname" .) .Values.learningService.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.learningService.serviceAccount.name }}
{{- end }}
{{- end }}
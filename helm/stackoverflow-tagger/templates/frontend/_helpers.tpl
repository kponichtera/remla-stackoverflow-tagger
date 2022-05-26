{{/*
Expand the name of the chart.
*/}}
{{- define "stackoverflow-tagger.frontend.fullname" -}}
{{- printf "%s-frontend" (include "stackoverflow-tagger.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "stackoverflow-tagger.frontend.selectorLabels" -}}
{{ include "stackoverflow-tagger.selectorLabels" . }}
stackoverflow-tagger/service: frontend
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "stackoverflow-tagger.frontend.serviceAccountName" -}}
{{- if .Values.frontend.serviceAccount.create }}
{{- default (include "stackoverflow-tagger.frontend.fullname" .) .Values.frontend.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.frontend.serviceAccount.name }}
{{- end }}
{{- end }}

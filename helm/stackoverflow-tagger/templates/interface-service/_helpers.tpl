{{/*
Expand the name of the chart.
*/}}
{{- define "stackoverflow-tagger.interfaceService.fullname" -}}
{{- printf "%s-interface-service" (include "stackoverflow-tagger.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "stackoverflow-tagger.interfaceService.selectorLabels" -}}
{{ include "stackoverflow-tagger.selectorLabels" . }}
stackoverflow-tagger/service: interface
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "stackoverflow-tagger.interfaceService.serviceAccountName" -}}
{{- if .Values.interfaceService.serviceAccount.create }}
{{- default (include "stackoverflow-tagger.interfaceService.fullname" .) .Values.interfaceService.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.interfaceService.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
ConfigMap name.
*/}}
{{- define "stackoverflow-tagger.interfaceService.configMap" -}}
{{- printf "%s-config" (include "stackoverflow-tagger.interfaceService.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

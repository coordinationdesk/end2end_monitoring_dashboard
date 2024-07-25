{{/*
Expand the name of the chart.
*/}}
{{- define "skedler.name" -}}
{{- default "skedler" .Values.skedler.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "skedler.fullname" -}}
{{- if .Values.skedler.fullnameOverride -}}
{{- .Values.skedler.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default "skedler" .Values.skedler.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "skedler.labels" -}}
helm.sh/chart: {{ include "maas-cds.chart" . }}
{{ include "skedler.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "skedler.selectorLabels" -}}
app.kubernetes.io/name: {{ include "skedler.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

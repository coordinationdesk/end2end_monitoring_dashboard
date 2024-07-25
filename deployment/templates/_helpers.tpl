{{/*
Expand the name of the chart.
*/}}
{{- define "maas-cds.name" -}}
{{- coalesce .componentOverrideName .Values.nameOverride .Chart.Name| trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "maas-cds.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := coalesce .componentOverrideName  .Values.nameOverride .Chart.Name  }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "maas-cds.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "maas-cds.labels" -}}
helm.sh/chart: {{ include "maas-cds.chart" . }}
{{ include "maas-cds.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "maas-cds.selectorLabels" -}}
app.kubernetes.io/name: {{ include "maas-cds.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "maas-cds.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "maas-cds.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "maas.esurl" -}}
{{- if .Values.global.elasticsearch.externalUrl -}}
{{- .Values.global.elasticsearch.externalUrl }}
{{- else -}}
{{ .Values.maas.elasticsearch.ingress.protocol | lower }}://{{ .Release.Name }}-opendistro-es-client-service.{{ .Release.Namespace }}:9200
{{- end }}
{{- end }}

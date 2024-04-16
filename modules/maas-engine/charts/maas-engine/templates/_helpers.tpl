{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
Note in mulitdeployment deployment should have a name to be deployed so namme override mechanism is no more needed.
Name is <release name>-<deployment name> 
if no release name is setted:
Name is <chart name>-<deployment name> 
*/}}
{{- define "maas-engine.fullname" -}}
{{- if and .Release.Name (ne .Release.Name "release-name") }}
{{- printf "%s-%s" .Release.Name .deploymentName | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Chart.Name .deploymentName | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "maas-engine.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "maas-engine.labels" -}}
helm.sh/chart: {{ include "maas-engine.chart" . }}
{{ include "maas-engine.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "maas-engine.selectorLabels" -}}
app.kubernetes.io/name: {{ include "maas-engine.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the config map to use
*/}}
{{- define "maas-engine.configMapName" -}}
{{- default (printf "%s-%s" (include "maas-engine.fullname" .) "cfg") .Values.configMap.name }}
{{- end }}

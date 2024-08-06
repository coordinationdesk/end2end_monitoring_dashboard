# Cluster Monitoring (to move in general doc)

## Open cluster monitoring grafana client

To acces cluster monitoring tool (Grafana): 

- Port forwarding : Grafana Monitoring service named "cds-prd-mon-grafana" in name space "monitoring" on port 80.

```kubectl port-forward -n monitoring service/cds-prd-mon-grafana 3000:80```

- Acces to service on http://localhost:3000/login credentials are in keepass.

## Checks maas cots state

### Elastic

Check the Cluster health status and charge:

http://localhost:3000/d/od-f5Ujnk/elasticsearch?orgId=1

### Rabitmq

Check the number of messages and their progress:

http://localhost:3000/d/Kn5xm-gZk/rabbitmq-overview?orgId=1&refresh=15s

A curve of message number in saw shape, is a good sign (messages are consumed).

Known risk indicators:
- more than 10000 messages.
- the message curve increases sharply.

Identify the queue that overflow:

http://localhost:3000/d/j9t8vwH7k/rabbitmq-queue?orgId=1

### Snapshots volume

http://localhost:3000/d/919b92a8e8041bd567af9edab12c840c/kubernetes-persistent-volumes?var-datasource=default&var-cluster=&var-namespace=esa-csc-prd-cce-omcs-db&var-volume=pvc-es-snapshots-nfs

### Nodes (root disks)

Check nodes status (disk and more):

http://localhost:3000/d/rYdddlPWk/node-exporter-full


## Check Maas components state

To check maas components status get logs in loki.

Check the errors for collectors and engines.

http://localhost:3000/d/liz0yRCZz/loki-dashboard-quick-search?orgId=1

Select the right **namespace** (*-etl) and **search** 'ERROR' then 'WARNING'

You could find some errors like collect errors or conflicts between consolidation engines. The most important to check is if they are cyclics and blocking the collect and or consolidation processes.


# MaaS Architecture

## Introduction

MaaS for Monitoring As A Service is a framework create by us, aim for generic data flow: Collect -> Extract -> Transform -> Display

## Component Diagram

Main MaaS components are:

- maas-collector: Collect any data from anywhere
- maas-engine: Generic message consumption flows
- maas-model: Some specific class that allow us to manipulate database object (if you want to modify the database, this is where most of the work will be done)

- maas-cds: on top off maas-engine, the system's computing core

Main MaaS COTS are:

- RabbitMQ
- Grafana
- OpenSearchDSL (the package is probably compatible with elasticsearch modulo some adjustments)

![Component Interaction][maas-synthetic]

[maas-synthetic]: assets/maas-synthetic.png "MaaS Componenet Interaction"

Disclaimer: This documentation presents the various components and the interactions between them.  
Each component has its own documentation (how to use, configuration, deployment, etc).

## Storytime

They all start with the need to collect data, for which a component called maas-collector is responsible. It is pre-developed to interface with different systems such as Odata, sftp and many others.  
The purpose of the collector is to retrieve data and store it in a database.  
You can easily add a new interface via configuration, and for “specific” cases you can also create custom collectors.  

Data collected and stored in the database, a message containing the newly stored data ids is sent (according to its configuration) to the correct routing key in the collect-exchange.  
Once the data is in the database we want to apply a first processing on it. This mechanic is possible thanks to the maas-engine overloaded by the maas-cds business logic.  

An engine is a component used to apply a process, and can be thought of as a function that applies a process to all the elements contained in a message.  
Engines are identified by an ENGINE_ID, engine are also quite specific to the business, but there are common engine structures in maas-engine. Businness engines on the other hand, are in maas-cds.
Engine are rabbit consumer, deploying an engine pool with a certain configuration will allow you to specify which queue requires which processing (for a given routing key, which engine(s) I need to execute).
If several routing keys are assigned to a pool, a round robin is performed on engine configurations are also configurable, such as whether or not to send database reports on the bus.

Then it is possible to chain other engines by consuming those emitted by another engine or a collector.

Some engine parameters are also configurable, such as whether or not to send database reports on the bus.

The database storage action will generate a report, based on which a message will be sent to the associated rabbit queue.
With this mechanism it is possible to extend the actions on each message. Through new engines on a queue.

Thanks of Grafana vizualisations tools we are able to show data that was process by our engines.
Grafana also allows you to use many datasources other than OpenSearch

## Technical Note

### Topology Strategy

- This makes it possible to increase the amount of consummers for certain routing keys.
- In the event of problems, this also allows you to stop certain consumer pools without completely shutting down the system.
- Depending on the engines' internal processing, scaling may not be a good idea and can lead to database conflicts.

### Engine responsability

- It would be possible to put them all in one engine, just as it would be possible to put each instruction in a single engine. Optimal performance is in the middle, experience allowed us to understand that batch processing was also more efficient than atomic processing. 
- The execution of an engine must be done like a micro services: Engine are state less, Engine execution must be fast (less than 30s).
- If the engine fail to process an messges, the message is not acknowledged, making it available in the queue

### Collector Key features

- Collection is self-orchestrated by a database log
- If production (on a single interface) exceeds the nominal collection speed, an orchestrator can be used.
- Backup of data is supported and allow us to made replay with them, and also investigate

### Grafana

- We use a postresql database to store Grafana content (like users, and some test dashboards)
- Dashboard and datasources are provisionnied in read only

### Deployment

- All components are containerized
- The system can be deploy on docker compose, or on kubernetes or barebone of course

## Technical Dashboard Applicable Diagram

### Detailled data flow from collect to engine

![Collect Topology And Engine][collect-topology]

[collect-topology]: assets/collect-topology.png "Collect topology"

### MaaS Class

![MaaS Python Class][maas-python-class]

[maas-python-class]: assets/maas-python-class.png "MaaS Python Class"

### Processing Chain Draw

![Processing Chain Draw][processing-chain-abstract]

[processing-chain-abstract]: assets/processing-chain-abstract.png "Processing Chain Abstract"


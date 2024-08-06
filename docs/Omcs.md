# Omcs 

This section describes how to acces to omcs monitoring tool.

Omcs monitoring tool is based on Grafana.

It provides specifics dashboards to monitor Copernicus Sentinel productions.

## Login

In your web browser go to Omcs url : https://omcs.copernicus.eu/grafana.

![Omcs loging page](../assets/omcs_loging.png)

Use your credentials to connect.

## OMCS home page

You are now connected to the OMCS home page:

![Omcs home page](../assets/omcs_home.png)

You can find in this page some sections like Home link, Breadcrumb, Menu ...

![Omcs home page](../assets/omcs_home_explained.png)

- ![](../assets/grafana_icon.png)Home link, to go to omcs home page (visible on all omcs pages)
- ![](../assets/search_tool.png)Global search bar, providing links to graphana resources like dashboard, help, ... 
- ![](../assets/help.png)Grafana help link.
- ![](../assets/news.png)Grafana news link.
- ![](../assets/user.png)User menu link.
- ![](../assets/menu.png)Menu buton, display Grafana menu.
- Bread crum bar.
- Release informations (release date, version).
- Omcs dashboards menu, links to main topics dashboards lists.
- Omcs dashboards list, list of omcs dashboards in the selected topics.
- Majors indicators, displayin status on severals items.

## Menu

The menu provider is the Grafana standard menu.

![Omcs menu](../assets/omcs_menu.png)

It provides services to:

- Find dashboards:
  - Stared display the list of bookmarked dashboards.
  - Browse dashboards display a page displaying dashboard arborescence.
- Alerting:
  - Configuration of alerts.
  
## Dashboards

### Omcs dashboards organisation

Omcs Dashboards are organized on topics:

- Acquisition, provides information about sentinels mission acquisitions pass, plan, ...
- Completeness, provides information about sentinels mission products completenesses, ...
- Timeliness, provides information about sentinels mission products timelinesses ...
- Volumes_Count, provides information about sentinels mission production volumes, ...
- System Technical budget, provides information about sentinels mission STB, ...
- Unavailability, provides information about sentinels mission satellites availability, ...
- Anomalies, provides information about anomalies Cams issues and their links to production,...
- Monitoring, provides Interface monitoring information about sentinels mission monitored interfaces status, ...

Details are provided chapter **OMCS Dashboard Description**.

### Omcs dashboards usage

The figure below presents an Omcs dashboard:

![Omcs dashboard](../assets/dashboard_usage.png)

Omcs dashboards presents generally some tools bars, filters selectors, the Grafana time selector, dashboard description.

From top to bottom:
- Top search bar, allow grafana navigation, link to home page, global search selector, grafana help and news links and user menu link.
- The breadcrum (for navigation) and the time selector.
- The filter bar list the specifics filters (designed for the dashboard sepecificaly) and in severals cases the Ad-Hock filter.
- The Dashboard description panel (colapsed by default).
- The Dashboard specifics panels.

The figure below presents the same Omcs dashboard explained:

![Omcs dashboard explained](../assets/dashboard_usage_explained.png)

## Dashboards Panels and Datasources

This section present a quick description of the datasources used in dashboards panels,  a complete description is disponible on the [grafana web site](https://grafana.com/docs/grafana/latest/datasources/) .

Data sources are the data providers of the panels, in omcs context they are generaly elasticsearch datasource pointing to omcs elasticsearch indices.
Theses datasources are filtered on time and on specifics filters using varriables in queries.
Theses filterings variables could be set using Time and Filter selectors. 
## Time selector usage

This section present a quick description of the time selector, a complete description is disponible on the [grafana web site](https://grafana.com/docs/grafana/latest/dashboards/use-dashboards/#set-dashboard-time-range) .

Datasources have a time reference field, times selection filter the queries on this time field.
It provides samrts function to select time range, time zoom and refreshing dashboard on time changes.

![Time selector](../assets/time_selection.png)

Clicking on Time seletion part will display an avanced tool to set time range.

![Time selector tools](../assets/time_selection_expended.png)

## Filters selector usage

This section presents a quick description of the filter selector, a complete description is disponible on the [grafana web site](https://grafana.com/docs/grafana/latest/dashboards/variables/) .

The figure below presents a Filters selector bar, in this case there is a set of filters (that could be linked to others) and the Ad-Hoc filter .

![Filters selector bar](../assets/grafana_filter_bar.png)
### Specifics filters usage.

Use the drop down box to select values filtereds.

Drop down box:

![](../assets/grafana_filter_conf_0.png)

Drop down box selected:

![](../assets/grafana_filter_conf_1.png)

Expresion filter:

![](../assets/grafana_filter_conf_2.png)

Multiples selection:

![](../assets/grafana_filter_conf_3.png)

Specifics filters could be chained, ie some filterings selection could reduce the set of values disponibles in others selectors.
In this exemple the list of ***Product types*** displayed depends on selected ***Product Level***,***Satellite*** and ***Mission*** .

![](../assets/grafana_filter_conf_chained_1.png)

![](../assets/grafana_filter_conf_chained_1.png)

![](../assets/grafana_filter_conf_chained_2.png)

### Ad-hoc filter usage. 

This filter is a generic filter, its impacts all the panels queries of the active dashboard it allow complex filtering on the queries results.
You  cans set a serie of Ad-Hoc filters by clicking on the + sign. 

Add Ad-Hoc filter:

![](../assets/grafana_filter_ad_hoc_conf_0.png)

Allow selection of query results fields:

![](../assets/grafana_filter_ad_hoc_conf_1.png)

Allow selection of opperators:

![](../assets/grafana_filter_ad_hoc_conf_2.png)

Allow set of selecteds values:

![](../assets/grafana_filter_ad_hoc_conf_3.png)

Ad-Hoc filter setted:

![](../assets/grafana_filter_ad_hoc_conf_4.png)

FROM grafana/grafana:11.3.0

COPY ./dashboard.json /var/lib/grafana/dashboards/

COPY ./dashboard.yaml /etc/grafana/provisioning/dashboards/

COPY ./datasources.yaml /etc/grafana/provisioning/datasources/

COPY ./grafana.ini /etc/grafana/

RUN grafana-cli plugins install volkovlabs-variable-panel

FROM grafana/grafana:11.2.2-security-01-ubuntu

COPY ./dashboard.json /var/lib/grafana/dashboards/

COPY ./dashboard.yaml /etc/grafana/provisioning/dashboards/

COPY ./datasources.yaml /etc/grafana/provisioning/datasources/

COPY ./grafana.ini /etc/grafana/

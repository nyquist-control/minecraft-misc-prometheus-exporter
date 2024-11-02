import time

import prometheus_client


# Disable default metrics
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


if __name__ == '__main__':
    # Start up the server to expose the metrics
    prometheus_client.start_http_server(8000)

    while True:
        time.sleep(20)

"""record one illustrative request, without starting a metrics server."""
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest


def example_metrics():
    registry = CollectorRegistry()
    requests = Counter('prediction_requests_total', 'prediction requests',
                       ['status_class'], registry=registry)
    latency = Histogram('prediction_latency_seconds', 'prediction latency', registry=registry)
    requests.labels(status_class='2xx').inc()
    latency.observe(0.03)
    return generate_latest(registry).decode()


if __name__ == '__main__':
    print(example_metrics())

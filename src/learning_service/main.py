from prometheus_client import start_http_server
from text_classification import main

if __name__ == '__main__':
    start_http_server(8000)  # exposes the Prometheus metrics on the localhost:8000/metrics URL
    while True:
        main()

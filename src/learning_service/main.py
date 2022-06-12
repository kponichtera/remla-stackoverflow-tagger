from prometheus_client import start_http_server
from text_classification import main

if __name__ == '__main__':
    start_http_server(9010)
    while True:
        main()

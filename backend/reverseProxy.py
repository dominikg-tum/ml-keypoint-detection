from requests import get

# Code adapted from https://ajhyndman.medium.com/hot-reloading-with-react-and-flask-b5dae60d9898
def proxyRequest(host, path):
    response = get(host + path)

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]

    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }

    return (response.content, response.status_code, headers)
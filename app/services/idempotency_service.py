processed_requests = {}


def get_processed_request(request_id: str):
    return processed_requests.get(request_id)


def save_processed_request(request_id: str, result):
    processed_requests[request_id] = result
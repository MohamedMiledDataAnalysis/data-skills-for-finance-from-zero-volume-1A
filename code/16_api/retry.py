# retry.py - retry on rate limits and server errors
import time

import requests

RETRY_STATUS = {429, 500, 502, 503, 504}


def get_with_retry(url, params=None, headers=None,
                   attempts=4, wait=1):
    """GET a URL, retrying on rate limits and server errors."""
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params,
                                    headers=headers, timeout=10)
        except (requests.ConnectionError,
                requests.Timeout) as error:
            print(f"attempt {attempt}: "
                  f"{type(error).__name__}")
        else:
            if response.status_code not in RETRY_STATUS:
                response.raise_for_status()
                return response
            print(f"attempt {attempt}: status "
                  f"{response.status_code}")
            if "Retry-After" in response.headers:
                wait = int(response.headers["Retry-After"])
        if attempt < attempts:
            print(f"   waiting {wait} s")
            time.sleep(wait)
            wait = wait * 2
    raise RuntimeError(f"gave up on {url} after "
                       f"{attempts} attempts")


if __name__ == "__main__":
    ok = get_with_retry("http://127.0.0.1:8000/health")
    print("8000:", ok.json())
    try:
        get_with_retry("http://127.0.0.1:8001/health",
                       attempts=3)
    except RuntimeError as error:
        print("RuntimeError:", error)

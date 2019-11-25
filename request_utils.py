from requests import post


def make_full_url(url: str, index: str) -> str:
    return f"{url}/{index}/_search"


def clear_cache(url: str, index: str):
    full_url = f"{url}/{index}/_cache/clear?request=true"
    r = post(full_url)
    if r.status_code != 200:
        raise Exception(f"Error clearing cache: {r.json()}")

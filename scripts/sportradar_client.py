# scripts/sportradar_client.py
import os, time, json, logging
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")
BASE_URL = os.getenv("SPORTRADAR_BASE_URL")
HEADERS = {"Accept": "application/json"}
logger = logging.getLogger(__name__)

def get_json(endpoint, params=None, save_path=None, max_retries=5, backoff=2.0):
    
    if params is None:
        params = {}
    params.update({"api_key": API_KEY})
    url = BASE_URL.rstrip("/") + "/" + endpoint.lstrip("/")

    for attempt in range(max_retries):
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        status = resp.status_code
        if status == 200:
            data = resp.json()
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return data
        elif status in (429, 503):  # rate limit or service unavailable
            wait = backoff * (2 ** attempt)
            logger.warning("Status %s, sleeping %s seconds...", status, wait)
            time.sleep(wait)
            continue
        else:
            resp.raise_for_status()

    raise RuntimeError(f"Failed to GET {url} after {max_retries} attempts")

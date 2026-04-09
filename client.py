import requests
import json
import logging
import time
import os
from datetime import datetime

SERVER_URL  = "https://student-server-production-528a.up.railway.app/submit-file"
INPUT_FILE  = "original.json"
RETRY_DELAY = 60

SERVER_OPEN_HOUR  = 9
SERVER_CLOSE_HOUR = 18

def is_server_hours():
    now = datetime.now()
    return SERVER_OPEN_HOUR <= now.hour < SERVER_CLOSE_HOUR

# figure out which log file to use before setting up logging
if is_server_hours():
    LOG_FILE      = "client_available.log"
    OUTPUT_FILE   = "modified_available.json"
    scenario      = "AVAILABLE"
else:
    LOG_FILE      = "client_unavailable.log"
    OUTPUT_FILE   = "modified_unavailable.json"
    scenario      = "UNAVAILABLE"

# ─── Logging Setup ───
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# PART 1 - JSON file Creation

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("File loaded: " + str(data))
    return data


# PART 2 - Client Implementation

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info("Saved to " + filepath)


def send_request(data):
    json_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
    files = {"file": ("original.json", json_bytes, "application/json")}
    print("Sending request...")
    response = requests.post(SERVER_URL, files=files, timeout=15)

    if response.status_code in (415, 422):
        logger.warning("Form-data rejected, retrying with raw JSON...")
        response = requests.post(SERVER_URL, json=data, timeout=15)

    response.raise_for_status()
    return response.json()


# PART 3 - Robustness Requirements

def run_client():
    logger.info("client started — scenario: " + scenario)
    logger.info("log file: " + LOG_FILE)
    logger.info("output file: " + OUTPUT_FILE)

    if not os.path.exists(INPUT_FILE):
        print("file not found!")
        return

    try:
        original_data = load_json(INPUT_FILE)
    except Exception as e:
        print("error reading json: " + str(e))
        return

    attempt = 0
    while True:
        attempt += 1
        logger.info("attempt #" + str(attempt))

        try:
            modified_data = send_request(original_data)
            save_json(OUTPUT_FILE, modified_data)
            logger.info("success!")
            print("Done! Check " + OUTPUT_FILE)
            compare_json(original_data, modified_data)
            break

        except requests.exceptions.ConnectionError:
            logger.warning("connection error, retrying...")
            print("cant connect, trying again in " + str(RETRY_DELAY) + " seconds")

        except requests.exceptions.Timeout:
            logger.warning("timeout")
            print("timeout :(")

        except requests.exceptions.HTTPError as e:
            logger.warning("http error: " + str(e.response.status_code))
            print("server said: " + str(e.response.status_code))
            if e.response.status_code == 400:
                print("bad request, stopping")
                break

        except Exception as e:
            logger.warning("something went wrong: " + str(e))
            print("error: " + str(e))

        time.sleep(RETRY_DELAY)


# PART 4 - Output Processing and Difference Analysis

def compare_json(original, modified):
    print("\n--- JSON Comparison ---")
    all_keys = set(original.keys()) | set(modified.keys())

    added = []
    changed = []
    unchanged = []

    for key in all_keys:
        if key not in original:
            added.append(key)
            print("ADDED: " + key + " = " + str(modified[key]))
            logger.info("ADDED: " + key)
        elif key not in modified:
            print("REMOVED: " + key)
        elif original[key] != modified[key]:
            changed.append(key)
            print("CHANGED: " + key + ": " + str(original[key]) + " -> " + str(modified[key]))
            logger.info("CHANGED: " + key)
        else:
            unchanged.append(key)
            print("same: " + key)

    print("\nSummary:")
    print("added: " + str(added))
    print("changed: " + str(changed))
    print("unchanged: " + str(unchanged))
    logger.info("added: " + str(added) + " | changed: " + str(changed) + " | unchanged: " + str(unchanged))


if __name__ == "__main__":
    run_client()
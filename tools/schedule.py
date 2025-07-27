import requests
import json
from dotenv import load_dotenv
import logging
from base import get_calcom_client


# Configure logging
logger = logging.getLogger(__name__)


load_dotenv()

def header():
    client = get_calcom_client()
    if not client:
        logging.error("Could not get Cal.com client")
        return {"error": "Could not get Cal.com client"}
    value = {
    "Authorization": client,
    "cal-api-version": "2024-06-11"
    }

    return value



def cal_get_all_schedules() -> dict:
    """
    Retrieve all schedules from Cal.com API.

    Returns:
        dict: On success → parsed JSON response from Cal.com API.
              On failure → dict with "error" key and message.
    """
    head = header()
    if not head:
        logging.error("Could not get Cal.com client")
        return {"error": "Could not get Cal.com client"}

    url = "https://api.cal.com/v2/schedules/"
    logging.info(f"Requesting Cal.com schedules from {url}")

    try:
        response = requests.get(url, headers=head)
        response.raise_for_status()  # Raise exception for HTTP errors
        logging.info("Successfully retrieved Cal.com schedules")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Could not get Cal.com schedules from {url}: {e}")
        return {"error": f"Could not get Cal.com schedules from {url}"}
    except Exception as e:
        logging.error(f"Unexpected error when fetching Cal.com schedules: {e}")
        return {"error": "Unexpected error occurred"}




if __name__ == "__main__":

    cal_schedules = cal_get_all_schedules()
    print(cal_schedules)
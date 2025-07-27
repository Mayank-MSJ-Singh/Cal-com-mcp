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
    headers = header()
    if not headers:
        logging.error("Could not get Cal.com client")
        return {"error": "Could not get Cal.com client"}

    url = "https://api.cal.com/v2/schedules/"
    logging.info(f"Requesting Cal.com schedules from {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        logging.info("Successfully retrieved Cal.com schedules")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Could not get Cal.com schedules from {url}: {e}")
        return {"error": f"Could not get Cal.com schedules from {url}"}
    except Exception as e:
        logging.error(f"Unexpected error when fetching Cal.com schedules: {e}")
        return {"error": "Unexpected error occurred"}

def cal_create_a_schedule(
    name: str,
    timeZone: str,
    isDefault: bool,
    availability: list = None,
    overrides: list = None
) -> dict:
    """
    Create a new schedule in Cal.com.

    Args:
        name (str): Schedule name.
        timeZone (str): Time zone string (e.g., "America/New_York").
        isDefault (bool): Whether this should be the default schedule.
        availability (list, optional): List of availability blocks. Each block is a dict:
            {
                "days": ["Monday", "Tuesday", ...],  # Days must start with a capital letter
                "startTime": "09:00",                # Time format: "HH:mm"
                "endTime": "17:00"
            }
        overrides (list, optional): List of overrides for specific dates. Each override is a dict:
            {
                "date": "YYYY-MM-DD",
                "startTime": "10:00",                # Time format: "HH:mm"
                "endTime": "12:00"
            }

    Returns:
        dict: If successful, parsed JSON response from Cal.com.
              If failed, dict with "error" key and message.
    """

    url = "https://api.cal.com/v2/schedules/"
    headers = header()
    if not headers:
        logging.error("Could not get Cal.com client")
        return {"error": "Could not get Cal.com client"}

    payload = {
        "name": name,
        "timeZone": timeZone,
        "isDefault": isDefault,
    }

    if availability:
        payload["availability"] = availability
    if overrides:
        payload["overrides"] = overrides

    logging.info(f"Creating Cal.com schedule: {name}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info("Successfully created Cal.com schedule")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Could not create Cal.com schedule: {e}")
        return {"error": f"Could not create Cal.com schedule: {e}"}
    except Exception as e:
        logging.error(f"Unexpected error when creating Cal.com schedule: {e}")
        return {"error": "Unexpected error occurred"}




if __name__ == "__main__":
    '''
    cal_schedules = cal_get_all_schedules()
    print(cal_schedules)
    
    result = cal_create_a_schedule(
        name="My Default Schedule",
        timeZone="America/New_York",
        isDefault=True,
        availability=[
            {
                "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "startTime": "09:00",
                "endTime": "17:00"
            }
        ],
        overrides=[]
    )

    print(result)
    '''

    pass



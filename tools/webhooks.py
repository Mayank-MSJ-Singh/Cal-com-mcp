import requests
import logging
from base import get_calcom_client

# Configure logging
logger = logging.getLogger(__name__)


def header():
    """Retrieve authentication headers for Cal.com API"""
    client = get_calcom_client()
    if not client:
        logger.error("Could not get Cal.com client")
        return None
    return {
        "Authorization": client,
        "Content-Type": "application/json"
    }


def cal_get_all_webhooks(take: int = 250, skip: int = None) -> dict:
    """
    Retrieve all webhooks with pagination support.

    Args:
        take (int): Number of records to return
        skip (int): Number of records to skip

    Returns:
        dict: API response or error message
    """
    headers = header()
    if not headers:
        return {"error": "Could not get Cal.com client"}

    url = "https://api.cal.com/v2/webhooks"
    params = {}

    if take is not None:
        params["take"] = take
    if skip is not None:
        params["skip"] = skip

    logger.info(f"Requesting webhooks (take: {take}, skip: {skip})")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logger.info("Successfully retrieved webhooks")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get webhooks: {e}")
        return {"error": f"Failed to get webhooks: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}


def cal_create_webhook(
    active: bool,
    subscriberUrl: str,
    triggers: list[str],
    payloadTemplate: str = None,
    secret: str = None
) -> dict:
    """
    Create a new webhook in Cal.com.

    Request Body (application/json):
        active (bool, required): Whether the webhook is active
        subscriberUrl (str, required): URL to receive webhook payloads
        triggers (list[str], required): List of trigger events. Valid options:
            - BOOKING_CREATED
            - BOOKING_PAYMENT_INITIATED
            - BOOKING_PAID
            - BOOKING_RESCHEDULED
            - BOOKING_REQUESTED
            - BOOKING_CANCELLED
            - BOOKING_REJECTED
            - BOOKING_NO_SHOW_UPDATED
            - FORM_SUBMITTED
            - MEETING_ENDED
            - MEETING_STARTED
            - RECORDING_READY
            - INSTANT_MEETING
            - RECORDING_TRANSCRIPTION_GENERATED
            - OOO_CREATED
            - AFTER_HOSTS_CAL_VIDEO_NO_SHOW
            - AFTER_GUESTS_CAL_VIDEO_NO_SHOW
            - FORM_SUBMITTED_NO_EVENT
        payloadTemplate (str, optional): Custom payload template.
            See: https://cal.com/docs/core-features/webhooks
            Example: '{"content":"New event","type":"{{type}}","name":"{{title}}"}'
        secret (str, optional): Secret for verifying webhooks

    Returns:
        dict: API response with structure:
            {
                "status": "success"|"error",
                "data": {
                    "id": int,                     # Webhook ID
                    "userId": int,                 # User ID
                    "subscriberUrl": str,          # Target URL
                    "active": bool,                # Active status
                    "triggers": list[str],         # Event triggers
                    "payloadTemplate": str,        # Payload template
                    "secret": str                  # Verification secret
                }
            }

    Example Response (201 - application/json):
        {
            "status": "success",
            "data": {
                "id": 123,
                "userId": 456,
                "subscriberUrl": "https://example.com/webhook",
                "active": true,
                "triggers": ["BOOKING_CREATED"],
                "payloadTemplate": "{\\"content\\":\\"New event\\"}",
                "secret": "my-secret-key"
            }
        }

    Error Responses:
        - 400: Invalid request parameters
        - 401: Unauthorized
        - 500: Server error
    """
    headers = header()
    if not headers:
        return {"error": "Could not get Cal.com client"}

    url = "https://api.cal.com/v2/webhooks"
    payload = {
        "active": active,
        "subscriberUrl": subscriberUrl,
        "triggers": triggers
    }

    if payloadTemplate:
        payload["payloadTemplate"] = payloadTemplate
    if secret:
        payload["secret"] = secret

    logger.info(f"Creating webhook for URL: {subscriberUrl}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info("Successfully created webhook")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook creation failed: {e}")
        return {"error": f"Webhook creation failed: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}


def cal_get_webhook(webhook_id: str) -> dict:
    """
    Get a specific webhook by ID.

    Args:
        webhook_id (str): ID of the webhook to retrieve

    Returns:
        dict: API response or error message
    """
    headers = header()
    if not headers:
        return {"error": "Could not get Cal.com client"}

    url = f"https://api.cal.com/v2/webhooks/{webhook_id}"
    logger.info(f"Requesting webhook with ID: {webhook_id}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully retrieved webhook ID {webhook_id}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            logger.error(f"Webhook not found with ID: {webhook_id}")
            return {"error": f"Webhook not found with ID: {webhook_id}"}
        logger.error(f"HTTP error getting webhook: {e}")
        return {"error": f"HTTP error getting webhook: {str(e)}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for webhook ID {webhook_id}: {e}")
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error getting webhook ID {webhook_id}: {e}")
        return {"error": "Unexpected error occurred"}


def cal_update_webhook(
    webhook_id: str,
    active: bool = None,
    subscriberUrl: str = None,
    triggers: list[str] = None,
    payloadTemplate: str = None,
    secret: str = None
) -> dict:
    """
    Update an existing webhook in Cal.com.

    Path Parameters:
        webhookId (str, required): ID of the webhook to update

    Request Body (application/json):
        active (bool, optional): Whether the webhook is active
        subscriberUrl (str, optional): New URL to receive webhook payloads
        triggers (list[str], optional): Updated list of trigger events. Valid options:
            - BOOKING_CREATED
            - BOOKING_PAYMENT_INITITATED
            - BOOKING_PAID
            - BOOKING_RESCHEDULED
            - BOOKING_REQUESTED
            - BOOKING_CANCELLED
            - BOOKING_REJECTED
            - BOOKING_NO_SHOW_UPDATED
            - FORM_SUBMITTED
            - MEETING_ENDED
            - MEETING_STARTED
            - RECORDING_READY
            - INSTANT_MEETING
            - RECORDING_TRANSCRIPTION_GENERATED
            - OOO_CREATED
            - AFTER_HOSTS_CAL_VIDEO_NO_SHOW
            - AFTER_GUESTS_CAL_VIDEO_NO_SHOW
            - FORM_SUBMITTED_NO_EVENT
        payloadTemplate (str, optional): Updated payload template.
            See: https://cal.com/docs/core-features/webhooks
            Example: '{"content":"Updated event","type":"{{type}}"}'
        secret (str, optional): New secret for verifying webhooks

    Returns:
        dict: API response with structure:
            {
                "status": "success"|"error",
                "data": {
                    "id": int,                     # Webhook ID
                    "userId": int,                 # User ID
                    "subscriberUrl": str,          # Updated target URL
                    "active": bool,                # Updated active status
                    "triggers": list[str],         # Updated event triggers
                    "payloadTemplate": str,        # Updated payload template
                    "secret": str                  # Updated verification secret
                }
            }

    Example Response (200 - application/json):
        {
            "status": "success",
            "data": {
                "id": 123,
                "userId": 456,
                "subscriberUrl": "https://example.com/webhook/updated",
                "active": true,
                "triggers": ["BOOKING_CREATED", "BOOKING_CANCELLED"],
                "payloadTemplate": "{\\"content\\":\\"Updated event\\"}",
                "secret": "new-secret-key"
            }
        }

    Error Responses:
        - 400: Invalid request parameters
        - 401: Unauthorized
        - 404: Webhook not found
        - 500: Server error
    """
    headers = header()
    if not headers:
        return {"error": "Could not get Cal.com client"}

    url = f"https://api.cal.com/v2/webhooks/{webhook_id}"
    payload = {}

    if active is not None:
        payload["active"] = active
    if subscriberUrl is not None:
        payload["subscriberUrl"] = subscriberUrl
    if triggers is not None:
        payload["triggers"] = triggers
    if payloadTemplate is not None:
        payload["payloadTemplate"] = payloadTemplate
    if secret is not None:
        payload["secret"] = secret

    logger.info(f"Updating webhook with ID: {webhook_id}")

    try:
        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully updated webhook ID {webhook_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook update failed: {e}")
        return {"error": f"Webhook update failed: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}


def cal_delete_webhook(webhook_id: str) -> dict:
    """
    Delete a webhook by ID.

    Args:
        webhook_id (str): ID of the webhook to delete

    Returns:
        dict: API response or error message
    """
    headers = header()
    if not headers:
        return {"error": "Could not get Cal.com client"}

    url = f"https://api.cal.com/v2/webhooks/{webhook_id}"
    logger.info(f"Deleting webhook with ID: {webhook_id}")

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully deleted webhook ID {webhook_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Webhook deletion failed: {e}")
        return {"error": f"Webhook deletion failed: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}


if __name__ == "__main__":
    import uuid
    import json

    print("---- TESTING cal_get_all_webhook ----")

    print("Test 1: take=5 (int)")
    print(cal_get_all_webhooks(take=5))

    print("\nTest 2: skip=2 (int)")
    print(cal_get_all_webhooks(skip=2))

    print("\nTest 3: take=10, skip=2 (int)")
    print(cal_get_all_webhooks(take=10, skip=2))

    print("\nTest 4: No parameters")
    print(cal_get_all_webhooks())

    print("---- TESTING cal_create_webhook with unique URLs ----")


    def unique_url():
        return f"https://example.com/webhook/{uuid.uuid4()}"


    print("\nTest 5: Basic webhook creation")
    print(cal_create_webhook(
        active=True,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED"]
    ))

    print("\nTest 6: Multiple triggers")
    print(cal_create_webhook(
        active=True,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED", "BOOKING_CANCELLED"]
    ))

    print("\nTest 7: With payload template")
    print(cal_create_webhook(
        active=True,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED"],
        payloadTemplate='{"custom": "{{booker.name}}"}'
    ))

    print("\nTest 8: With secret")
    print(cal_create_webhook(
        active=True,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED"],
        secret="my-secret-123"
    ))

    print("\nTest 9: Inactive webhook")
    print(cal_create_webhook(
        active=False,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED"]
    ))

    print("\nTest 10: All parameters")
    print(cal_create_webhook(
        active=True,
        subscriberUrl=unique_url(),
        triggers=["BOOKING_CREATED", "BOOKING_CANCELLED"],
        payloadTemplate='{"custom":"{{booker.name}}"}',
        secret="my-secret-123"
    ))

    print("---- TESTING cal_get_webhook / cal_update_webhook / cal_delete_webhook ----")


    # Helper to create a webhook and return its ID
    def create_test_webhook():
        response = cal_create_webhook(
            active=True,
            subscriberUrl=f"https://example.com/webhook/{uuid.uuid4()}",
            triggers=["BOOKING_CREATED"]
        )
        try:
            data = json.loads(response)
            return data["id"]  # Adjusted based on actual API response structure
        except:
            return None


    # Test 11: Create webhook, then get it
    print("\nTest 11: Create + Get webhook")
    webhook_id = create_test_webhook()
    if webhook_id:
        print("Created webhook ID:", webhook_id)
        print("Get webhook response:")
        print(cal_get_webhook(webhook_id))
    else:
        print("Failed to create test webhook")

    # Test 12: Update webhook - toggle active status
    print("\nTest 12: Update webhook - toggle active")
    if webhook_id:
        print(cal_update_webhook(
            webhookId=webhook_id,
            active=False
        ))

    # Test 13: Update webhook - change URL
    print("\nTest 13: Update webhook - change URL")
    if webhook_id:
        print(cal_update_webhook(
            webhookId=webhook_id,
            subscriberUrl=f"https://example.com/updated/{uuid.uuid4()}"
        ))

    # Test 14: Update webhook - change triggers
    print("\nTest 14: Update webhook - change triggers")
    if webhook_id:
        print(cal_update_webhook(
            webhookId=webhook_id,
            triggers=["BOOKING_CANCELLED", "MEETING_ENDED"]
        ))

    # Test 15: Update webhook - all parameters
    print("\nTest 15: Update webhook - all parameters")
    if webhook_id:
        print(cal_update_webhook(
            webhookId=webhook_id,
            active=True,
            subscriberUrl=f"https://example.com/final/{uuid.uuid4()}",
            triggers=["BOOKING_RESCHEDULED"],
            payloadTemplate={"newTemplate": "{{attendee.email}}"},
            secret="new-secret-456"
        ))

    # Test 16: Delete webhook
    print("\nTest 16: Delete webhook")
    if webhook_id:
        print("Delete response:")
        print(cal_delete_webhook(webhook_id))
        print("Attempting to get deleted webhook:")
        print(cal_get_webhook(webhook_id))
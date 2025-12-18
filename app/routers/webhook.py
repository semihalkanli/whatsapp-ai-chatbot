"""
WhatsApp webhook router for receiving messages and events.
"""

import logging
from fastapi import APIRouter, Request, HTTPException, Query
from app.config import settings
from app.models.messages import WebhookPayload
from app.services.whatsapp import whatsapp_service
from app.services.ai import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge")
):
    """
    Verify webhook endpoint for WhatsApp Business API setup.

    This endpoint is called by Meta during webhook configuration.
    """
    logger.info(f"Webhook verification request received: mode={mode}")

    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        logger.info("Webhook verified successfully")
        return int(challenge)
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive webhook events from WhatsApp Business API.

    Processes incoming messages and sends AI-generated responses.
    """
    try:
        # Parse webhook payload
        body = await request.json()
        logger.info(f"Webhook received: {body}")

        # Validate webhook payload structure
        try:
            payload = WebhookPayload(**body)
        except Exception as e:
            logger.warning(f"Invalid webhook payload: {str(e)}")
            return {"status": "ignored"}

        # Process each entry
        for entry in payload.entry:
            for change in entry.changes:
                value = change.get("value", {})

                # Check if there are messages
                messages = value.get("messages")
                if not messages:
                    logger.debug("No messages in webhook")
                    continue

                # Process each message
                for message in messages:
                    await process_message(message)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # Return 200 to prevent Meta from retrying
        return {"status": "error", "message": str(e)}


async def process_message(message: dict):
    """
    Process a single incoming message.

    Args:
        message: Message object from webhook
    """
    try:
        # Extract message details
        message_id = message.get("id")
        from_number = message.get("from")
        message_type = message.get("type")

        # Only handle text messages
        if message_type != "text":
            logger.info(f"Ignoring non-text message type: {message_type}")
            return

        # Get message text
        text_body = message.get("text", {}).get("body", "").strip()
        if not text_body:
            logger.warning("Empty message body")
            return

        logger.info(f"Processing message from {from_number}: {text_body}")

        # Mark message as read
        await whatsapp_service.mark_message_as_read(message_id)

        # Generate AI response
        ai_response = await ai_service.process_message(
            phone_number=from_number,
            user_message=text_body
        )

        # Send response back to user
        await whatsapp_service.send_text_message(
            to=from_number,
            message=ai_response
        )

        logger.info(f"Response sent to {from_number}")

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        # Try to send error message to user
        try:
            error_msg = "Sorry, I encountered an error. Please try again later."
            await whatsapp_service.send_text_message(
                to=message.get("from"),
                message=error_msg
            )
        except:
            pass

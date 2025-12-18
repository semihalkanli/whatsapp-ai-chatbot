"""
WhatsApp Business API service for sending messages.
"""

import logging
import httpx
from app.config import settings
from app.models.messages import TextMessage

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Service for interacting with WhatsApp Business API."""

    def __init__(self):
        """Initialize WhatsApp service."""
        self.base_url = settings.whatsapp_api_base_url
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.token = settings.whatsapp_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        logger.info("WhatsApp service initialized")

    async def send_text_message(self, to: str, message: str) -> dict:
        """
        Send a text message via WhatsApp.

        Args:
            to: Recipient's phone number
            message: Text message content

        Returns:
            API response as dict

        Raises:
            Exception: If the API call fails
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        # Create message payload
        payload = TextMessage(
            to=to,
            text={"body": message}
        )

        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Sending WhatsApp message to {to}: {message[:50]}...")
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload.model_dump(),
                    timeout=30.0
                )
                response.raise_for_status()

                result = response.json()
                logger.info(f"Message sent successfully: {result}")
                return result

        except httpx.HTTPStatusError as e:
            logger.error(f"WhatsApp API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Failed to send WhatsApp message: {e.response.text}")
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            raise Exception(f"Failed to send WhatsApp message: {str(e)}")

    async def mark_message_as_read(self, message_id: str) -> dict:
        """
        Mark a message as read.

        Args:
            message_id: ID of the message to mark as read

        Returns:
            API response as dict
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                logger.debug(f"Message {message_id} marked as read")
                return result

        except Exception as e:
            logger.warning(f"Failed to mark message as read: {str(e)}")
            # Don't raise - marking as read is not critical
            return {}


# Global WhatsApp service instance
whatsapp_service = WhatsAppService()

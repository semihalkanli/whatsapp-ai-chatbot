"""
Pydantic models for WhatsApp webhook messages.
"""

from typing import Any, Literal
from pydantic import BaseModel, Field


class WebhookMessage(BaseModel):
    """WhatsApp webhook message model."""

    from_: str = Field(alias="from", description="Sender's phone number")
    id: str = Field(description="Message ID")
    timestamp: str = Field(description="Message timestamp")
    text: dict[str, str] | None = Field(default=None, description="Text message content")
    type: str = Field(description="Message type (text, image, etc.)")


class WebhookValue(BaseModel):
    """WhatsApp webhook value model."""

    messaging_product: str = Field(description="Product name (whatsapp)")
    metadata: dict[str, Any] = Field(description="Metadata including phone number ID")
    contacts: list[dict[str, Any]] | None = Field(default=None, description="Contact information")
    messages: list[WebhookMessage] | None = Field(default=None, description="Received messages")
    statuses: list[dict[str, Any]] | None = Field(default=None, description="Message status updates")


class WebhookEntry(BaseModel):
    """WhatsApp webhook entry model."""

    id: str = Field(description="WhatsApp Business Account ID")
    changes: list[dict[str, Any]] = Field(description="Changes array")


class WebhookPayload(BaseModel):
    """Root WhatsApp webhook payload model."""

    object: str = Field(description="Object type (whatsapp_business_account)")
    entry: list[WebhookEntry] = Field(description="Webhook entries")


class TextMessage(BaseModel):
    """Model for sending a text message via WhatsApp."""

    messaging_product: Literal["whatsapp"] = "whatsapp"
    recipient_type: Literal["individual"] = "individual"
    to: str = Field(description="Recipient's phone number")
    type: Literal["text"] = "text"
    text: dict[str, str] = Field(description="Text message content")


class ChatMessage(BaseModel):
    """Model for chat conversation messages."""

    role: Literal["user", "assistant", "system"] = Field(description="Message role")
    content: str = Field(description="Message content")

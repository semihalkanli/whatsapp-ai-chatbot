"""
AI Service module with provider factory and session management.
"""

import logging
from typing import Literal
from app.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.groq import GroqProvider
from app.services.ai.openai import OpenAIProvider
from app.services.ai.claude import ClaudeProvider
from app.models.messages import ChatMessage

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """Factory for creating AI provider instances."""

    @staticmethod
    def create_provider(
        provider_type: Literal["groq", "openai", "claude"]
    ) -> AIProvider:
        """
        Create an AI provider instance based on the provider type.

        Args:
            provider_type: Type of AI provider to create

        Returns:
            AIProvider instance

        Raises:
            ValueError: If provider type is invalid or API key is missing
        """
        if provider_type == "groq":
            if not settings.groq_api_key:
                raise ValueError("GROQ_API_KEY is not configured")
            return GroqProvider(api_key=settings.groq_api_key)

        elif provider_type == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not configured")
            return OpenAIProvider(api_key=settings.openai_api_key)

        elif provider_type == "claude":
            if not settings.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is not configured")
            return ClaudeProvider(api_key=settings.anthropic_api_key)

        else:
            raise ValueError(f"Unknown AI provider: {provider_type}")


class ConversationManager:
    """Manages conversation history for different phone numbers (in-memory)."""

    def __init__(self, max_history: int = 10):
        """
        Initialize conversation manager.

        Args:
            max_history: Maximum number of messages to keep per conversation
        """
        self.conversations: dict[str, list[ChatMessage]] = {}
        self.max_history = max_history
        logger.info(f"Conversation manager initialized (max history: {max_history})")

    def add_message(self, phone_number: str, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            phone_number: User's phone number (conversation ID)
            role: Message role (user/assistant)
            content: Message content
        """
        if phone_number not in self.conversations:
            self.conversations[phone_number] = []

        # Create message
        message = ChatMessage(role=role, content=content)
        self.conversations[phone_number].append(message)

        # Trim history if needed (keep only last N messages)
        if len(self.conversations[phone_number]) > self.max_history:
            self.conversations[phone_number] = self.conversations[phone_number][-self.max_history:]

        logger.debug(f"Added {role} message for {phone_number} (history: {len(self.conversations[phone_number])})")

    def get_history(self, phone_number: str) -> list[ChatMessage]:
        """
        Get conversation history for a phone number.

        Args:
            phone_number: User's phone number

        Returns:
            List of chat messages (empty list if no history)
        """
        return self.conversations.get(phone_number, [])

    def clear_history(self, phone_number: str) -> None:
        """
        Clear conversation history for a phone number.

        Args:
            phone_number: User's phone number
        """
        if phone_number in self.conversations:
            del self.conversations[phone_number]
            logger.info(f"Cleared conversation history for {phone_number}")


class AIService:
    """Main AI service that coordinates provider and conversation management."""

    def __init__(self):
        """Initialize AI service with configured provider."""
        self.provider = AIProviderFactory.create_provider(settings.ai_provider)
        self.conversation_manager = ConversationManager()
        logger.info(f"AI Service initialized with provider: {self.provider.get_provider_name()}")

    async def process_message(self, phone_number: str, user_message: str) -> str:
        """
        Process a user message and generate a response.

        Args:
            phone_number: User's phone number (used for conversation tracking)
            user_message: The user's message text

        Returns:
            AI-generated response text
        """
        try:
            # Get conversation history
            history = self.conversation_manager.get_history(phone_number)

            # Generate response
            logger.info(f"Processing message from {phone_number}: {user_message[:50]}...")
            response = await self.provider.generate_response(
                user_message=user_message,
                conversation_history=history
            )

            # Update conversation history
            self.conversation_manager.add_message(phone_number, "user", user_message)
            self.conversation_manager.add_message(phone_number, "assistant", response)

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "Sorry, I encountered an error processing your message. Please try again."


# Global AI service instance
ai_service = AIService()

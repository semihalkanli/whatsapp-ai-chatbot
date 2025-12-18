"""
Abstract base class for AI providers.
All AI providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Protocol


class ChatMessage(Protocol):
    """Protocol for chat messages."""
    role: str
    content: str


class AIProvider(ABC):
    """Abstract base class for AI chat providers."""

    SYSTEM_PROMPT = """You are a helpful AI assistant integrated with WhatsApp Business.
You can communicate in multiple languages - automatically detect and respond in the user's language.

Key behaviors:
- Be friendly, professional, and concise
- Respond in the same language the user writes in
- If you don't understand something, politely ask for clarification
- Keep responses brief and relevant for messaging context
- Be helpful and informative

You are here to assist with general questions and conversations."""

    @abstractmethod
    async def generate_response(
        self,
        user_message: str,
        conversation_history: list[ChatMessage] | None = None
    ) -> str:
        """
        Generate a response to the user's message.

        Args:
            user_message: The user's message text
            conversation_history: Optional list of previous messages in the conversation

        Returns:
            The AI-generated response text

        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the AI provider.

        Returns:
            Provider name (e.g., "Groq", "OpenAI", "Claude")
        """
        pass

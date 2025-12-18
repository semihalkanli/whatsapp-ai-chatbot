"""
Groq AI provider implementation.
Uses Groq's API with Llama models (free tier available).
"""

import logging
from groq import AsyncGroq
from app.services.ai.base import AIProvider, ChatMessage

logger = logging.getLogger(__name__)


class GroqProvider(AIProvider):
    """Groq AI provider using Llama models."""

    def __init__(self, api_key: str):
        """
        Initialize Groq provider.

        Args:
            api_key: Groq API key from console.groq.com
        """
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Fast and capable model
        logger.info(f"Initialized Groq provider with model: {self.model}")

    async def generate_response(
        self,
        user_message: str,
        conversation_history: list[ChatMessage] | None = None
    ) -> str:
        """Generate a response using Groq's Llama model."""
        try:
            # Build messages array
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({"role": msg.role, "content": msg.content})

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call Groq API
            logger.debug(f"Calling Groq API with {len(messages)} messages")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )

            # Extract response text
            response_text = response.choices[0].message.content
            logger.info(f"Groq response generated: {len(response_text)} characters")
            return response_text

        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise Exception(f"Failed to generate response from Groq: {str(e)}")

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Groq"

"""
OpenAI provider implementation.
Uses OpenAI's GPT models (paid service).
"""

import logging
from openai import AsyncOpenAI
from app.services.ai.base import AIProvider, ChatMessage

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI provider using GPT models."""

    def __init__(self, api_key: str):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key from platform.openai.com
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cost-effective and capable model
        logger.info(f"Initialized OpenAI provider with model: {self.model}")

    async def generate_response(
        self,
        user_message: str,
        conversation_history: list[ChatMessage] | None = None
    ) -> str:
        """Generate a response using OpenAI's GPT model."""
        try:
            # Build messages array
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({"role": msg.role, "content": msg.content})

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI API
            logger.debug(f"Calling OpenAI API with {len(messages)} messages")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1
            )

            # Extract response text
            response_text = response.choices[0].message.content
            logger.info(f"OpenAI response generated: {len(response_text)} characters")
            return response_text

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate response from OpenAI: {str(e)}")

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "OpenAI"

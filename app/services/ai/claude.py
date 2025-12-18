"""
Claude/Anthropic provider implementation.
Uses Anthropic's Claude models (paid service).
"""

import logging
from anthropic import AsyncAnthropic
from app.services.ai.base import AIProvider, ChatMessage

logger = logging.getLogger(__name__)


class ClaudeProvider(AIProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key from console.anthropic.com
        """
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Sonnet model
        logger.info(f"Initialized Claude provider with model: {self.model}")

    async def generate_response(
        self,
        user_message: str,
        conversation_history: list[ChatMessage] | None = None
    ) -> str:
        """Generate a response using Claude."""
        try:
            # Build messages array (Claude doesn't include system in messages)
            messages = []

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    # Skip system messages in history (Claude handles system separately)
                    if msg.role != "system":
                        messages.append({"role": msg.role, "content": msg.content})

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call Claude API (system prompt is separate parameter)
            logger.debug(f"Calling Claude API with {len(messages)} messages")
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.SYSTEM_PROMPT,
                messages=messages,
                temperature=0.7
            )

            # Extract response text
            response_text = response.content[0].text
            logger.info(f"Claude response generated: {len(response_text)} characters")
            return response_text

        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise Exception(f"Failed to generate response from Claude: {str(e)}")

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Claude"

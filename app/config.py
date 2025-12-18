"""
Application configuration management using Pydantic Settings.
Handles environment variables and application settings.
"""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # WhatsApp Business API Configuration
    whatsapp_token: str = Field(
        description="WhatsApp Business API access token from Meta Developer Portal"
    )
    whatsapp_phone_number_id: str = Field(
        description="WhatsApp Business phone number ID"
    )
    whatsapp_verify_token: str = Field(
        description="Custom verification token for webhook setup"
    )

    # AI Provider Configuration
    ai_provider: Literal["groq", "openai", "claude"] = Field(
        default="groq",
        description="AI provider to use for chat completions"
    )

    # AI API Keys (at least one is required based on ai_provider)
    groq_api_key: str | None = Field(
        default=None,
        description="Groq API key from console.groq.com"
    )
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key from platform.openai.com"
    )
    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key from console.anthropic.com"
    )

    # Application Settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    log_level: str = Field(
        default="info",
        description="Logging level (debug, info, warning, error, critical)"
    )

    # WhatsApp API Base URL
    whatsapp_api_base_url: str = Field(
        default="https://graph.facebook.com/v18.0",
        description="WhatsApp Business API base URL"
    )

    def validate_ai_provider_key(self) -> None:
        """Validate that the required API key is present for the selected provider."""
        if self.ai_provider == "groq" and not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is required when AI_PROVIDER is 'groq'")
        elif self.ai_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER is 'openai'")
        elif self.ai_provider == "claude" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when AI_PROVIDER is 'claude'")


# Global settings instance
settings = Settings()

# Validate AI provider configuration on startup
settings.validate_ai_provider_key()

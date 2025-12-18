"""
Terminal-based Interactive Chat - WhatsApp AI Chatbot
Test the AI chatbot directly from your terminal without WhatsApp
"""

import asyncio
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ai import ai_service


async def interactive_chat():
    """Interactive chat with AI in the terminal."""

    print("=" * 70)
    print("🤖 WhatsApp AI Chatbot - Interactive Terminal Chat")
    print("=" * 70)
    print("\nCommands:")
    print("  - Type your message and press Enter to chat")
    print("  - Exit: 'exit', 'quit', 'q' or Ctrl+C")
    print("  - Clear history: 'clear', 'reset'")
    print("=" * 70)
    print(f"  AI Provider: {ai_service.provider.get_provider_name()}")
    print("=" * 70)

    # Test phone number (fake, just for session tracking)
    user_phone = "+1234567890"
    message_count = 0

    try:
        while True:
            # Get user input
            try:
                user_message = input("\n💬 You: ").strip()
            except EOFError:
                print("\n\n👋 Goodbye!")
                break

            # Check for empty input
            if not user_message:
                continue

            # Check for exit commands
            if user_message.lower() in ['exit', 'quit', 'q', 'bye']:
                print("\n👋 Goodbye!")
                print(f"📊 Total messages: {message_count}")
                break

            # Check for clear history command
            if user_message.lower() in ['clear', 'reset']:
                ai_service.conversation_manager.clear_history(user_phone)
                print("✅ Conversation history cleared!")
                message_count = 0
                continue

            # Process message with AI
            try:
                print("🤔 Bot is thinking...", end="\r")
                response = await ai_service.process_message(
                    phone_number=user_phone,
                    user_message=user_message
                )

                message_count += 1
                print(f"🤖 Bot: {response}")

            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("\nPlease check:")
                print("  - Is your API key set in .env file?")
                print("  - Is AI_PROVIDER configured correctly?")
                print("  - Do you have internet connection?")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        print(f"📊 Total messages: {message_count}")

    # Show conversation stats
    history = ai_service.conversation_manager.get_history(user_phone)
    if history:
        print(f"\n📝 Conversation history: {len(history)} messages")


if __name__ == "__main__":
    print("\n🚀 Starting AI service...\n")
    asyncio.run(interactive_chat())


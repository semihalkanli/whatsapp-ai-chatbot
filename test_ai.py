"""
AI Service test script - WhatsApp olmadan AI'yı test et
"""

import asyncio
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ai import ai_service


async def test_ai():
    """Test AI service without WhatsApp."""

    print("=" * 60)
    print("AI Service Test - WhatsApp AI Chatbot")
    print("=" * 60)

    # Test phone number (fake)
    test_phone = "+905551234567"

    # Test messages
    test_messages = [
        "Merhaba! Nasılsın?",
        "Python öğrenmek için tavsiye verir misin?",
        "Teşekkürler, çok yardımcı oldun!"
    ]

    print(f"\nTest kullanıcı: {test_phone}\n")

    for i, message in enumerate(test_messages, 1):
        print(f"[{i}] Kullanıcı: {message}")

        try:
            # Process message
            response = await ai_service.process_message(
                phone_number=test_phone,
                user_message=message
            )

            print(f"[{i}] Bot: {response}")
            print("-" * 60)

        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            print("\nLütfen .env dosyasını kontrol edin:")
            print("- GROQ_API_KEY ayarlandı mı?")
            print("- AI_PROVIDER=groq olarak ayarlandı mı?")
            break

    print("\n✅ Test tamamlandı!")
    print(f"Konuşma geçmişi: {len(ai_service.conversation_manager.get_history(test_phone))} mesaj")


if __name__ == "__main__":
    asyncio.run(test_ai())

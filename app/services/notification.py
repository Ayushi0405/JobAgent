import telegram
import os

class NotificationService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = telegram.Bot(token=self.token) if self.token else None

    async def send_alert(self, message: str, image_path: str = None):
        if not self.bot: return
        
        await self.bot.send_message(chat_id=self.chat_id, text=message)
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                await self.bot.send_photo(chat_id=self.chat_id, photo=photo)
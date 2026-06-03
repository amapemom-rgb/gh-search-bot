import asyncio, logging, os, uuid
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

user_threads: dict[int, str] = {}

def get_thread_id(chat_id: int) -> str:
    if chat_id not in user_threads:
        user_threads[chat_id] = str(chat_id)
    return user_threads[chat_id]

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Privet! Rasskazhi chto tebe nuzhno najti - ja pomogу razobratsia.")

@dp.message(Command("reset"))
async def reset(message: Message):
    chat_id = message.chat.id
    user_threads[chat_id] = f"{chat_id}_{uuid.uuid4().hex[:8]}"
    await message.answer("Dialog sbroshen. Nachinaem snachala!")

@dp.message()
async def handle(message: Message):
    thread_id = get_thread_id(message.chat.id)
    msg = await message.answer("...")
    try:
        result = await run_agent(message.text, thread_id)
        await msg.delete()
        for chunk in [result[i:i+4000] for i in range(0, len(result), 4000)]:
            await message.answer(chunk)
    except Exception as e:
        await msg.delete()
        await message.answer(f"Oshibka: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

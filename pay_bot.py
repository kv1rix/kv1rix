import asyncio
import uuid
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.filters import CommandStart

BOT_TOKEN = "PLACE_YOUR_BOT_TOKEN_HERE"
PROVIDER_TOKEN = "PLACE_YOUR_PROVIDER_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Это демо-бот для демонстрации автоматической выдачи доступов.\n"
        "Вы можете протестировать покупку подписки. Деньги реальные не списываются, платеж тестовый.\n\n"
        "Нажмите /buy чтобы проверить процесс оплаты."
    )

@dp.message(F.text == "/buy")
async def send_invoice(message: Message):
    await message.answer_invoice(
        title="Подписка на Сервис (1 месяц)",
        description="Автоматический доступ к сервису без участия админа.",
        payload="month_subscription",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Доступ на 30 дней", amount=49900)]
    )

@dp.shipping_query()
async def process_shipping(shipping_query):
    await bot.answer_shipping_query(shipping_query.id, ok=True)

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment(message: Message):
    generated_key = f"KEY-{uuid.uuid4().hex[:12].upper()}"
    
    await message.answer(
        f"✅ Оплата прошла успешно!\n\n"
        f"🤖 Система автоматически активировала ваш профиль.\n"
        f"🔑 Ваш индивидуальный ключ доступа:\n`{generated_key}`\n\n"
        f"Инструкция по подключению отправлена на вашу почту.",
        parse_mode="Markdown"
    )

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

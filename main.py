import logging
from aiogram import Bot, Dispatcher, executor, types
import config as cfg
import markups as nav
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')

# Проверка подписки
async def check_subscriptions(user_id):
    for channel in cfg.CHANNELS:
        try:
            user = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if user.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logging.warning(f"Ошибка при проверке подписки на {channel}: {e}")
            return False
    return True

# Обработчик кнопки "Я подписался"
@dp.message_handler(lambda message: message.text == "✅ Я подписался")
async def check_subscription_again(message: types.Message):
    if await check_subscriptions(message.from_user.id):
        await message.answer("✅ Спасибо за подписку! Можешь пользоваться ботом.", reply_markup=nav.mainMenu)
    else:
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Ты ещё не подписан на все каналы. Подпишись на все и нажми кнопку ещё раз:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            start_command = message.text
            referrer_id = None

            if len(start_command) > 7:
                referrer_id = start_command[7:]

                if referrer_id == str(message.from_user.id):
                    await bot.send_message(message.from_user.id, "⚠️ Нельзя регистрироваться по собственной ссылке!")
                    return

                db.add_user(message.from_user.id, referrer_id)
                db.add_balance(referrer_id, 1)
                try:
                    await bot.send_message(referrer_id, "🎉 По вашей ссылке зарегистрировался новый пользователь!")
                except:
                    logging.warning("Не удалось отправить сообщение рефереру")
            else:
                db.add_user(message.from_user.id)

            await bot.send_message(message.from_user.id, "Добро пожаловать! Для просмотра баланса нажми кнопку ниже.", reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "Ты уже зарегистрирован!", reply_markup=nav.mainMenu)

# Кнопка "Баланс"
@dp.message_handler(lambda message: message.text == "💰 Баланс")
async def balance_button(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    bal = db.get_balance(message.from_user.id)
    await bot.send_message(message.from_user.id, f"⭐ У тебя {bal} TG Stars")

# Кнопка "Моя статистика"
@dp.message_handler(lambda message: message.text == "📊 Моя статистика")
async def referral_stats_button(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    ref_count = db.get_referral_count(message.from_user.id)
    await bot.send_message(message.from_user.id, f"👥 Ты пригласил {ref_count} рефералов.")

# Кнопка "Моя реферальная ссылка"
@dp.message_handler(lambda message: message.text == "🔗 Моя реферальная ссылка")
async def referral_link(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    user_id = message.from_user.id
    referral_link = f"https://t.me/{cfg.BOT_USERNAME}?start={user_id}"
    await bot.send_message(message.from_user.id, f"Твоя реферальная ссылка: {referral_link}")

# Кнопка "Вывод"
@dp.message_handler(lambda message: message.text == "💸 Вывод")
async def withdrawal_button(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    bal = db.get_balance(message.from_user.id)
    if bal < 15:
        await bot.send_message(message.from_user.id, "❌ У тебя недостаточно средств для вывода!")
        return

    await bot.send_message(message.from_user.id, "Выбери сумму для вывода: 15, 25 или 50 TG Stars.", reply_markup=nav.withdrawalMenu())

# Запрос на вывод
@dp.message_handler(lambda message: message.text in ["15", "25", "50"])
async def request_withdrawal(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        channels_text = "\n".join([f"👉 {channel}" for channel in cfg.CHANNELS])
        await message.answer(
            f"❗ Для использования бота подпишись на все каналы:\n\n{channels_text}",
            reply_markup=nav.checkSubMenu
        )
        return

    withdrawal_amount = int(message.text)
    bal = db.get_balance(message.from_user.id)

    if withdrawal_amount > bal:
        await bot.send_message(message.from_user.id, "❌ У тебя недостаточно средств для вывода!")
        return

    if not message.from_user.username:
        await bot.send_message(message.from_user.id, "⚠️ У тебя должен быть установлен username, чтобы вывести средства.")
        return

    db.add_balance(message.from_user.id, -withdrawal_amount)

    withdrawal_message = f"🔔 Новый запрос на вывод:\n\nПользователь: @{message.from_user.username}\nСумма: {withdrawal_amount} TG Stars"
    await bot.send_message(cfg.ADMIN_ID, withdrawal_message)

    await bot.send_message(message.from_user.id, f"✅ Заявка на вывод {withdrawal_amount} TG Stars принята. Ожидайте обработки.")

# Админ: запросы на вывод
@dp.message_handler(lambda message: message.from_user.id == cfg.ADMIN_ID and message.text == "📋 Запросы на вывод")
async def admin_withdrawal_requests(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы можете просматривать запросы на вывод здесь.")

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)

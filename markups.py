from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(KeyboardButton('💰 Баланс'))
mainMenu.add(KeyboardButton('📊 Моя статистика'))
mainMenu.add(KeyboardButton('🔗 Моя реферальная ссылка'))
mainMenu.add(KeyboardButton('💸 Вывод'))

# Меню для вывода
def withdrawalMenu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('15'))
    markup.add(KeyboardButton('25'))
    markup.add(KeyboardButton('50'))
    return markup

# Меню для проверки подписки
checkSubMenu = ReplyKeyboardMarkup(resize_keyboard=True)
checkSubMenu.add(KeyboardButton("✅ Я подписался"))

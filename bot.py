import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 🔐 ТВОЙ ТОКЕН
TOKEN = "8454559980:AAGxR0SKsZPVqYfe1Q3k3I4-AgqMFCQNqC0"

# 🔗 Ссылка на товар в FunPay (замени на свою)
FUNPAY_URL = "https://funpay.com/chips/offer/123456/"  # ← ЗАМЕНИ НА СВОЮ ССЫЛКУ

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID файла премиум-конфига
PREMIUM_CONFIG_FILE_ID = None

# Статистика (временно в памяти)
DOWNLOAD_COUNT = 0
PREMIUM_SALES = 0
ANALYZE_REQUESTS = 0

# Стартовый экран
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 CS2", callback_data='game_cs2')],
        [InlineKeyboardButton("🚗 GTA V", callback_data='game_gta5')],
        [InlineKeyboardButton("🔫 Warzone", callback_data='game_warzone')],
        [InlineKeyboardButton("🟪 Fortnite", callback_data='game_fortnite')],
        [InlineKeyboardButton("🔺 Apex Legends", callback_data='game_apex')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚀 Привет! Я GameBoost AI — помогу оптимизировать твой ПК под игру.\n\nВыбери игру:",
        reply_markup=reply_markup
    )

# Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ Как пользоваться ботом:\n\n"
        "1. Выбери игру из меню.\n"
        "2. Получи инструкцию и базовый конфиг.\n"
        "3. Чтобы применить конфиг:\n"
        "   - Кликни ПКМ по .reg файлу\n"
        "   - Выбери “Запуск от имени администратора”\n"
        "   - Нажми “Да” → перезагрузи ПК\n\n"
        "4. Хочешь больше FPS? Купи премиум-конфиг через FunPay.\n"
        "5. После оплаты — напиши /check и пришли скрин.\n\n"
        "Команды:\n"
        "/start — Главное меню\n"
        "/help — Помощь\n"
        "/check — Проверить оплату\n"
        "/analyze — Прислать скрин для анализа\n"
        "/stats — Статистика бота"
    )

# Обработка выбора игры
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global DOWNLOAD_COUNT
    query = update.callback_query
    await query.answer()

    game = query.data

    if game == 'game_cs2':
        text = (
            "📌 Оптимизация для CS2:\n\n"
            "1. Панель управления → Электропитание → “Высокая производительность”\n"
            "2. NVIDIA/AMD Панель → “Максимальная производительность”\n"
            "3. Отключи Xbox Game Bar (Win+G → Настройки)\n"
            "4. В игре: Fullscreen, Shadows Low, FSR → Performance\n"
            "5. Закрой Discord overlay и браузеры.\n\n"
            "⬇️ Скачай автоматический оптимизатор (безопасно, можно откатить):"
        )
        config_file = "configs/cs2_basic.reg"

    elif game == 'game_gta5':
        text = (
            "📌 Оптимизация для GTA V:\n\n"
            "1. Электропитание → “Высокая производительность”\n"
            "2. NVIDIA: Power → Prefer max perf, VSync → Off\n"
            "3. В игре: FXAA/MSAA Off, Population Density → 0.5\n"
            "4. Отключи Steam Overlay\n"
            "5. Запускай от имени Администратора.\n\n"
            "⬇️ Скачай автоматический оптимизатор:"
        )
        config_file = "configs/gta5_basic.reg"

    elif game == 'game_warzone':
        text = (
            "📌 Оптимизация для Warzone:\n\n"
            "1. Электропитание → “Высокая производительность”\n"
            "2. NVIDIA: Power → Max perf, VSync → Off\n"
            "3. В игре: Fullscreen Exclusive, Shadows → Off\n"
            "4. Отключи все оверлеи (Discord, Steam)\n"
            "5. Добавь в ярлык: -d3d11 -fullscreen -refresh 144\n\n"
            "⬇️ Скачай автоматический оптимизатор:"
        )
        config_file = "configs/warzone_basic.reg"

    elif game == 'game_fortnite':
        text = (
            "📌 Оптимизация для Fortnite:\n\n"
            "1. Установи “Высокая производительность” в электропитании.\n"
            "2. NVIDIA: VSync → Off, Power management → Max perf\n"
            "3. В игре: 3D Resolution → Low, Shadows → Off\n"
            "4. Отключи оверлеи (Discord, GeForce Experience)\n"
            "5. Закрой фоновые приложения.\n\n"
            "⬇️ Скачай автоматический оптимизатор:"
        )
        config_file = "configs/fortnite_basic.reg"

    elif game == 'game_apex':
        text = (
            "📌 Оптимизация для Apex Legends:\n\n"
            "1. Электропитание → “Высокая производительность”\n"
            "2. NVIDIA: VSync → Off, Shader Cache → On\n"
            "3. В игре: Texture Streaming Budget → 2GB\n"
            "4. Отключи Origin Overlay\n"
            "5. Добавь в ярлык: -refresh 144 -fullscreen\n\n"
            "⬇️ Скачай автоматический оптимизатор:"
        )
        config_file = "configs/apex_basic.reg"

    # Отправляем инструкцию + файл
    with open(config_file, 'rb') as f:
        await query.message.reply_document(document=f, caption=text)
    
    # Увеличиваем счётчик скачиваний
    DOWNLOAD_COUNT += 1

    # Предлагаем купить премиум (только для CS2 в MVP)
    if game == 'game_cs2':
        buy_button = [[InlineKeyboardButton("💰 Купить CS2 ULTRA FPS BOOST (99₽)", callback_data='buy_premium')]]
        buy_markup = InlineKeyboardMarkup(buy_button)
        await query.message.reply_text(
            "🔥 Хочешь ещё больше FPS?\n\nПопробуй премиум-конфиг: +15–30% FPS, настройка сети, отключение телеметрии.\n\nЦена: 99₽",
            reply_markup=buy_markup
        )

# Обработка покупки через FunPay
async def buy_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PREMIUM_SALES
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💳 Чтобы купить премиум-конфиг, перейди по ссылке ниже и оплати вручную:\n\n"
        f"🔗 [Купить за 99₽ через FunPay]({FUNPAY_URL})\n\n"
        "После оплаты — напиши команду /check и пришли скриншот оплаты.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Перейти к оплате", url=FUNPAY_URL)]
        ])
    )
    
    # Увеличиваем счётчик продаж
    PREMIUM_SALES += 1

# Команда /check — пользователь присылает скрин
async def check_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Пришли скриншот оплаты, и я вручную вышлю тебе файл.\n\n"
        "Если хочешь — можешь написать: “Готово, оплатил”."
    )

# Автоответ на скриншоты
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"📸 Спасибо, {user.first_name}! Я получил скриншот. Проверю оплату и вышлю файл в течение 10 минут."
    )

# === НОВОЕ: ИИ-анализ (ручной) ===

# Команда /analyze
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ANALYZE_REQUESTS
    await update.message.reply_text(
        "📸 Пришли скриншот из игры (например, раунд в CS2), и я дам тебе совет по улучшению!"
    )
    ANALYZE_REQUESTS += 1

# Обработка скриншотов для анализа
async def handle_game_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"📸 Спасибо, {user.first_name}! Я получил скриншот. Через 5–10 минут пришлю тебе совет по улучшению игры."
    )
    # Здесь ты вручную смотришь скрин и отвечаешь

# === НОВОЕ: Статистика ===

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 Статистика бота:\n"
        f"⬇️ Скачано базовых конфигов: {DOWNLOAD_COUNT}\n"
        f"💰 Продано премиумов: {PREMIUM_SALES}\n"
        f"🕵️ Запросов на анализ: {ANALYZE_REQUESTS}"
    )

# Главная функция
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("check", check_payment))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(buy_premium, pattern='^buy_premium$'))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # Обработка скриншотов
    application.add_handler(MessageHandler(filters.PHOTO, handle_game_screenshot))  # Для анализа

    print("🚀 Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
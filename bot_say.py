from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Обработчик команды /start
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Отправьте мне текст, и я размещу его на картинке и отправлю вам.")

# Обработчик текстовых сообщений
def handle_text(update: Update, context):
    text = update.message.text
    print("Message: " + text + "\n\n")

    # Создание пути для сохранения изображения
    output_path = f'output_image_{update.message.chat_id}.jpg'

    # Создание изображения с размещенным текстом
    add_text_to_image('input.jpg', text, output_path, max_line_length=38)

    # Отправка изображения пользователю
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(output_path, 'rb'))

    # Удаление временных файлов
    os.remove(output_path)

# Функция для размещения текста на изображении
def add_text_to_image(image_path, text, output_path, max_line_length):

    # Загрузка изображения
    tile_image = Image.open(image_path)
    # Задание шрифта и размера текста
    font = ImageFont.truetype('Star_Rail.ttf', 20)  # Путь к шрифту и размер шрифта

    # Вычисление размеров изображения
    tile_width, tile_height = tile_image.size

    # Подготовка строк с текстом
    text_lines = []
    for line in (text.split('\n')):
        text_lines.extend(textwrap.wrap(line, width=max_line_length))

    # Вычисление размеров нового изображения
    tile_width, tile_height = tile_image.size
    new_height = tile_height * len(text_lines)

    # Создание нового изображения
    new_image = Image.new('RGB', (tile_width, new_height))

    # Замощение исходного изображения на новом изображении
    for y in range(0, new_height, tile_height):
        new_image.paste(tile_image, (0, y))

    # Создание объекта ImageDraw для рисования на изображении
    draw = ImageDraw.Draw(new_image)

    # Задание высоты установки первой строки
    y = 70 # Расчет идёт от верхнего края


    # Рисование текста на изображении
    for line in text_lines:
        x = 150 # Левая граница текста
        draw.text((x, y), line, font=font, fill='black')
        y += tile_height # Вместо text height использовать высоту изображения-тайла.

    # Сохранение нового изображения
    new_image.save(output_path)

# Открытие файла с токеном для чтения
with open('token.txt', 'r') as file:
    # Чтение значения из файла
    TOKEN = file.readline().strip()

print(TOKEN)

# Создание объекта Updater и передача токена
updater = Updater(token=TOKEN, use_context=True)

# Получение диспетчера для регистрации обработчиков
dispatcher = updater.dispatcher

# Регистрация обработчиков команд
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Регистрация обработчика текстовых сообщений
text_handler = MessageHandler(Filters.text, handle_text)
dispatcher.add_handler(text_handler)

# Запуск бота
updater.start_polling()

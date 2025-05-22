from flask import Flask, request, send_from_directory, render_template
import os
import uuid
import logging

# Настройка логирования
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создание экземпляра Flask
app = Flask(__name__)


# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')


# Маршрут для загрузки изображений
@app.route('/upload', methods=['POST'])
def upload():
    # Логирование начала загрузки
    logging.info("Upload request received.")

    # Получите загруженный файл
    file = request.files['file']
    if file:
        # Проверьте формат файла
        if file.filename.endswith(('.jpg', '.png', '.gif')):
            # Проверьте размер файла
            if file.content_length > 5 * 1024 * 1024:
                logging.warning("File size exceeds the limit of 5 MB.")
                return "File size exceeds the limit of 5 MB."

            # Создайте уникальное имя для файла
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            # Сохраните файл в папку /images
            file.save(os.path.join('images', filename))
            # Логирование успешного сохранения
            logging.info(f"Image {filename} uploaded successfully.")
            # Верните ссылку на загруженное изображение
            return f"Image uploaded successfully! URL: /images/{filename}"
        else:
            logging.warning("Unsupported file format.")
            return "Unsupported file format. Only .jpg, .png, and .gif are allowed."
    else:
        logging.warning("No file uploaded.")
        return "No file uploaded."


# Маршрут для доступа к загруженным изображениям
@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
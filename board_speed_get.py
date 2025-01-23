import requests
from datetime import datetime
import time
import os
import json
import argparse
import sys
from pathlib import Path
import tzlocal

class PostingSpeedDownloader:
    def __init__(self, url, rating_file="rating"):
        """
        Инициализация класса.
        :param url: URL сайта, с которого нужно скачать JSON.
        """
        self.url = url
        # Создаем файл рейтинга, если он не существует
        self.rating_file = Path(rating_file).stem + '.json'
        if not os.path.exists(self.rating_file):
            with open(self.rating_file, 'w') as f:
                json.dump([], f)  # Инициализируем пустым списком

    def download_json(self):
        """
        Скачивает JSON с указанного URL.
        :return: JSON-данные в виде словаря или None, если произошла ошибка.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Проверяем, что запрос успешен
            return response.json()  # Возвращаем JSON-данные
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке JSON: {e}")
            return None

    def get_posting_speed(self):
        """
        Извлекает данные о скорости постинга из JSON.
        :return: Список словарей в формате {'posts': количество_постов, 'datetime': дата_и_время}.
        """
        json_data = self.download_json()
        if not json_data:
            return []

        # Предполагаем, что данные о скорости постинга находятся в ключе 'speed'
        if 'board_speed' not in json_data:
            print("Ключ 'board_speed'не найден в JSON.")
            return []

        # Преобразуем данные в нужный формат
        #posting_speed_data = []
        try:
            posting_speed_data = {
                'board_speed': json_data['board_speed'],  # Количество постов за час
                'timestamp': time.time()  # Дата и время
            }
        except KeyError as e:
            print(f"Некорректный формат данных: {e}")

        return posting_speed_data

    def save_rating(self, new_entry):
        """
        Сохраняет новую запись в файл рейтинга.
        :param new_entry: Словарь с данными о скорости постинга.
        """
        try:
            # Читаем текущие данные из файла
            if os.path.exists(self.rating_file) and os.path.getsize(self.rating_file) > 0:
                with open(self.rating_file, 'r') as f:
                    try:
                        rating_data = json.load(f)
                    except json.JSONDecodeError:
                        print("Файл рейтинга поврежден. Инициализируем новый рейтинг.")
                        rating_data = []
            else:
                rating_data = []

            # Добавляем новую запись
            rating_data.append(new_entry)
            # Сохраняем обновленные данные обратно в файл
            with open(self.rating_file, 'w') as f:
                json.dump(rating_data, f, indent=4)

            print("Рейтинг успешно обновлен.")
        except Exception as e:
            print(f"Ошибка при сохранении рейтинга: {e}")

    def load_rating(self):
        """
        Загружает данные рейтинга из файла.
        :return: Список записей рейтинга.
        """
        try:
            if os.path.exists(self.rating_file) and os.path.getsize(self.rating_file) > 0:
                with open(self.rating_file, 'r') as f:
                    return json.load(f)
            else:
                print("Файл рейтинга пуст или отсутствует.")
                return []
        except json.JSONDecodeError:
            print("Файл рейтинга поврежден. Возвращаем пустой список.")
            return []
        except Exception as e:
            print(f"Ошибка при загрузке рейтинга: {e}")
            return []

# Пример использования
if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--filename", help="Файл json с логом", type=str, default="{board}")
    parser.add_argument("-ss", "--show-statistic", help="Выводить статистику в консоль", type=str, choices=["Y", "N"], default="Y")
    parser.add_argument("-i", "--interval", help="Интервал в минутах для обновления статистики", type=int, default=10)
    args = parser.parse_args()
    # Пример URL (замените на реальный URL)
    url = input('URL с json содержающий параметр board_speed: ')
    # Создаем объект и получаем данные о скорости постинга
    if args.filename == "" or args.filename == "{board}":
        filename = url.split('/')[-2]
    else:
        filename = args.filename
    downloader = PostingSpeedDownloader(url, filename)
    rating_last_index = 0
    while(True):
        try:
            posting_speed_data = downloader.get_posting_speed()
            if posting_speed_data:
                # Сохраняем новую запись в рейтинг
                downloader.save_rating(posting_speed_data)
                if args.show_statistic == 'Y':
                    # Загружаем и выводим текущий рейтинг
                    rating = downloader.load_rating()
                    if rating_last_index != 0:
                        rating = rating[rating_last_index:]
                    i = 0
                    for entry in rating:
                        i += 1
                        local_time = datetime.fromtimestamp(entry['timestamp'], tzlocal.get_localzone())
                        local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Постов за час: {entry['board_speed']}, Дата и время: {local_time}")
                    rating_last_index += i
        except Exception as e:
            print(e)
        time.sleep(60 * args.interval)

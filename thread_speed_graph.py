import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os
import json
import argparse
from pathlib import Path
import pytz
import sys
import time
import tzlocal

class PostingInThreadSpeedAnalyzer:
    def __init__(self, data, title = 'Скорость постинга', filename = 'posting_in_thread_speed.png', datetime_format = '%Y-%m-%d %H:%M:%S', timezone = 'UTC', interval_minutes = 0, interval_hours = 0, interval_days = 0, width = False, height = False):
        """
        Инициализация класса.
        :param data: Список словарей в формате {'board_speed': количество_постов, 'timestamp': timestamp}.
        """
        self.data = data
        self.title = title
        self.filename = filename
        self.datetime_format = datetime_format
        if timezone == 'local' or timezone == '' or timezone == False:
            timezone = tzlocal.get_localzone_name()
        try:
            self.timezone = pytz.timezone(timezone)
        except:
            print('Неправильный часовой пояс: ' + timezone)
            self.timezone = pytz.timezone(tzlocal.get_localzone_name())
        self.interval_minutes = interval_minutes
        self.interval_hours = interval_hours
        self.interval_days = interval_days
        self.interval_total_seconds = (interval_minutes * 60) + (interval_hours * 60 * 60) + (interval_days * 24 * 60 * 60)
        self.width = width
        if height <= 2 or height == None or height == False or height > 20:
            self.height = 6
        else:
            self.height = height

    def plot_posting_speed(self):
        """
        Строит график скорости постинга.
        """
        # Извлекаем данные
        dates = []
        posts = []
        prev_entry_datetime = False
        for entry in self.data:
            entry_datetime = datetime.fromtimestamp(entry['timestamp'], self.timezone)
            if prev_entry_datetime == False:
                prev_entry_datetime = entry_datetime
                dates.append(entry_datetime.strftime(self.datetime_format))
                posts.append(entry['posts_count'])
            else:
                difference = entry_datetime - prev_entry_datetime
                print(difference.total_seconds())
                if difference.total_seconds() >= self.interval_total_seconds:
                    dates.append(entry_datetime.strftime(self.datetime_format))
                    posts.append(entry['posts_count'])                
                    prev_entry_datetime = entry_datetime
        # Создаем график
        if self.width <= 3 or self.width == None or self.width == False or self.width > 30:
            len_dates = len(dates)
            if len_dates <= 10:
                plt.figure(figsize=(10, self.height))
            elif len_dates <= 15:
                plt.figure(figsize=(15, self.height))
            elif len_dates <= 20:
                plt.figure(figsize=(20, self.height))
            else:
                plt.figure(figsize=(25, self.height))
        else:
            plt.figure(figsize=(self.width, self.height))
        plt.plot(dates, posts, marker='o', linestyle='-', color='b')

        # Настройки графика
        plt.title(self.title)
        plt.xlabel('Дата и время (' + str(self.timezone) + ')')
        plt.ylabel('Количество постов')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Показываем график
        plt.savefig(self.filename)
        plt.show()

# Пример использования
if __name__ == "__main__":
    # Пример данных
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-b", "--board", help="Доска", type=str, default="")
    parser.add_argument("-dtf", "--datetime-format", help='Формат вывода даты и времени на графике', type=str, default="%Y-%m-%d %H:%M:%S")   
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="UTC")   
    parser.add_argument("-im", "--interval-minutes", help="Интервал в минутах для оси времени графика", type=int, default=0)  
    parser.add_argument("-ih", "--interval-hours", help="Интервал в часах для оси времени графика", type=int, default=0)  
    parser.add_argument("-id", "--interval-days", help="Интервал в днях для оси времени графика", type=int, default=0)  
    parser.add_argument("-w", "--width", help="Ширина графика (от 3 до 30)", type=int, default=0)  
    parser.add_argument("-h2", "--height", help="Высота графика (от 2 до 20)", type=int, default=0) 
    args = parser.parse_args()
    rating_file = os.path.abspath(input('Файл с json: '))
    if os.path.exists(rating_file) == False and Path(rating_file).suffix != '.json':
        rating_file = rating_file + '.json'
    if args.board != "":
        title = 'График скорости постинга в /' + args.board + '/res/' + Path(rating_file).stem + '.html'
    else:
        title = 'График скорости постинга в треде №' + Path(rating_file).stem
    try:
        if os.path.exists(rating_file) and os.path.getsize(rating_file) > 0:
            with open(rating_file, 'r') as f:
                data = json.load(f)
                # Создаем объект и строим график
                analyzer = PostingInThreadSpeedAnalyzer(data, title, Path(rating_file).stem, args.datetime_format, args.timezone, args.interval_minutes, args.interval_hours, args.interval_days, args.width, args.height)
                analyzer.plot_posting_speed() 
        else:
            print("Файл рейтинга пуст или отсутствует.")
            data = []
    except Exception as e:
        print(e)

Установка зависимостей: pip install -r requirements.txt

### Сбор статистики в разделе 
Анонимный форум должен отдавать board_speed в json раздела, чтобы скрипт мог собирать статистику.
```
usage: python board_speed_get.py [-h] [-f FILENAME] [-ss {Y,N}] [-i INTERVAL]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Файл json с логом (default: {board})
  -ss {Y,N}, --show-statistic {Y,N}
                        Выводить статистику в консоль (default: Y)
  -i INTERVAL, --interval INTERVAL
                        Интервал в минутах для обновления статистики (default: 10)
```
### Построение графика для оценки скорости постинга в разделе
```
usage: python board_speed_graph.py [-h] [-dtf DATETIME_FORMAT] [-tz TIMEZONE] [-im INTERVAL_MINUTES] [-ih INTERVAL_HOURS]
                                   [-id INTERVAL_DAYS]

options:
  -h, --help            show this help message and exit
  -dtf DATETIME_FORMAT, --datetime-format DATETIME_FORMAT
                        Формат вывода даты и времени на графике (default: %Y-%m-%d %H:%M:%S)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default: UTC)
  -im INTERVAL_MINUTES, --interval-minutes INTERVAL_MINUTES
                        Интервал в минутах для оси времени графика (default: 0)
  -ih INTERVAL_HOURS, --interval-hours INTERVAL_HOURS
                        Интервал в часах для оси времени графика (default: 0)
  -id INTERVAL_DAYS, --interval-days INTERVAL_DAYS
                        Интервал в днях для оси времени графика (default: 0)

```
### Сбор статистики в треде
Анонимный форум должен отдавать posts_count в json треда, чтобы скрипт мог собирать статистику.
```
usage: python thread_speed_get.py [-h] [-f FILENAME] [-ss {Y,N}] [-i INTERVAL]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Файл json с логом (default: {thread})
  -ss {Y,N}, --show-statistic {Y,N}
                        Выводить статистику в консоль (default: Y)
  -i INTERVAL, --interval INTERVAL
                        Интервал в минутах для обновления статистики (default: 10)
```
### Построение графика для оценки скорости постинга в треде
```
usage: python thread_speed_graph.py [-n] [-h] [-b BOARD] [-dtf DATETIME_FORMAT] [-tz TIMEZONE] [-im INTERVAL_MINUTES]
                                         [-ih INTERVAL_HOURS] [-id INTERVAL_DAYS]

options:
  -h, --help            show this help message and exit
  -b BOARD, --board BOARD
                        Доска (default: )
  -dtf DATETIME_FORMAT, --datetime-format DATETIME_FORMAT
                        Формат вывода даты и времени на графике (default: %Y-%m-%d %H:%M:%S)
  -tz TIMEZONE, --timezone TIMEZONE
                        Часовой пояс (local - локальный часовой пояс) (default: UTC)
  -im INTERVAL_MINUTES, --interval-minutes INTERVAL_MINUTES
                        Интервал в минутах для оси времени графика (default: 0)
  -ih INTERVAL_HOURS, --interval-hours INTERVAL_HOURS
                        Интервал в часах для оси времени графика (default: 0)
  -id INTERVAL_DAYS, --interval-days INTERVAL_DAYS
                        Интервал в днях для оси времени графика (default: 0)
```


Загрузите необходимые файлы из репозитория: скрипт с функциями practice.py, папку с access-логами и файл настроек logs.
Убедитесь, что на вашем компьютере установлены следующие компоненты: Python, Flask, sqlite3 и apache_log_parser.
Проверьте, что порт 5000 не используется другими приложениями.
Откройте терминал и запустите скрипт командой: python -i practice.py.
Чтобы загрузить логи в базу данных, вызовите функцию parse_logs(путь_к_логам), указав путь к файлу с логами.
Для отображения всех логов, хранящихся в базе данных, воспользуйтесь командой view_logs().
Чтобы выполнить поиск логов с использованием фильтров по дате, IP или статусу, используйте функцию view_logs() с нужными параметрами: view_logs('дата_начала', 'дата_окончания', 'ip', 'статус').
Для получения логов в формате JSON, выполните команду generate_get_logs_link() и перейдите по сгенерированной ссылке для просмотра всех данных.
Если хотите получить фильтрованные данные в формате JSON, вызовите generate_get_logs_link() с параметрами в виде словаря. Пример: generate_get_logs_link({'date_from': 'начальная_дата', 'date_to': 'конечная_дата', 'ip': 'ip', 'status': 'статус'}), затем откройте сгенерированную ссылку в браузере для просмотра результатов.

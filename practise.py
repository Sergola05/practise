from flask import Flask, request, jsonify
import sqlite3
import apache_log_parser
from datetime import datetime

# Подключение к БД + создание курсора
connection = sqlite3.connect('access_logs.db')
db_cursor = connection.cursor()

# Создание таблицы
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        logname TEXT,
        user TEXT,
        date TIMESTAMP,
        request TEXT,
        status INTEGER,
        bytes INTEGER
    )
''')
connection.commit()

def create_application():
    app = Flask(__name__)
    
    @app.route('/get_logs', methods=['GET'])
    def get_logs():
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        ip = request.args.get('ip')
        status = request.args.get('status')
    
        conn = sqlite3.connect('access_logs.db')
        cursor = conn.cursor()
    
        query = "SELECT * FROM access_logs WHERE 1=1"
        if date_from:
            query += f" AND date >= '{date_from}'"
        if date_to:
            query += f" AND date <= '{date_to}'"
        if ip:
            query += f" AND ip = '{ip}'"
        if status:
            query += f" AND status = '{status}'"

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Ошибка выполнения запроса: {e}')
        
        conn.close()
    
        logs = []
        for record in records:
            log_entry = {
                "ip": record[1],
                "date": record[4],
                "request": record[5],
                "status": record[6],
                "bytes": record[7]
            }
            logs.append(log_entry)
        
        return jsonify(logs)
    return app

app = create_application()

if __name__ == '__main__':
    def parse_logs(log_file_path):
        with open('logs/config.ini', 'r') as config_file:
            for line in config_file:
                if line.startswith('format:'):
                    log_format = line[len('format:'):].strip()[1:-1]
                    break
        
        print("Используемый формат из config.ini:", log_format)
        
        parser = apache_log_parser.make_parser(log_format)

        logs = []
        try:
            with open(log_file_path) as log_file:
                for log_entry in log_file:
                    parsed_entry = parser(log_entry)
                    logs.append(parsed_entry)
        except FileNotFoundError:
            print('Лог файл не найден')
        
        for entry in logs:
            ip = entry['remote_host']
            logname = entry['remote_logname']
            user = entry['remote_user']
            date_str = entry['time_received'][1:-1]
            date_format = "%d/%b/%Y:%H:%M:%S %z"
            log_date = datetime.strptime(date_str, date_format)
            request_line = entry['request_first_line']
            status_code = entry['status']
            response_bytes = entry['response_bytes']
            db_cursor.execute('''
                INSERT INTO access_logs (ip, logname, user, date, request, status, bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (ip, logname, user, log_date, request_line, status_code, response_bytes))
        
        connection.commit()

    def view_logs(date_from=None, date_to=None, ip=None, status=None):
        try:
            query = 'SELECT * FROM access_logs WHERE 1=1'
            params = []
        
            if date_from:
                query += ' AND date >= ?'
                params.append(date_from)

            if date_to:
                query += ' AND date <= ?'
                params.append(date_to)

            if ip:
                query += ' AND ip = ?'
                params.append(ip)

            if status:
                query += ' AND status = ?'
                params.append(status)

            db_cursor.execute(query, params)
            records = db_cursor.fetchall()
            print(records)
        
        except sqlite3.Error as e:
            print(f'Ошибка выполнения запроса: {e}')
        
        except Exception as ex:
            print(f'Общая ошибка: {ex}')

    def generate_get_logs_link(params=None):
        base_url = 'http://localhost:5000/get_logs'
        if params:
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
            link = f"{base_url}?{query_string}"
        else:
            link = base_url
        
        print(link)
        app.run()


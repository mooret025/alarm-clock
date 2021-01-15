import PySimpleGUI as sg
import sqlite3
from sqlite3 import Error
import datetime
import os
# Lab 25 Timestamping using date time

class AlarmClock:

    def __init__(self):
        pass

    def create_alarm(self):
        pass

    def edit_alarm(self):
        pass

    def delete_alarm(self):
        pass

    def play_sound(self):
        pass


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query, args):
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    # Create gui and instantiate alarm clock


def main():
    # Create DB to store alarms
    conn = create_connection('/Users/tyronemoore/Desktop/PycharmProjects/alarmClock/alarms.sqlite')

    # Creates alarms table
    # need to add alarm time to schema
    # and active flag either 1 or 0
    # and maybe add sound to alarm object
    create_alarms_table = """
    CREATE TABLE IF NOT EXISTS alarms (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date date,
      timestamp timestamp,
      alarm_time text,
      active INTEGER  
      );
    """
    execute_query(conn, create_alarms_table, '')

    today = datetime.date.today()
    now = datetime.datetime.now()

    # Create an alarm
    create_alarm = """
INSERT INTO
  alarms (date, timestamp, alarm_time, active)
VALUES
  (?, ?, ?, ?)
"""
    put_in_table = today, now, '', 1

    execute_query(conn, create_alarm, put_in_table)

    # Create clock

    hour_col = [[sg.Text('H', justification='center')], [sg.Spin(values=[x for x in range(00, 13)])]]
    min_col = [[sg.Text('M', justification='center')], [sg.Spin(values=[x for x in range(00, 60)])]]
    sec_col = [[sg.Text('S', justification='center')], [sg.Spin(values=[x for x in range(00, 60)])]]
    am_pm = [[sg.Text('AM/PM', justification='center')], [sg.Spin(values=['AM', 'PM'])]]

    layout = [[sg.Frame("Clock", [[sg.Col(hour_col), sg.Col(min_col), sg.Col(sec_col), sg.Col(am_pm)],
                                  [sg.Button('New'), sg.Button('Delete'),
                                   sg.Button("<< doesn't do anything")]])]]

    window = sg.Window('Test', layout)

    while True:  # Event Loop
        events, values = window.read()
        if events == sg.WIN_CLOSED:
            break
        if events == 'New':
            # Take input from user and insert into DB
            new = str(values[0]) + str(values[1]) + str(values[2]) + str(values[3])
            output = today, now, new, '1'
            execute_query(conn, create_alarm, output)

        if events == "<< doesn't do anything":
            os.system("say Delete does not do anything, but I say 'Delete does not do anything.'")



if __name__ == '__main__':
    main()

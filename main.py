import time
import threading
import PySimpleGUI as sg
from ossapi import Ossapi

# Global variable to hold the monitor thread
monitor_thread = None

def main():
    layout = [
        [sg.Text("Key:"), sg.Input(key='key')],
        [sg.Text("Secret Key:"), sg.Input(key='secret_key')],
        [sg.Text("Player:"), sg.Input(key='player')],
        [sg.Button("Start"), sg.Button("Exit")]
    ]

    window = sg.Window("osu! Rank Monitor", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Start':
            global monitor_thread
            # If there's a previous monitor thread, stop it before starting a new one
            if monitor_thread and monitor_thread.is_alive():
                monitor_thread.do_run = False
                monitor_thread.join()
            key = values['key']
            secret_key = values['secret_key']
            player = values['player']
            api = Ossapi(key, secret_key)
            monitor_thread = threading.Thread(target=monitor_rank, args=(api, player), daemon=True)
            monitor_thread.start()

    window.close()

def monitor_rank(api, player):
    global monitor_thread
    monitor_thread.do_run = True
    while getattr(monitor_thread, "do_run", True):
        rank = api.user(player).rank_history
        with open('rank_data.txt', 'w') as file:
            file.write(str(rank.data[-1]))
        print(rank.data[-1])
        print(api.user(9657753, mode="osu").username)
        time.sleep(3)

if __name__ == "__main__":
    main()

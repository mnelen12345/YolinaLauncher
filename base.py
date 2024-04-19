from pypresence import Presence
import subprocess
import json
import tkinter as tk
from tkinter import filedialog
import psutil
import random
import json
import time
from flask import Flask, render_template, jsonify
from werkzeug.serving import make_server
import threading
import tkinter as tk
from tkinter import ttk
import webview

RPC = None
current_game = None

image_urls = [
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/1.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/2.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/3.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/4.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/5.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/6.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/7.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/8.jpg",
    "https://raw.githubusercontent.com/mnelen12345/YolinaLauncher/main/large_image/9.jpg"
]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def open_html_interface():
    window = webview.create_window("YolinaLauncher", url="http://127.0.0.1:5000/", width=1410, height=720, resizable=False,)
    drpidle()
    webview.start()

def check_running_processes():
    global current_game, RPC
    running_processes = []
    for p in psutil.process_iter(['name'], ad_value=''):
        try:
            running_processes.append(p.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if "GenshinImpact.exe" in running_processes:
        current_game = "Genshin Impact"
        print("1")
    elif "StarRail.exe" in running_processes:
        current_game = "Honkai: Star Rail"
        print("2")
    elif "BH3.exe" in running_processes:
        current_game = "Honkai Impact 3rd"
        print("3")
    else:
        current_game = None
        if RPC:  # Проверяем, что RPC инициализирован
            RPC.update(state="Idle", details="In menu")
        print("4")
    time.sleep(5)

def create_rpc():
    global RPC
    RPC = Presence('1223969994824482879')
    try:
        RPC.connect()
        print("Discord Rich Presence подключен успешно.")
    except Exception as e:
        print("Ошибка при подключении к Discord Rich Presence:", e)

def launch_game(exe_path):
    subprocess.run([exe_path])

def select_game_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir="C:/", title="Выберите исполняемый файл игры")
    return file_path

def save_game_path(choice, game_path):
    try:
        with open('games.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[choice] = {"path": game_path}

    with open('games.json', 'w') as json_file:
        json.dump(data, json_file)

def load_game_path(choice):
    try:
        with open('games.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    game_path = data.get(choice, {}).get("path", None)
    return game_path

@app.route('/genshin_impact')
def genshin_impact():
    game_path = load_game_path('1')
    if game_path:
        drpgi()
        launch_game(game_path)
        drpidle()
    else:
        print("Путь к игре Genshin Impact не найден в файле games.json.")
        game_path = select_game_path()
        if game_path:
            save_game_path('1', game_path)
            drpgi()
            launch_game(game_path)
            drpidle()
        else:
            print("Не выбран путь к игре Genshin Impact.")

    result = {"message": "Genshin Impact function executed successfully!"}
    return jsonify(result)

@app.route('/honkai_star_rail')
def honkai_star_rail():
    game_path = load_game_path('2')
    if game_path:
        drphsr()
        launch_game(game_path)
        drpidle()
    else:
        print("Путь к игре Honkai: Star Rail не найден в файле games.json.")
        game_path = select_game_path()
        if game_path:
            save_game_path('2', game_path)
            drphsr()
            launch_game(game_path)
            drpidle()
        else:
            print("Не выбран путь к игре Honkai: Star Rail.")

    result = {"message": "Genshin Impact function executed successfully!"}
    return jsonify(result)

@app.route('/honkai_impact_3rd')
def honkai_impact():
    game_path = load_game_path('3')
    if game_path:
        drphi3rd()
        launch_game(game_path)
        drpidle()
    else:
        print("Путь к игре Honkai Impact 3rd не найден в файле games.json.")
        game_path = select_game_path()
        if game_path:
            save_game_path('3', game_path)
            drphi3rd()
            launch_game(game_path)
            drpidle()
        else:
            print("Не выбран путь к игре Honkai Impact 3rd.")

    result = {"message": "Genshin Impact function executed successfully!"}
    return jsonify(result)

def drpidle():
    RPC.update(state="idle", large_image=random.choice(image_urls), small_image="idle")

def drpgi():
    RPC.update(state="Playing Genshin Impact", large_image=random.choice(image_urls), small_image="gi")

def drphsr():
    RPC.update(state="Playing Honkai: Star Rail", large_image=random.choice(image_urls), small_image="hsr")

def drphi3rd():
    RPC.update(state="Playing Honkai Impact 3rd", large_image=random.choice(image_urls), small_image="hi3rd")

def run_flask_app():
    server = make_server('localhost', 5000, app)
    server.serve_forever()

def update_rpc():
    global RPC
    while True:
        time.sleep(5)

if __name__ == "__main__":
    create_rpc()

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    rpc_thread = threading.Thread(target=update_rpc)
    rpc_thread.start()

    open_html_interface()

    while True:
        check_running_processes()
        time.sleep(1)
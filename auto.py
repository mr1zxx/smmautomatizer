import os
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmmBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def login_smm(self):
        try:
            logging.info(f"{self.username}: Iniciando login no smm personalizado...")
            self.driver.get('smm target')

            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            password_input = self.driver.find_element(By.NAME, 'password')

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Feed de notícias']"))
            )
            logging.info(f"{self.username}: Login realizado com sucesso.")
        except TimeoutException:
            logging.error(f"{self.username}: Timeout durante o login. Verifique suas credenciais e conexão com a internet.")
        except NoSuchElementException:
            logging.error(f"{self.username}: Elemento de login não encontrado. Verifique a estrutura da página.")

    def follow_profile(self, profile_url):
        try:
            logging.info(f"{self.username}: Acessando perfil: {profile_url}")
            self.driver.get(profile_url)

            follow_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button//*[text()='Seguir']"))
            )
            follow_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button//*[text()='Seguindo']"))
            )
            logging.info(f"{self.username}: Seguindo o perfil: {profile_url}")
        except TimeoutException:
            logging.error(f"{self.username}: Timeout ao tentar seguir {profile_url}. A pagina esta certa?.")
        except NoSuchElementException:
            logging.error(f"{self.username}: Botão nao encontrado {profile_url}. A pagina esta certa?.")

    def close_browser(self):
        logging.info(f"{self.username}: Fechando o navegador.")
        self.driver.quit()

def run_bot(username, password, profiles):
    bot = SmmBot(username, password)
    bot.login_smm()
    for profile in profiles:
        bot.follow_profile(profile)
    bot.close_browser()

def start_bot_thread(username, password, profiles):
    bot_thread = threading.Thread(target=run_bot, args=(username, password, profiles))
    bot_thread.start()

def add_account():
    username = simpledialog.askstring("Input", "Digite o nome de usuário:")
    password = simpledialog.askstring("Input", "Digite a senha:", show='*')
    if username and password:
        accounts.append((username, password))
        accounts_listbox.insert(tk.END, username)

def add_profile():
    profile = simpledialog.askstring("Input", "Digite a URL do perfil:")
    if profile:
        profiles_to_follow.append(profile)
        profiles_listbox.insert(tk.END, profile)

def follow_profiles():
    for username, password in accounts:
        start_bot_thread(username, password, profiles_to_follow)

app = tk.Tk()
app.title("SMM Bot Manager")

accounts = []
profiles_to_follow = []

tk.Button(app, text="Adicionar Conta", command=add_account).pack()
tk.Button(app, text="Adicionar Perfil", command=add_profile).pack()
tk.Button(app, text="Seguir Perfis", command=follow_profiles).pack()

accounts_listbox = tk.Listbox(app)
accounts_listbox.pack()
profiles_listbox = tk.Listbox(app)
profiles_listbox.pack()

app.mainloop()

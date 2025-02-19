import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageDraw
from io import BytesIO
from weather import Weather
from user import User
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["Users"]
users = db["Forecast_Users"]

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Previsão Tempo')
        self.root.iconbitmap("assets/icone.ico")
        self.root.geometry("1200x720")
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.background = tk.Canvas(self.main_frame, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.place(x=0, y=0)

        self.user = None

        self.switch_frames(StartMenu)

    def create_rounded_button(self, canva, x1, y1, x2, y2, color, color_outline, command):

        width = int(x2 - x1)
        height = int(y2 - y1)

        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(5, 5), (width - 5, height - 5)],
            radius=20,
            fill=color,
            outline=color_outline,
            width=0
        )
        rounded_image = ImageTk.PhotoImage(image)
        button_image = canva.create_image(x1, y1, anchor="nw", image=rounded_image)

        if not hasattr(self, "_images"):
            self._images = []
        self._images.append(rounded_image)
        canva.tag_bind(button_image, "<Button-1>", lambda event, cmd=command: cmd())
        canva.tag_bind(button_image, "<Enter>", lambda event: canva.config(cursor="hand2"))
        canva.tag_bind(button_image, "<Leave>", lambda event: canva.config(cursor=""))

        return button_image


    def switch_frames(self, next_frame_class, *args, **kwargs):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_frame = next_frame_class(self.main_frame, self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
    
    def show_start_menu(self):
        self.switch_frames(StartMenu)

    def show_create_account(self):
        self.switch_frames(CreateAccount)

    def show_login(self):
        self.switch_frames(Login)
    
    def show_menu_weather(self):
        self.switch_frames(MenuWeather)
    
    def show_forecast(self, city, date_begin, date_end):
        self.switch_frames(Forecast, city, date_begin, date_end)

    def finish_program(self):
        self.main_frame.destroy()
        self.root.quit()

class StartMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.background = tk.Canvas(self, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.place(x=0, y=0)

        center_x = 1200 / 2
        center_y = 720 / 2

        self.controller.user = None

        self.background.create_text(center_x, 180, text="Previsão do Tempo", font=("Tahoma", 40, "bold"), fill="#FFFFFF")

        button_image = self.controller.create_rounded_button(self.background, center_x - 150, 250, center_x + 150, 310, "#001b71", "#1e1e1e", self.controller.show_create_account)
        text_id = self.background.create_text(center_x, 280, text="Criar Conta", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_create_account())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        button_image = self.controller.create_rounded_button(self.background, center_x - 150, 330, center_x + 150, 390, "#001b71", "#1e1e1e", self.controller.show_login)
        text_id = self.background.create_text(center_x, 360, text="Login", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_login())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        button_image = self.controller.create_rounded_button(self.background, center_x - 150, 410, center_x + 150, 470, "#001b71", "#1e1e1e", self.controller.finish_program)
        text_id = self.background.create_text(center_x, 440, text="Finalizar Programa", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.finish_program())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

class CreateAccount(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
    
        self.controller = controller

        self.background = tk.Canvas(self, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.place(x=0, y=0)

        center_x = 1200 / 2
        center_y = 720 / 2

        self.background.create_text(center_x, 180, text="Criar Conta", font=("Tahoma", 33, "bold"), fill="#FFFFFF")

        self.background.create_text(center_x, 250, text="Username", font=("Tahoma", 24, "bold"), fill="#FFFFFF")
        self.username_entry = tk.Entry(self, font=("Tahoma", 22), bg="#FFFFFF")
        self.username_entry.place(x=center_x, y=300, anchor="center")

        self.background.create_text(center_x, 350, text="Password", font=("Tahoma", 24, "bold"), fill="#FFFFFF")
        self.password_entry = tk.Entry(self, font=("Tahoma", 22), bg="#FFFFFF", show="*")
        self.password_entry.place(x=center_x, y=400, anchor="center")

        button_image = self.controller.create_rounded_button(self.background, center_x + 5, 450, center_x + 205, 510, "#001b71", "#1e1e1e", self.create_account)
        text_id = self.background.create_text(center_x + 110, 480, text="Criar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.create_account())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        button_image = self.controller.create_rounded_button(self.background, center_x - 205, 450, center_x - 5 , 510, "#001b71", "#1e1e1e", self.controller.show_start_menu)
        text_id = self.background.create_text(center_x - 110, 480, text="Voltar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_start_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not password or not username:
            messagebox.showerror("Erro", "Campos obrigatórios não preenchidos")

        elif users.find_one({"username": username}):
            messagebox.showerror("Erro", "Nome já em uso")

        else:
            user = User(username, password)
            users.insert_one(user.to_dict())
            messagebox.showinfo("Sucesso", "Conta criada com sucesso")
            self.controller.show_start_menu()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
    
        self.controller = controller

        self.background_image = Image.open("assets/background.webp")
        self.background_image = ImageTk.PhotoImage(self.background_image)

        self.background = tk.Canvas(self, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.place(x=0, y=0)

        center_x = 1200 / 2
        center_y = 720 / 2

        self.background.create_text(center_x, 180, text="Login", font=("Tahoma", 33, "bold"), fill="#FFFFFF")

        self.background.create_text(center_x, 250, text="Username", font=("Tahoma", 24, "bold"), fill="#FFFFFF")
        self.username_entry = tk.Entry(self, font=("Tahoma", 22), bg="#FFFFFF")
        self.username_entry.place(x=center_x, y=300, anchor="center")

        self.background.create_text(center_x, 350, text="Password", font=("Tahoma", 24, "bold"), fill="#FFFFFF")
        self.password_entry = tk.Entry(self, font=("Tahoma", 22), bg="#FFFFFF", show="*")
        self.password_entry.place(x=center_x, y=400, anchor="center")

        button_image = self.controller.create_rounded_button(self.background, center_x + 5, 450, center_x + 205, 510, "#001b71", "#1e1e1e", self.login)
        text_id = self.background.create_text(center_x + 110, 480, text="Entrar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.login())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        button_image = self.controller.create_rounded_button(self.background, center_x - 205, 450, center_x - 5 , 510, "#001b71", "#1e1e1e", self.controller.show_start_menu)
        text_id = self.background.create_text(center_x - 110, 480, text="Voltar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_start_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user = None

        if not password or not username:
            messagebox.showerror("Erro", "Campos obrigatórios não preenchidos")
            return
        
        user = users.find_one({"username": username})

        if user:
            if user["password"] == password:
                self.controller.user = user
                messagebox.showinfo("Sucesso", "Login realizado com sucesso")
                self.controller.show_menu_weather()
        else:
            messagebox.showerror("Erro", "Username ou senha incorretos")

class MenuWeather(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.background = tk.Canvas(self, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.place(x=0, y=0)

        center_x = 1200 / 2
        center_y = 720 / 2

        self.background.create_text(center_x, 180, text="Previsão Tempo", font=("Tahoma", 40, "bold"), fill="#FFFFFF")

        self.background.create_text(center_x, 250, text="Cidade", font=("Tahoma", 22, "bold"), fill="#FFFFFF", justify="left")
        self.city_entry = tk.Entry(self, font=("Tahoma", 20), bg="#FFFFFF")
        self.city_entry.place(x=center_x, y=300, anchor="center")

        self.background.create_text(center_x, 350, text="Data Início", font=("Tahoma", 22, "bold"), fill="#FFFFFF", justify="left")
        self.date_begin_entry = DateEntry(self, width=20, font=("Tahoma", 16, "bold"), foreground="#FFFFFF", borderwidth=2, date_pattern="yyyy-MM-dd")
        self.date_begin_entry.place(x=center_x, y=400, anchor="center")

        self.background.create_text(center_x, 450, text="Data Fim", font=("Tahoma", 22, "bold"), fill="#FFFFFF", justify="left")
        self.date_end_entry = DateEntry(self, width=20, font=("Tahoma", 16, "bold"), foreground="#FFFFFF", borderwidth=2, date_pattern="yyyy-MM-dd")
        self.date_end_entry.place(x=center_x, y=500, anchor="center")

        self.background.create_text(center_x - 350, 350, text="* Intervalo de dias não pode ser superior a 10", font=("Tahoma", 22, "bold"), fill="#FFFFFF", width=300)

        button_image = self.controller.create_rounded_button(self.background, center_x + 5, 550, center_x + 205, 610, "#001b71", "#1e1e1e", self.search_weather)
        text_id = self.background.create_text(center_x + 110, 580, text="Confirmar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.search_weather())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))
        
        button_image = self.controller.create_rounded_button(self.background, center_x - 205, 550, center_x - 5 , 610, "#001b71", "#1e1e1e", self.controller.show_start_menu)
        text_id = self.background.create_text(center_x - 110, 580, text="Voltar", font=("Tahoma", 22, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_start_menu())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))


    def search_weather(self):
        date_begin = self.date_begin_entry.get_date()
        date_end = self.date_end_entry.get_date()
        city = self.city_entry.get()

        if not city:
            messagebox.showinfo("Erro", "Nenhuma cidade digitada")
        elif (date_end - date_begin).days > 10:
            messagebox.showinfo("Erro", "Intervalo superior que 10 dias")
        else:
            self.controller.show_forecast(city, date_begin, date_end)

class Forecast(tk.Frame):
    def __init__(self, parent, controller, city, date_begin, date_end):
        super().__init__(parent)

        self.controller = controller
        self.city = city
        self.date_begin = date_begin
        self.date_end = date_end

        self.dates = [
            (self.date_begin + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((self.date_end - self.date_begin).days + 1)
        ]
        self.current_day_index = 0

        self.background = tk.Canvas(self, width=1200, height=720, bd=0, highlightthickness=0, background="#2f6bcb")
        self.background.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.display_day(self.current_day_index)

    def display_day(self, day_index):
        self.background.delete("all")

        center_x = 1200 / 2

        self.background.create_text(center_x, 83, text=f"{self.city}", font=("Tahoma", 33, "bold"), fill="#FFFFFF", anchor="center")
        self.background.create_text(center_x, 160, text="Previsão do Tempo", font=("Tahoma", 28, "bold"), fill="#FFFFFF", anchor="center")

        day = self.dates[day_index]
        formatted_date = datetime.strptime(day, "%Y-%m-%d").strftime("%d/%m/%Y")
        data = Weather.request_weather(self.city, day, self.controller.user)

        if "error" in data:
            self.background.create_text(center_x, 300, text="Cidade não existente", font=("Tahoma", 30, "bold"), fill="#FFFFFF", anchor="center")
        else:
            icon_url = "https:" + data["forecast"]["forecastday"][0]["day"]["condition"]["icon"]
            icon = self.weather_icon(icon_url)

            chance_of_rain = data["forecast"]["forecastday"][0]["day"].get("daily_chance_of_rain", 0)

            self.background.create_text(center_x, 250, text=f"Dia {formatted_date}", font=("Tahoma", 22, "bold"), fill="#FFFFFF", anchor="center")
            self.background.create_text(
                center_x, 300,
                text=f"{data['forecast']['forecastday'][0]['day']['mintemp_c']}°C - {data['forecast']['forecastday'][0]['day']['maxtemp_c']}°C",
                font=("Tahoma", 18), fill="#FFFFFF", anchor="center"
            )
            self.background.create_text(
                center_x, 350,
                text=data['forecast']['forecastday'][0]['day']['condition']['text'],
                font=("Tahoma", 18), fill="#FFFFFF", anchor="center"
            )
            self.background.create_image(center_x, 400, image=icon)
            self.background.image = icon
            self.background.create_text(
                center_x, 450,
                text=f"Chance de chuva: {chance_of_rain}%",
                font=("Tahoma", 18), fill="#FFFFFF", anchor="center"
            )

        self.add_navigation_buttons()

    def add_navigation_buttons(self):
        center_x = 1200 / 2

        if self.current_day_index > 0:
            self.controller.create_rounded_button(
                self.background, 50, 320, 150, 380,
                "#001b71", "#1e1e1e", self.show_previous_day
            )
            text_id = self.background.create_text(100, 350, text="Anterior", font=("Tahoma", 16, "bold"), fill="#FFFFFF")
            self.background.tag_bind(text_id, "<Button-1>", lambda event: self.show_previous_day())
            self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        if self.current_day_index < len(self.dates) - 1:
            self.controller.create_rounded_button(
                self.background, 1050, 320, 1150, 380,
                "#001b71", "#1e1e1e", self.show_next_day
            )
            text_id = self.background.create_text(1100, 350, text="Próximo", font=("Tahoma", 16, "bold"), fill="#FFFFFF")
            self.background.tag_bind(text_id, "<Button-1>", lambda event: self.show_next_day())
            self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
            self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

        self.controller.create_rounded_button(
            self.background, center_x - 100, 600, center_x + 100, 660,
            "#001b71", "#1e1e1e", self.controller.show_menu_weather
        )
        text_id = self.background.create_text(center_x, 630, text="Voltar", font=("Tahoma", 16, "bold"), fill="#FFFFFF")
        self.background.tag_bind(text_id, "<Button-1>", lambda event: self.controller.show_menu_weather())
        self.background.tag_bind(text_id, "<Enter>", lambda event: self.background.config(cursor="hand2"))
        self.background.tag_bind(text_id, "<Leave>", lambda event: self.background.config(cursor=""))

    def show_previous_day(self):
        if self.current_day_index > 0:
            self.current_day_index -= 1
            self.display_day(self.current_day_index)

    def show_next_day(self):
        if self.current_day_index < len(self.dates) - 1:
            self.current_day_index += 1
            self.display_day(self.current_day_index)

    def weather_icon(self, icon_url):
        response = requests.get(icon_url)
        
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img_tk = ImageTk.PhotoImage(img)

        return img_tk

root =  tk.Tk()

app = GUI(root)
root.mainloop()
import tkinter as tk
import threading
import time
import random
import requests
from io import BytesIO

class TaiXiuApp:
    def __init__(self, master):
        self.master = master
        master.title("Tool Tài Xỉu - BIGCHANG")

        # Đặt màu nền của cửa sổ
        master.configure(bg="#cd6a5a")

        # Đặt kích thước cửa sổ
        master.geometry("400x400")

        # Tạo khung chứa hình ảnh và tiêu đề
        self.image_frame = tk.Frame(master, bg="#cd6a5a")
        self.image_frame.pack()

        # Tạo Label cho hình ảnh
        self.image_label = tk.Label(self.image_frame, bg="#cd6a5a")
        self.image_label.pack()

        # Load hình ảnh từ URL
        self.load_image_from_url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0GCkHlITOBsFVaT4o0RmimdPxEIwmogxqvg&s", self.image_label)

        # Tạo Label cho tiêu đề
        self.title_label = tk.Label(master, text=" gg ", bg="#cd6a5a", fg="white", font=("Times New Roman", 16, "bold"))
        self.title_label.pack()

        self.label = tk.Label(master, text="Nhập số phiên:", bg="#cd6a5a", fg="white", font=("Times New Roman", 12))
        self.label.pack()

        self.entry = tk.Entry(master, font=("Times New Roman", 12))
        self.entry.pack()

        self.predict_button = tk.Button(master, text="Dự đoán", command=self.predict, bg="#cd6a5a", fg="white", font=("Times New Roman", 12))
        self.predict_button.pack()

        self.result_label = tk.Label(master, text="", bg="#cd6a5a", fg="white", font=("Times New Roman", 12))
        self.result_label.pack()

        self.xiu_canvas = tk.Canvas(master, width=50, height=50, bg="#cd6a5a", highlightthickness=0)
        self.xiu_canvas.place(x=300, y=100)
        self.xiu_canvas.create_oval(5, 5, 45, 45, fill="#cd6a5a", tags="xiu_light")

        self.xiu_label = tk.Label(master, text="Xỉu", fg="black", bg="#cd6a5a", font=("Times New Roman", 25, "bold"))
        self.xiu_label.place(x=295, y=45)

        self.tai_canvas = tk.Canvas(master, width=50, height=50, bg="#cd6a5a", highlightthickness=0)
        self.tai_canvas.place(x=50, y=100)
        self.tai_canvas.create_oval(5, 5, 45, 45, fill="#cd6a5a", tags="tai_light")

        self.tai_label = tk.Label(master, text="Tài", fg="black", bg="#cd6a5a", font=("Times New Roman", 25, "bold"))
        self.tai_label.place(x=48, y=45)

        self.blinking = False
        self.blink_thread = None

        # Tạo bàn phím ảo
        self.keyboard_frame = tk.Frame(master, bg="#cd6a5a")
        self.keyboard_frame.pack(pady=10)
        self.create_virtual_keyboard()

    def create_virtual_keyboard(self):
        buttons = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('0', 4, 1), ('C', 4, 0), ('Del', 4, 2)
        ]

        for (text, row, col) in buttons:
            if text == 'C':
                command = self.clear_entry
            elif text == 'Del':
                command = self.delete_last_char
            else:
                command = lambda t=text: self.insert_number(t)
            
            button = tk.Button(
                self.keyboard_frame, text=text, command=command, 
                font=("Arial", 12), width=5, height=2, bg="#ffffff"
            )
            button.grid(row=row, column=col, padx=5, pady=5)

    def insert_number(self, number):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_text + number)

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def delete_last_char(self):
        current_text = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_text[:-1])

    def predict(self):
        session_numbers = self.entry.get().strip()

        if not session_numbers:
            self.result_label.config(text="Vui lòng nhập số phiên.")
            return

        session_numbers = [int(num) for num in session_numbers.split()]

        self.result_label.config(text="Đang phân tích...")
        self.master.after(5000, lambda: self.wait_and_predict(session_numbers))

    def wait_and_predict(self, session_numbers):
        result = self.predict_outcome(session_numbers)
        self.result_label.config(text=f"Hãy đặt: {result}")
        if result == "Tài":
            self.blink_lights(self.tai_canvas)
        else:
            self.blink_lights(self.xiu_canvas)

    def predict_outcome(self, session_numbers):
        return "Xỉu" if random.random() < 0.5 else "Tài"

    def blink_lights(self, light):
        self.blinking = True
        if self.blink_thread is None or not self.blink_thread.is_alive():
            self.blink_thread = threading.Thread(target=self.blink, args=(light,))
            self.blink_thread.start()
        threading.Thread(target=self.turn_off_after_25_seconds).start()

    def blink(self, light):
        while self.blinking:
            light.itemconfig("xiu_light", fill="red") if light == self.xiu_canvas else light.itemconfig("tai_light", fill="red")
            self.master.after(200, lambda:light.itemconfig("xiu_light", fill="#cd6a5a") if light == self.xiu_canvas else light.itemconfig("tai_light", fill="#cd6a5a"))
            time.sleep(0.2)

    def turn_off_after_25_seconds(self):
        time.sleep(25)
        self.blinking = False
        self.master.after(0, lambda: self.xiu_canvas.itemconfig("xiu_light", fill="#cd6a5a") and self.tai_canvas.itemconfig("tai_light", fill="#cd6a5a"))

    def load_image_from_url(self, url, label):
        try:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            resized_image = image.resize((50, 50), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            label.config(image=photo)
            label.image = photo
        except Exception as e:
            print(f"Error loading image: {e}")

root = tk.Tk()
app = TaiXiuApp(root)
root.mainloop()
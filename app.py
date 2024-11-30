import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import threading
from playsound import playsound
from util import Netra
import serial
import time
from util import kosongin
import queue

class TabunganAppUI:
    def __init__(self):
        self.screenText=""
        self.screenTextTabungan=""
        self.isUserActive = False
        self.cameraResult = None
        self.cap = cv2.VideoCapture(0)
        self.root = tk.Tk()
        self.camera_label = Label(self.root)
        self.camera_label.pack()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.result_queue = queue.Queue()

    def greet(self):
        time.sleep(2)
        threading.Thread(target=lambda: playsound("audio/greet.mp3"), daemon=True).start()

    def reset(self):
        self.isUserActive=False
        self.cameraResult=None
        threading.Thread(target=lambda: playsound("audio/greet.mp3"), daemon=True).start()

    def capture(self):
        def run_scan(frame):
            result = Netra.scan(frame)
            self.result_queue.put({
                "id":"deteksi",
                "result":result
            })
            self.process_result()
        ret, frame = self.cap.read()
        if ret:
            threading.Thread(target=run_scan, args=(frame,), daemon=True).start()

    def captureTabung(self):
        res = Netra.tabung()
        self.result_queue.put({
            "id":'tabung',
            "result":f"Tabungan {res[0]} = Rp{res[1]}"
        })
        self.process_result()

    def process_result(self):
        if not self.result_queue.empty():
            result = self.result_queue.get()
            print(result)
            if result["id"]=="tabung":
                self.screenTextTabungan=result["result"]
            else:
                self.screenText=result["result"]

    def constructButton(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        reset = tk.Button(button_frame, text="Reset", command=self.reset)
        reset.pack(side=tk.LEFT, padx=10, pady=10)

        btn_laporan = tk.Button(button_frame, text="Laporan Uang", command=Netra.laporan)
        btn_laporan.pack(side=tk.LEFT, padx=10, pady=10)

        btn_tabungan = tk.Button(button_frame, text="Menabung Uang", command=self.captureTabung)
        btn_tabungan.pack(side=tk.LEFT, padx=10, pady=10)

        btn_capture = tk.Button(button_frame, text="Deteksi Uang", command=self.capture)
        btn_capture.pack(side=tk.LEFT, padx=10, pady=10)

    def show_camera(self):
        ret, frame = self.cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            text = self.screenText
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (255, 0, 0)
            thickness = 2
            position = (10, 30)
            cv2.putText(cv2image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
            # font second
            text = self.screenTextTabungan
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            color = (255, 0, 0)
            thickness = 2
            position = (10, 60)
            cv2.putText(cv2image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.camera_label.after(10, self.show_camera)

    def start_serial_listener(self):
        def listen_serial():
            arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
            time.sleep(5)
            print("ARDUINO CONNECTED")
            while True:
                if arduino.in_waiting:
                    packet = arduino.readline()
                    serialText = packet.decode('utf-8').rstrip()
                    if serialText == "btn.1":
                        print("Serial button pressed, capturing image")
                        self.capture()
                    elif serialText == "btn.2":
                        Netra.tabung()
                    elif serialText == "btn.3":
                        Netra.laporan()
                    elif serialText=="btn.4":
                        self.reset()
                    elif serialText=="jarak.1" and not self.isUserActive:
                        print("User Terdeteksi, Open App")
                        self.isUserActive=True
                        self.greet()
                        self.show_camera()
                        self.constructButton()
        threading.Thread(target=listen_serial, daemon=True).start()

# Initialize the app
kosongin.empty_folder("captured_images")
kosongin.empty_folder("audio/temp")
print("INITIALIZE APP")
Sistem = TabunganAppUI()
Sistem.root.title("TABITA SYSTEM")
Sistem.start_serial_listener()
print("TKINTER RUNNING")
Sistem.root.mainloop()

Sistem.cap.release()
cv2.destroyAllWindows()

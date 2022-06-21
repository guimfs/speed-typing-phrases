import tkinter as tk
import random
import time
import threading
from textwrap import wrap


class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Speed Typing Test')
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#CDAA7D")
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))

        self.phrases = open('phrases.txt', 'r').read().split('\n')

        self.frame = tk.Frame(self.root)
        self.frame.config(bg="#CDAA7D")

        self.title = tk.Label(self.frame, 
                            text="Type as fast as you can!", 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D",
                            fg="#8B1A1A")
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=70)

        self.label = tk.Label(self.frame, 
                            text=random.choice(self.phrases), 
                            font=("Gill Sans Ultra Bold", 25),
                            bg="#CDAA7D")
        self.label.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.speed = tk.Label(self.frame, 
                            text='0.00 Words per second\n0.00 Words per minute', 
                            font=("Gill Sans Ultra Bold", 20),
                            bg="#CDAA7D")
        self.speed.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.input = tk.Entry(self.frame, width=40, font=("Gill Sans Ultra Bold", 20))
        self.input.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.input.bind("<KeyPress>", self.start)

        self.reset = tk.Button(self.frame,
                            text='Reset', 
                            command=self.reset,
                            bg="#9C9C9C",
                            padx=100,
                            pady=25,
                            font=("Gill Sans Ultra Bold", 15),
                            activebackground='#345',
                            activeforeground='white',
                            borderwidth=3,
                            relief='raised',
                            )
        self.reset.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0

        self.running = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18, 27]: #Shift, Alt, Control, Esc
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.label.cget('text').startswith(self.input.get()):
            self.input.config(fg="red")
        else:
            self.input.config(fg="black")
        if self.input.get() == self.label.cget('text'):
            self.running = False
            self.input.config(fg="green")

    def time_thread(self):
        while self.running:
            time.sleep(0.01)
            self.counter += 0.01
            wps = len(self.input.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed.config(text=f'{wps:.2f} Words per second\n {wpm:.2f} Words per minute')

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed.config(text='0.00 Words per second\n0.00 Words per minute')
        self.label.config(text=random.choice(self.phrases))
        self.input.delete(0, tk.END)


if __name__ == '__main__':
    Interface()


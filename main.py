import tkinter as tk
import random
import time
import threading

class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Speed Typing Test')
        self.root.geometry('600x400')

        self.phrases = open('phrases.txt', 'r').read().split('\n')

        self.frame = tk.Frame(self.root)

        self.label = tk.Label(self.frame, text=random.choice(self.phrases))
        self.label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.speed = tk.Label(self.frame, text='0.00 Words per second\n0.00 Words per minute')
        self.speed.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.input = tk.Entry(self.frame, width=40)
        self.input.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input.bind("<KeyPress>", self.start)

        self.reset = tk.Button(self.frame, text='Reset', command=self.reset)
        self.reset.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0

        self.running = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]: #Shift, Alt, Control
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
            time.sleep(0.1)
            self.counter += 0.1
            wps = len(self.input.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed.config(text=f'{wps:.2f} Words per second\n {wpm:.2f} Words per minute')

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed.config(text='Speed: \n0.00 CPS\n0.00 CPM')
        self.label.config(text=random.choice(self.phrases))
        self.input.delete(0, tk.END)

Interface()


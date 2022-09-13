# # import threading
# # import queue
# # import random
# # import math
# # import time
# # import tkinter
# #
# # random.seed(0)
# #
# # class App:
# #     def __init__(self, queue, width=400, height=300):
# #         self.width, self.height = width, height
# #         self.canvas = tkinter.Canvas(width=width, height=height, bg='black')
# #         self.canvas.pack(fill='none', expand=False)
# #         self._oid = []
# #         self.canvas.after(10, self.move)
# #
# #         self.queue = queue
# #         self.canvas.after(50, self.check_queue)
# #
# #     def check_queue(self):
# #         try:
# #             x, y, rad, outline = self.queue.get(block=False)
# #         except queue.Empty:
# #             pass
# #         else:
# #             self.create_moving_ball(x, y, rad, outline)
# #         self.canvas.after(50, self.check_queue)
# #
# #     def move(self):
# #         width, height = self.width, self.height
# #         for i, (oid, r, angle, speed, (x, y)) in enumerate(self._oid):
# #             sx, sy = speed
# #             dx = sx * math.cos(angle)
# #             dy = sy * math.sin(angle)
# #             if y + dy + r> height or y + dy - r < 0:
# #                 sy = -sy
# #                 self._oid[i][3] = (sx, sy)
# #             if x + dx + r > width or x + dx - r < 0:
# #                 sx = -sx
# #                 self._oid[i][3] = (sx, sy)
# #             nx, ny = x + dx, y + dy
# #             self._oid[i][-1] = (nx, ny)
# #             self.canvas.move(oid, dx, dy)
# #         self.canvas.update_idletasks()
# #         self.canvas.after(10, self.move)
# #
# #     def create_moving_ball(self, x=100, y=100, rad=20, outline='white'):
# #         oid = self.canvas.create_oval(x - rad, y - rad, x + rad, y + rad,
# #                 outline=outline)
# #         oid_angle = math.radians(random.randint(1, 360))
# #         oid_speed = random.randint(2, 5)
# #         self._oid.append([oid, rad, oid_angle, (oid_speed, oid_speed), (x, y)])
# #
# # def queue_create(queue, running):
# #     while running:
# #         if random.random() < 1e-6:
# #             print ("Create a new moving ball please")
# #             x, y = random.randint(100, 150), random.randint(100, 150)
# #             color = random.choice(['green', 'white', 'yellow', 'blue'])
# #             queue.put((x, y, random.randint(10, 30), color))
# #         time.sleep(0) # Effectively yield this thread.
# #
# # root = tkinter.Tk()
# # running = [True]
# #
# # q = queue.Queue()
# #
# # app = App(q)
# # app.create_moving_ball()
# # app.canvas.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))
# #
# # thread = threading.Thread(target=queue_create, args=(q, running))
# # thread.start()
# #
# # root.mainloop()
#
# import time
# import threading, queue
#
# q = queue.Queue()
#
# def worker():
#     while True:
#         item = q.get()
#         print(f'Working on {item}')
#         print(f'Finished {item}')
#         q.task_done()
#
# # turn-on the worker thread
# threading.Thread(target=worker, daemon=True).start()
#
# # send thirty task requests to the worker
# for item in range(30):
#     q.put(item)
# print('All task requests sent\n', end='')
#
# # block until all tasks are done
# q.join()
# print('All work completed')

import tkinter as tk
from tkinter import ttk
# from ttk import *
import time
import queue, threading
from tkinter.ttk import Progressbar


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Demo')

    def show(self):
        self.progress = tk.IntVar()
        self.progress_max = 100
        self.progressbar = Progressbar(self.root, mode='determinate', orient=tk.HORIZONTAL, variable=self.progress,
                                       maximum=self.progress_max)
        self.progressbar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.progress.set(0)

        btn = tk.Button(self.root, text='start', command=self.start)
        btn.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.btn = btn

        self.root.mainloop()

    def start(self):
        self.progress.set(0)
        self.btn.config(state=tk.DISABLED)

        self.thread_queue = queue.Queue()  # used to communicate between main thread (UI) and worker thread
        new_thread = threading.Thread(target=self.run_loop, kwargs={'param1': 100, 'param2': 20})
        new_thread.start()

        # schedule a time-task to check UI
        # it's in main thread, because it's called by self.root
        self.root.after(100, self.listen_for_result)

    def run_loop(self, param1, param2):
        progress = 0
        for entry in range(self.progress_max):
            time.sleep(0.1)
            progress = progress + 1
            self.thread_queue.put(progress)

    def listen_for_result(self):
        '''
        Check if there is something in the queue.
        Must be invoked by self.root to be sure it's running in main thread
        '''
        try:
            progress = self.thread_queue.get(False)
            self.progress.set(progress)
        except queue.Empty:  # must exist to avoid trace-back
            pass
        finally:
            if self.progress.get() < self.progressbar['maximum']:
                self.root.after(100, self.listen_for_result)
            else:
                self.btn.config(state=tk.NORMAL)


if __name__ == '__main__':
    win = MainWindow()
    win.show()
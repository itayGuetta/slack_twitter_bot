#
#
#
# from tkinter import *
# from tkinter.ttk import *
# from time import strftime
#
#
# def helloCallBack():
#     print("hello")
#
#
#
# if __name__ == '__main__':
#     window = Tk()
#     window.geometry("500x200")
#
#     greeting = Label(text="Qmaster Slack-Twitter Bot ")
#
#     B = Button(window, text ="Now", command = helloCallBack)
#     greeting.pack()
#     B.pack()
#
#
#     def countdown(count):
#         # change text in label
#         label['text'] = count
#         if count > 0:
#             # call countdown again after 1000ms (1s)
#             window.after(1000, countdown, count - 1)
#
#
#
#
#     label = Label(window)
#     label.place(x=35, y=15)
#
#     # call countdown first time
#     countdown(5)
#     # root.after(0, countdown, 5)
#
#
#
#
#     window.mainloop()




# import tkinter as tk
#
# class ExampleApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.label = tk.Label(self, text="", width=10)
#         self.label.pack()
#         self.remaining = 0
#         self.countdown(60*60*60)
#
#     def countdown(self, remaining = None):
#         if remaining is not None:
#             self.remaining = remaining
#
#         if self.remaining <= 0:
#             # Send meassege to slack bot
#             self.label.configure(text="time's up!")
#         else:
#             self.label.configure(text="%d" % self.remaining)
#             self.remaining = self.remaining - 1
#             self.after(1000, self.countdown)
#
# if __name__ == "__main__":
#     app = ExampleApp()
#
#
#
#
#
#     app.mainloop()
# import time
# import tkinter as tk
# import datetime as dt
#
#
# class CountdownLabel(tk.Label):
#     """ A Label in the format of HH:MM:SS, that displays counting down from given
#     seconds.
#     """
#
#     def __init__(self, master, seconds_left):
#         super().__init__(master)
#         self._seconds_left = seconds_left
#         self._seconds_left_global = seconds_left
#         self._timer_on = False
#         self.label = tk.Label(self, text="", width=10,height=3, font=('times', 20, 'bold'))
#         self._countdown()                   # Start counting down immediately
#
#     def _start_countdown(self):
#         self._stop_countdown()
#         self._countdown()
#
#     def _stop_countdown(self):
#         if self._timer_on:
#             self.after_cancel(self._timer_on)
#             self._timer_on = False
#
#     def _countdown(self):
#         self['text'] = self._get_timedelta_from_seconds(self._seconds_left)
#         if self._seconds_left:
#             self._seconds_left -= 1
#             self._timer_on = self.after(1000, self._countdown)
#         if self._seconds_left <= 0:
#             self.label.configure(text="time's up!")
#             self.label.pack()
#             time.sleep(10)
#             self.label.destroy()
#             self._start_countdown()
#
#
#
#             #             # Send meassege to slack bot
#     #             self.label.configure(text="time's up!")
#
#     @staticmethod
#     def _get_timedelta_from_seconds(seconds):
#         return dt.timedelta(seconds=seconds)
#
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry("500x200")
#     greeting = tk.Label(text="Qmaster Slack-Twitter Bot ")
#     countdown = CountdownLabel(root, 4)
#     countdown.pack()
#     greeting.pack()
#     root.mainloop()
from datetime import datetime
import json
import tkinter as tk
import datetime as dt
from qmaster_bot_slack_twitter import slack_api


def read_config_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def Send_Massege_now(slack_client):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    slack_api.send_massage(slack_client)
    print("Send Message ! ")


class ExampleApp(tk.Tk):
    def __init__(self ,seconds_left,config_data):
        tk.Tk.__init__(self)
        self.slack_obj_client = slack_api.authenticate_slack(config_data)
        self.greeting = tk.Label(text="Qmaster Slack-Twitter Bot")
        self.button_now = tk.Button(self, text="Now", command= lambda: Send_Massege_now(self.slack_obj_client))
        self.greeting.pack()
        self.label = tk.Label(self, text="", width=10,height=3, font=('times', 20, 'bold'))
        self.label.pack()
        self.button_now.pack()
        self.remaining = 0
        self.countdown(seconds_left)
        self.seconds_left =seconds_left

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.countdown(self.seconds_left)
        else:
            time_format = self._get_timedelta_from_seconds(self.remaining)
            self.label.configure(text=time_format)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    @staticmethod
    def _get_timedelta_from_seconds(seconds):
        return dt.timedelta(seconds=seconds)


if __name__ == "__main__":
    path_to_config_file = "/qmaster_bot_slack_twitter/config.json"
    config_data = read_config_file(path_to_config_file)
    app = ExampleApp(60*60,config_data)
    app.geometry("500x200")
    app.mainloop()


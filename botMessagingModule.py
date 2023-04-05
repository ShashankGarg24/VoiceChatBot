import tkinter as tk


msg_list = None

def createMessageListBox(frame, y_scroll_bar, x_scroll_bar):
    msg_list = tk.Listbox(frame, height=20, width=50, yscrollcommand=y_scroll_bar.set, xscrollcommand=x_scroll_bar.set)
    msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
    msg_list.pack()


def insertMessage(msg):
    msg_list(tk.END, msg)
from tkinter import *


class App:
    def __init__(self):
        root = Tk()

        cv = Canvas(root, width=400, height=400, background="White")
        cv.pack()
        print(type(cv["width"]))
        print(cv.size())

        root.mainloop()


if __name__ == "__main__":
    a = App()

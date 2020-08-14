import os
import tempfile


class File:

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        if not os.path.exists(filename):
            with open(filename, 'w') as _:
                pass
        self.text = ""

    def __str__(self):
        return self.filename

    def read(self):
        try:
            with open(self.filename, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            text = ""
        return text

    def write(self, text):
        try:
            with open(self.filename, 'w') as f:
                return f.write(text)
        except FileNotFoundError:
            pass

    def __add__(self, other):
        new_file = os.path.join(tempfile.gettempdir(), str(tempfile.NamedTemporaryFile()))
        new_obj = File(new_file)
        new_text = self.read() + other.read()
        new_obj.write(new_text)
        return new_obj

    def __iter__(self):

        if os.path.getsize(self.filename) == 0:
            self.text_list = []
        else:
            text_list = self.read().split('\n')
            self.text_list = [value+'\n' for value in text_list if value != '']
        self.x = 0
        self.len = len(self.text_list)
        return self

    def __next__(self):
        if self.x == self.len:
            raise StopIteration

        res = self.text_list[self.x]
        self.x += 1
        return res

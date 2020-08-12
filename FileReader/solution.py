class FileReader:

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            text = ""
        return text





# override the DFA model in parser of filter

class model:
    """
    store funcs
    """
    def __init__(self):
        self.stack = []
        self.pos = 0
    
    def prev(self, step=1):
        self.pos -= step
    
    def next(self, step=1):
        self.pos += step
    
    

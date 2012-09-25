# override a DFA model 
# the self.model used in MyParser class of filter_content.py

class model:
    """ 
    # the self.model used in MyParser class of filter_content.py
    # setup an instance with push() method before use it
    
    lamF = lambda *pargs: False
    lamN = lambda *pargs: None
    """
    
    def __init__(self):
        self.stack = []
        self.pos = 0
    
    def push(self, *funcs):
        """ To store tuples of funcs in stack
        at most 4 funcs: (nextCond, prevCond, handleTag, handleData)
          if there is no func, set None in position
            otherwise all the funcs after that will be None
            
        handleTag, handleData:
          handle the data in the state
        
        nextCond, prevCond
          check whether goto next state.
          the return value(num) decide next state will be.
        """
        self.stack.append(funcs)
        
    """ To return handle func to user """
    def getHandleTag(self):
        try:
            #handle = self.stack[self.pos].handleTag
            handle = self.stack[self.pos][2]
        except IndexError:
            handle = None
        return handle
    
    def getHandleData(self):
        try:
            #handle = self.stack[self.pos].handleData
            handle = self.stack[self.pos][3]
        except IndexError:
            handle = None
        return handle

    """ To move the current state """
    def prev(self, *pargs):
        try:
            #func = self.stack[self.pos].prevCond
            func = self.stack[self.pos][1]
            if not func:
                return
        except IndexError:
            pass
        else:
            check = func(*pargs)
            if check:
                self.pos -= int(check)
            
    def next(self, *pargs): 
        try:
            #func = self.stack[self.pos].nextCond
            func = self.stack[self.pos][0]
            if not func:
                return
        except IndexError:
            pass
        else:
            check = func(*pargs)
            if check:
                self.pos += int(check)
                

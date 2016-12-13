class AtomicList:
    def __init__(self,alist,shallow_copy=True):
        self.original=alist
        self.shallow_copy=shallow_copy
    
    def __enter__(self):
        self.modified=(self.original[:] if self.shallow_copy else copy.copy.deepcopy(self.original))
        return self.modified
    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type is  None:
            self.original[:]=self.modified
        
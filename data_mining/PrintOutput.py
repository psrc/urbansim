
class PrintOutput :
    
    def __init__(self, logCB, progressCB, profiling):
        self.logCB = logCB
        self.progressCB = progressCB
        self.profiling = profiling
        
    def pLog(self, string):
        if self.logCB != None :
            self.logCB(string + "\n")
        if self.profiling != None :
            print string
            
    def progress(self, x):
        if self.progressCB != None:
            self.progressCB(x)
        
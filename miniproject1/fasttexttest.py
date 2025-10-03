import fasttext
class testing:

    def __init__(self):
        #self.modules=modules
        pass
        
    def print(self):
        model_en=fasttext.load_model("C:\Users\varun\Downloads\cc.en.300.bin")
        print(dir(model_en))
    
    
if __name__=="__main__":
    obj=testing()
    obj.print()
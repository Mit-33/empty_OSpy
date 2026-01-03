import os

class OSexplorer:
    def __init__(self,path:str=os.getcwd(),cd:bool=False):
        self.path = path
        self._cd = cd
        if self._cd:
            os.chdir(self.path)
    
    def ls(self):
        return os.listdir(self.path)

    def cd(self,path:str):
        path = os.path.normpath(path)
        if os.path.isabs(path):
            self.path = path
            if self._cd:
                os.chdir(self.path)
        elif os.path.isdir(os.path.join(self.path,path)):
            path = os.path.normpath(os.path.join(self.path,path))
            self.path = path
            if self._cd:
                os.chdir(self.path)
        else:
            raise FileNotFoundError("no such file or directory")
    
    def mkdir(self,path:str):
        os.mkdir(os.path.join(self.path,path))
    
    def mkfile(self,name:str):
        with open(os.path.join(self.path,name),"w"):
            pass
    
    def rmdir(self,path:str):
        os.rmdir(path)
    
    def rmfile(self,name:str):
        os.remove(os.path.join(self.path,name))
    
    def rename(self,oldname:str,newname:str):
        os.rename(os.path.join(self.path,oldname),os.path.join(self.path,newname))

    def open(self,file:str):
        if os.path.isfile(os.path.join(self.path,file)):
            try:
                with open(os.path.join(self.path,file)) as data:
                    return data.read()
            except UnicodeDecodeError:
                with open(os.path.join(self.path,file),"rb") as data:
                    return data.read()
        else:
            raise FileNotFoundError("no such file or directory")

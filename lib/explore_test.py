from OSexplorer import OSexplorer
import unittest

class TestOS(unittest.TestCase):

    def setUp(self):
        self.fe = OSexplorer()
    
    def test_all_cd(self):
        self.fe._cd = True
        self.assertTrue(type(self.fe.ls()) is list)
        self.fe.mkdir("myDir")
        self.assertTrue("myDir" in self.fe.ls())
        self.fe.cd("myDir")
        self.fe.mkfile("myFile")
        self.assertTrue("myFile" in self.fe.ls())
        self.assertTrue( (type(self.fe.open("myFile")) is str) or (type(self.fe.open("myFile")) is bytes))
        self.fe.rename("myFile","myFileRenamed")
        self.assertTrue("myFileRenamed" in self.fe.ls())
        self.fe.rmfile("myFileRenamed")
        self.assertTrue(self.fe.ls()==[])
        self.fe.cd("../")
        self.fe.rmdir("myDir")
        self.assertFalse("myDir" in self.fe.ls())
    
    def test_all(self):
        self.assertTrue(type(self.fe.ls()) is list)
        self.fe.mkdir("myDir")
        self.assertTrue("myDir" in self.fe.ls())
        self.fe.cd("myDir")
        self.fe.mkfile("myFile")
        self.assertTrue("myFile" in self.fe.ls())
        self.assertTrue( (type(self.fe.open("myFile")) is str) or (type(self.fe.open("myFile")) is bytes))
        self.fe.rename("myFile","myFileRenamed")
        self.assertTrue("myFileRenamed" in self.fe.ls())
        self.fe.rmfile("myFileRenamed")
        self.assertTrue(self.fe.ls()==[])
        self.fe.cd("../")
        self.fe.rmdir("myDir")
        self.assertFalse("myDir" in self.fe.ls())


if __name__ == '__main__':
    unittest.main()

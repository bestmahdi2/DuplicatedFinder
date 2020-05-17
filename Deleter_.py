from  os import sep, path, chdir, listdir, remove
from sys import argv
from send2trash import send2trash


class deleter:
    def __init__(self):
        self.answer = ""

    def mains(self,dele):
        self.maindir = '.' + sep
        absol = path.abspath(self.maindir)

        all = listdir(absol)
        dirs = []
        for f in all:
            if path.isdir(f):
                dirs.append(f)

        if len(dirs) != 0:
            for dir in dirs:
                chdir(absol + sep + dir)
                self.lister = listdir(self.maindir)
                self.lister = listdir(self.maindir)

                if "Right_Path.txt" in self.lister:
                    self.lister.remove("Right_Path.txt")

                if len(self.lister) > 1 :
                    self.deleter(dele,dir)
        print("\n===Done!===\n")
        input()


    def deleter(self,dele,dir):
        filetype = self.lister[0].replace(self.lister[0][:self.lister[0].rfind(".")], "")

        x = 0
        while x < len(self.lister):
            self.lister[x] = self.lister[x].replace(self.lister[x][self.lister[x].rfind("."):], "")
            x += 1

        # numberic = []
        mainFile = ""
        if len(self.lister) > 1:
            c = 0
            while c < len(self.lister):
                x = c + 1
                while x < len(self.lister):
                    if self.lister[x] in self.lister[c]:
                        mainFile = self.lister[x]
                    x += 1
                c += 1
            # print("m " , mainFile)

            if dele == "-p":
                if mainFile != "":
                    self.lister.remove(mainFile)
                    for name in self.lister:
                        remove(self.maindir + name + filetype)
                        print(dir + sep + name + filetype + " deleted.")

                if mainFile == "":
                    self.lister = sorted(self.lister)
                    self.lister.remove(self.lister[0])
                    for name in self.lister:
                        remove(self.maindir + name + filetype)
                        print(dir + sep + name + filetype + " deleted.")

            if dele == "-r":
                if mainFile != "":
                    self.lister.remove(mainFile)
                    for name in self.lister:
                        send2trash(self.maindir + name + filetype)
                        print(dir + sep + name + filetype + " moved to RecycleBin.")

                if mainFile == "":
                    self.lister = sorted(self.lister)
                    self.lister.remove(self.lister[0])
                    for name in self.lister:
                        send2trash(self.maindir + name + filetype)
                        print(dir + sep + name + filetype + " moved to RecycleBin.")


    def inputer(self):
        self.answer = input("\nDo you want your files to be moved to RecycleBin(yes) or Permanently(no) delete? (yes, no)\n >  ")
        if self.answer == "yes":
            d.mains("-r")
        elif self.answer == "no":
            d.mains("-p")
        else:
            print("\nWrong answer!!!")

if __name__ == '__main__':
    d = deleter()
    orders = argv[1:]
    if len(orders) == 0:
       d.inputer()
    if "-r" in orders and "-p" not in orders:
        d.mains("-r")
    elif "-p" in orders and "-r" not in orders:
        d.mains("-p")
    else:
        if d.answer == "":
            print("""\nUsage:   python Deleter.py [-r] [-p]
            -r                 Move to RecycleBin
            -p                 Permanently delete

        *NOTE : can't use both -r and -s together""")
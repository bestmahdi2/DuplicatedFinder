from  os import sep, path, chdir, listdir, remove
from sys import argv
# import  Send2Trash


class deleter:
    def __init__(self):
        self.answer = ""
    def mains(self,dele):
        print(dele)
        absol = path.abspath('./')

        all = listdir(absol)
        dirs = []
        for f in all:
            if path.isdir(f):
                dirs.append(f)

        if len(dirs) != 0:
            for dir in dirs:
                chdir(absol + sep + dir)
                lister = listdir("./")

                if "Right_Path.txt" in lister:
                    lister.remove("Right_Path.txt")


                if len(lister) > 1 :
                    filetype = lister[0].replace(lister[0][:lister[0].rfind(".")],"")

                    x = 0
                    while x < len(lister):
                        lister[x] = lister[x].replace(lister[x][lister[x].rfind("."):], "")
                        x += 1

                    # numberic = []
                    mainFile = ""
                    if len(lister) > 1:
                        c = 0
                        while c < len(lister):
                            x = c+1
                            while x < len(lister):
                                if lister[x] in lister[c]:
                                    mainFile = lister[x]
                                x += 1
                            c +=1
                        # print("m " , mainFile)

                        if mainFile != "":
                            lister.remove(mainFile)
                            for name in lister:
                                remove("./" + name + filetype)
                                print(dir + sep + name + filetype + " deleted.")

                        if mainFile == "":
                            lister = sorted(lister)
                            lister.remove(lister[0])

                            for name in lister:
                                remove("./" + name + filetype)
                                print(dir + sep + name + filetype + " deleted.")
        input()

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
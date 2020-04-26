import os
# import  Send2Trash

absol = os.path.abspath('./')

all = os.listdir(absol)
dirs = []
for f in all:
    if os.path.isdir(f):
        dirs.append(f)

if len(dirs) != 0:
    for dir in dirs:
        os.chdir(absol + os.sep + dir)
        lister = os.listdir("./")

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
                        os.remove("./" + name + filetype)
                        print(dir + os.sep + name + filetype + " deleted.")

                if mainFile == "":
                    lister = sorted(lister)
                    lister.remove(lister[0])

                    for name in lister:
                        os.remove("./" + name + filetype)
                        print(dir + os.sep + name + filetype + " deleted.")
input()
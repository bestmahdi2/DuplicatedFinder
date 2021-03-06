from os import makedirs, path, listdir, walk, sep, chdir, getcwd, remove
from sys import argv, exit
from hashlib import md5
from shutil import move,rmtree
from send2trash import send2trash
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from ProgramFile.DuplicateFinderQT import Ui_MainWindow

# Handle high resolution displays:
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class DuplicateFinder_GUI(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        # _translate = QtCore.QCoreApplication.translate


class DuplicateFinder:
    def __init__(self):
        self.filetype = set([])
        self.destinationDir = "duplicated_files" + sep
        print("\n### Duplicated File Finder ###\n")

    def find_dup(self, parentFolder):
        # Dups in format {hash:[names]}
        dups = {}
        for dirName, subdirs, fileList in walk(parentFolder):
            print('========\n\nScanning %s...' % dirName)
            for filename in fileList:
                # Get the path to the file
                path_ = path.join(dirName, filename)
                # Calculate hash
                file_hash = self.hashfile(path_)
                # Add or append the file path
                if file_hash in dups:
                    dups[file_hash].append(path_)
                else:
                    dups[file_hash] = [path_]
        return dups

    # Joins two dictionaries
    def join_dicts(self, dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]

    def hashfile(self, path, blocksize=65536):

        # open the file in binary
        afile = open(path, 'rb')
        hasher = md5()

        # read the file till "blocksize" byte.
        buf = afile.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()

    def print_results(self, dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))

        if len(results) > 0:
            print('\nDuplicates Found:')
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________\n')

            # Number of the directories which been made
            dir_num = 0

            for result in results:
                x = 1
                dir_num += 1
                to_print = []
                for subresult in result:
                    print('\t\t%s' % subresult.replace("\\",sep).replace("/",sep))
                    to_print.append(subresult.replace("\\",sep).replace("/",sep))
                    # absolute path of the file :
                    absulpath = path.abspath(subresult.replace("\\",sep).replace("/",sep))

                    filefullname = absulpath[absulpath.rfind(sep):]

                    # file with no format :
                    filename = filefullname[:filefullname.rfind(".")]

                    # just file format :
                    filetype = filefullname[filefullname.rfind("."):]

                    self.filetype.add(filetype)

                    makedirs(path.dirname(self.destinationDir +str(dir_num) + sep), exist_ok=True)
                    #

                    listd = listdir(self.destinationDir + str(dir_num))

                    if filefullname.replace(sep, "") not in listd:
                        move(absulpath, self.destinationDir + str(dir_num) + filefullname)
                    else:
                        move(absulpath, self.destinationDir + str(dir_num) + filename + "({" + str(x) + "})" + filetype)
                        x += 1

                # creat txt file for duplicated files' locations
                file = open(self.destinationDir + str(dir_num) + sep + "Right_Path.txt", "w",encoding="utf-8")
                for k in to_print:
                    try:
                        file.write(k + "\n")
                    except:
                        file.write("Couldn't write in this file because texts are not ASCII\n")
                file.close()

                print('___________________\n')
            print("All files have been moved to : " + self.destinationDir )
        else:
            print('\nNo duplicate files found.')

        # self.filetype = list(filter(None, self.filetype))

    def opendir(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(initialdir=".", title="Select Directory")
        return file_path

    def inputer(self):
        dups = {}
        print("Select the directory you want to search in for duplicated files.\n")
        address = self.opendir()
        if path.exists(address):
            self.join_dicts(dups, self.find_dup(address))
        else:
            print('%s is not a valid path, please verify' % address)
            input()
            exit()
        self.print_results(dups)
        if len(self.filetype) != 0:
            print("\nAll file types are : " + str(self.filetype).replace("{", "").replace("}", "")+"\n")

class deleter:
    def __init__(self):
        print("\n### File Deleter ###\n")
        self.answer = ""

        # print(str(getcwd()))

        if "duplicated_files" in listdir("."):
            self.pwdParent = getcwd()
            chdir("duplicated_files")
            self.pwd = getcwd()
        else:
            # region ask open folder
            input(
                "====\nThe [duplicated_files] couldn't be found ." + "\nClick [Enter] to select the folder manually.\n")
            if self.opendir() == "":
                input("You didn't choose a file, select again[Enter]\n")
                if self.opendir() == "":
                    print("Time out!!!")
                    input()
                    exit()
            chdir(self.pwd)
            # endregion
    def opendir(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(initialdir=".", title="Select Directory")
        self.pwd = file_path.replace("\\",sep).replace("/",sep)
        print(self.pwd)
        return file_path

    def mains(self,dele):
        self.maindir = self.pwd + sep

        all = listdir(self.maindir)
        dirs = [f for f in all if path.isdir(f)]

        if len(dirs) != 0:
            for dir in dirs:
                chdir(self.maindir + dir)
                self.lister = listdir(".")
                self.lister = listdir(".")

                if "Right_Path.txt" in self.lister:
                    self.lister.remove("Right_Path.txt")

                if len(self.lister) > 1 :
                    self.deleter(dele,dir)
        print("\n===Done!===\n")
        # input()

    def deleter(self,dele,dir):
        filetype = self.lister[0].replace(self.lister[0][:self.lister[0].rfind(".")], "")

        x = 0
        while x < len(self.lister):
            self.lister[x] = self.lister[x].replace(self.lister[x][self.lister[x].rfind("."):], "")
            x += 1

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
                        remove(self.maindir+dir +sep+ name + filetype)
                        print(dir + sep + name + filetype + " deleted.")

                if mainFile == "":
                    self.lister = sorted(self.lister)
                    self.lister.remove(self.lister[0])
                    for name in self.lister:
                        remove(self.maindir+dir +sep+ name + filetype)
                        print(dir + sep + name + filetype + " deleted.")

            if dele == "-r":
                if mainFile != "":
                    self.lister.remove(mainFile)
                    for name in self.lister:
                        send2trash(self.maindir+dir +sep+ name + filetype)
                        print(dir + sep + name + filetype + " moved to RecycleBin.")

                if mainFile == "":
                    self.lister = sorted(self.lister)
                    self.lister.remove(self.lister[0])
                    for name in self.lister:
                        send2trash(self.maindir+dir +sep+ name + filetype)
                        print(dir + sep + name + filetype + " moved to RecycleBin.")


    def inputer(self):
        self.answer = input("Do you want your files to be moved to RecycleBin(yes) or Permanently(no) delete? (yes, no)\n >  ")
        if self.answer == "yes":
            self.mains("-r")
        elif self.answer == "no":
            self.mains("-p")
        else:
            print("\nWrong answer!!!")

class bringer:
    def __init__(self,dir):
        print("\n### File Bringer ###\n")
        if dir != "":
            self.pwd = dir
            if not path.exists(dir):
        # region ask open folder
                input("====\nThe [duplicated_files] couldn't be found ." + "\nClick [Enter] to select the folder manually.\n")
                if self.opendir() == "":
                    input("You didn't choose a file, select again[Enter]\n")
                    if self.opendir() == "":
                        print("Time out!!!")
                        input()
                        exit()
        # endregion

        if dir == "":
            if "duplicated_files" in listdir("."):
                self.pwdParent = getcwd()
                chdir("duplicated_files")
                self.pwd = getcwd()
            else:
                # region ask open folder
                input(
                    "====\nThe [duplicated_files] couldn't be found ."+ "\nClick [Enter] to select the folder manually.\n")
                if self.opendir() == "":
                    input("You didn't choose a file, select again[Enter]\n")
                    if self.opendir() == "":
                        print("Time out!!!")
                        input()
                        exit()
                # endregion


        chdir(self.pwd)
        dirs = [i for i in listdir(".") if path.isdir(i) and "Right_Path.txt" in listdir(i)]
        # print(dirs)

        self.dirs = []
        self.counter = 0
        for i in dirs:
            chdir(self.pwd)
            self.bring(i)
            self.dirs.append(i)

        if self.counter > 0 :
            print(str(self.counter) + " file(s) brought back.")
        else:
            print("No file brought back.")

    def opendir(self):
        file_path = ""
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(initialdir=".", title="Select Directory")
        self.pwd = file_path.replace("\\",sep).replace("/",sep)
        return file_path

    def bring(self,dir):
        chdir(dir)
        self.counter += len(listdir("."))-1

        file_txt = open("Right_Path.txt", "r")
        Saved_loc = [i.replace("\n","") for i in file_txt.readlines() if i != ""]

        for file in listdir("."):
            absulpath = path.abspath(file)
            po_loc = []  # possible locations for a file
            fileO = file[:file.rfind("({")] + file[file.rfind("})"):].replace("})","")
            for loc in Saved_loc:
                if fileO in loc:
                    po_loc.append(loc)

            # print(po_loc)
            # print(fileO)
            # print(Saved_loc)

            if len(po_loc) == 1:
                # move(pwd+file,po_loc[0][:po_loc[0].rfind(sep)])
                move(absulpath , po_loc[0][:po_loc[0].rfind(sep)]+sep+fileO )
            if len(po_loc) >1 :
                x =0
                print("\nWhich location do you prefer to return (%s)?"%fileO)
                while x < len(po_loc):
                    print(str(x+1)+") "+po_loc[x])
                    x +=1
                answer = int(input(" > "))
                move(absulpath , po_loc[answer-1][:po_loc[answer-1].rfind(sep)]+sep+fileO)

    def deleter(self):
        chdir(self.pwd)
        for dir in self.dirs:
            rmtree(dir,ignore_errors=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    MainWindow = QtWidgets.QMainWindow()

    ui = DuplicateFinder_GUI()
    ui.setupUi(MainWindow)

    MainWindow.show()
    exit(app.exec_())

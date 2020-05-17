from os import makedirs, path, listdir, walk , sep
from sys import argv, exit
from hashlib import md5
from shutil import move


class Mains:
    def __init__(self):
        self.destinationDir = "duplicated_files" + sep
        print("\n### Duplicated Files ###\n")

    def find_dup(self, parentFolder):
        # Dups in format {hash:[names]}
        dups = {}
        for dirName, subdirs, fileList in walk(parentFolder):
            print('Scanning %s...' % dirName)
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
        afile = open(path, 'rb')
        hasher = md5()
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
            print('\n___________________\n')

            # Number of the directories which been made
            dir_num = 0

            for result in results:
                x = 1
                dir_num += 1
                to_print = []
                for subresult in result:
                    print('\t\t%s' % subresult)
                    to_print.append(subresult)
                    # absolute path of the file :
                    absulpath = path.abspath(subresult)

                    filefullname = absulpath[absulpath.rfind(sep):]
                    # file with no format :
                    filename = filefullname[:filefullname.rfind(".")]
                    # just file format :
                    filetype = filefullname[filefullname.rfind("."):]

                    makedirs(path.dirname(self.destinationDir + str(dir_num) + sep), exist_ok=True)

                    listd = listdir(self.destinationDir + str(dir_num))

                    if filefullname.replace(sep, "") not in listd:
                        move(absulpath, self.destinationDir + str(dir_num) + filefullname)
                    else:
                        move(absulpath, self.destinationDir + str(dir_num) + filename + "(" + str(x) + ")" + filetype)
                        x += 1

                # creat txt file for duplicated files' locations
                file = open(self.destinationDir + str(dir_num) + sep + "Right_Path.txt", "w",encoding="utf-8")
                for k in to_print:
                    try:
                        file.write(k + "\n")
                    except:
                        file.write("Couldn't write in this file because texts are not ASCII\n")
                file.close()

                print('\n___________________\n')
            print("\nAll files have been moved to : " + self.destinationDir + "\n" )
        else:
            print('\nNo duplicate files found.')


if __name__ == '__main__':
    M = Mains()
    if len(argv) > 1:
        dups = {}
        folders = argv[1:]
        for folder in folders:
            # Iterate the folders given
            if path.exists(folder):
                # Find the duplicated files and append them to the dups
                M.join_dicts(dups, M.find_dup(folder))
            else:
                print('%s is not a valid path, please verify' % folder)
                exit()
        M.print_results(dups)
    else:
        print("&^% Wrong %^&\n")
        print('Usage: python dupFinder.py folder *OR* python dupFinder.py folder1 folder2 folder3')
    input()
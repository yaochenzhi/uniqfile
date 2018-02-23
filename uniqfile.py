import os
import sys
import hashlib
from colorama import init as colorinit
from termcolor import colored
# import logging


def print_usage():
    print("Usage: python {script} {{target_dir}}".format(script=sys.argv[0]))


def main():

    colorinit()

    try:
        target_dir = sys.argv[1]
    except IndexError:
        print_usage()
    else:
        if not os.path.isdir(target_dir):
            print_usage()
        else:
            ## ------ filter the repeated ----------------------
            hashes = {}
            # the repeated
            repeated = {}
            # count for all file no matter repeated or not 
            file_count = 0
            for root, dirs, files in os.walk(target_dir):
                if root == target_dir:
                    for file in files:
                        # print(file)
                        # print(os.path.join(root, file))
                        m = hashlib.md5()
                        with open(os.path.join(root, file), 'rb') as f:
                            while True:
                                buff = f.read(2048)
                                if not buff:
                                    break
                                m.update(buff)
                        # returned md5 is of string format
                        md5 = m.hexdigest()

                        ## ---------------print item process-----------------
                        file_count += 1
                        filesize = round(os.path.getsize(os.path.join(root, file)) / (1024 * 1024), 2)
                        print(str(file_count) + ":\t", file + "\t" + str(filesize) + "M" + "\t" + md5)

                        try:
                            first = hashes[md5]
                        except KeyError:
                            hashes[md5] = file
                        else:
                            try:
                                existed = repeated[md5]
                            except KeyError:
                                repeated[md5] = [first, file]
                            else:
                                repeated[md5].append(file)
            ## ------ print the repeated ----------------------
            for key, value in repeated.items():
                print("File(s)\t{}\tis repeated with md5\t{}\t!".format(colored(value, 'green'), colored(key, 'red')))


if __name__ == '__main__':
    main()
    # print_usage()
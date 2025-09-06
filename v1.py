import glob
import re
from PIL import Image

# Python code to iterate over all the png images and generate bad-apple.c


def print_header():
    print("#include <stdio.h>")
    print("#include <unistd.h>")
    print("int main(int argc, char** argv) {")


def print_footer(delay):
    if delay > 0:
        print("usleep({0});".format(delay))
    print("}")


def process_png_files():
    """
    Read the png files and print a #define statement for each file.
    """
    files = glob.glob("frames-png/*")
    files.sort()
    for file in files:
        id = re.findall("\\d+", file)[0]
        with Image.open(file) as img:
            pixels = list(img.getdata(0))
            if id == "0001":
                print("#if defined frame{0}".format(id))
            else:
                print("#elif defined frame{0}".format(id))
            print("(int)\"[2J[2H", end="")
            for j in range(0, img.height):
                for i in range(0, img.width):
                    if pixels[j * img.width + i] >= 128:
                        print("█", end="")
                    else:
                        print(" ", end="")
                print("[1E", end="")
            print("[1E                                                            {0}[1E".format(
                id), end="")
            print("\";")
            print(
                "printf(\"gcc -o %s -Dframe{0:04d} bad-apple.c\\n\", argv[0]);".format(int(id) + 1))
    print("#else")
    print("printf(\"gcc -o %s -Dframe0001 bad-apple.c\\n\", argv[0]);")
    print("#endif")


def print_file(delay):
    print_header()
    process_png_files()
    print_footer(delay)


print_file(delay=0)

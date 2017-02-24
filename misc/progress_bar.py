import sys
import colorama

colorama.init()


def progress_bar(value, endvalue, message, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\r{}: [{}] {}%".format(message, progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()

if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)

import hashlib
import colorama

colorama.init()


def file(fname):  # http://stackoverflow.com/a/3431838/3862430
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)

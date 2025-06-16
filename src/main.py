import textnode
import os
import shutil

def main():
    #node = textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    #print(node)
    wipe_dir("public")
    copy_dir("static", "public")

def copy_dir(src, to):
    if not os.path.exists(src):
        raise Exception(f"copy_dir: source path {src} does not exist")
    if not os.path.exists(to):
        os.mkdir(to)
    elif not os.path.isdir(to):
        raise Exception(f"copy_dir: destination path {to} is not a directory")
    dir = os.listdir(src)
    for entry in dir:
        fullsrc = os.path.join(src, entry)
        fullto =  os.path.join(to, entry)
        if os.path.isfile(fullsrc):
            #print(f"{fullsrc} -> {fullto}")
            shutil.copy(fullsrc, fullto)
        elif os.path.isdir(fullsrc):
            copy_dir(fullsrc, fullto)

def wipe_dir(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise Exception(f"wipe_dir: path {path} is not a regular file or directory")
    os.mkdir(path)

main()

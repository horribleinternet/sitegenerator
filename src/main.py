import sys
import os
import io
import shutil
import markdown
import nodeconvert

def main():
    #node = textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    #print(node)
    basepath = None
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if basepath == "" or basepath == None:
        basepath = "/"
    
    wipe_dir("docs")
    copy_dir("static", "docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")

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

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    title = ""
    htmlnode = None
    with io.open(from_path) as markdown_file:
        markdown_text = markdown_file.read()
        title = markdown.extract_title(markdown_text)
        htmlnode = nodeconvert.markdown_to_html_node(markdown_text)
    output_text = ""
    with io.open(template_path) as template_file:
        output_text = template_file.read()
    output_text = output_text.replace(r"{{ Title }}", title, 1)
    output_text = output_text.replace(r"{{ Content }}", htmlnode.to_html())
    #print(f'href={basepath}')
    output_text = output_text.replace('href="/', f'href="{basepath}')
    output_text = output_text.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with io.open(dest_path, mode="w") as output_file:
        output_file.write(output_text)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    entrys = os.listdir(dir_path_content)
    #print(entrys)
    for entry in entrys:
        full_content_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(full_content_path):
            generate_pages_recursive(basepath, full_content_path, template_path, os.path.join(dest_dir_path, entry))
        elif os.path.isfile(full_content_path):
            split_type = entry.rsplit(".", 1)
            if split_type[1] == "md":
                generate_page(basepath, os.path.join(full_content_path), template_path, os.path.join(dest_dir_path, split_type[0]+".html"))

main()

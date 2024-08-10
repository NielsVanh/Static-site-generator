from textnode import TextNode
from htmlnode import LeafNode
from block_converter import *
from node_converter import *

import os
import shutil
from re import *

def copy_source_to_destination(source, destination):
    shutil.rmtree(destination)
    os.mkdir(destination)
    if os.path.exists(source):
        source_dir_paths = os.listdir(source)
        for path in source_dir_paths:
            source_path = source + "/" + path
            if os.path.isdir(source_path):
                destination_dir_path = destination + "/" + path
                os.mkdir(destination_dir_path)
                copy_source_to_destination(source + "/" + path, destination_dir_path)
            else:
                shutil.copy(source_path, destination)

def extract_title(markdown):
    if findall(r"<h1>.*</h1>", markdown):
        return findall(r"(<h1>.*</h1>)", markdown)[0]
    else:
        raise Exception("There is no h1 header.")
    
def generate_page(from_path, template_path, dest_path):
    print("Generating page from from_path to dest_path using template_path")
    if os.path.exists(from_path) and os.path.exists(template_path) and os.path.exists(dest_path):
        new_dest_path = dest_path + "/index.html"
        with open(from_path) as markdown_file:
            markdown = markdown_file.read()
            markdown_file.close()
            with open(template_path) as template_file:
                template = template_file.read()
                nodes = markdown_to_html_node(markdown)
                string = nodes.to_html()
                title = extract_title(string)
                content_list = findall(r"<html><h1>.*</h1>((.*\n?)*)</html>", string)
                content_tuple = content_list[0]
                content = content_tuple[0]
                new_template = template.replace(r"{{ Title }}", title)
                new_template = new_template.replace(r"{{ Content }}", content)
                template_file.close()
                with open(new_dest_path, "x") as index:
                    index.write(new_template)
                    index.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(dir_path_content) and os.path.exists(template_path) and os.path.exists(dest_dir_path):
        content_dir_paths = os.listdir(dir_path_content)
        for path in content_dir_paths:
            content_path = dir_path_content + "/" + path
            if os.path.isfile(content_path):
                generate_page(content_path, template_path, dest_dir_path)
            else:
                destination_dir_path = dest_dir_path + "/" + path
                os.mkdir(destination_dir_path)
                generate_pages_recursive(content_path,template_path, destination_dir_path)

def main():
    scource = "/home/niels/workspace/github.com/NielsVanh/staticSiteGenerator/static"
    destination = "/home/niels/workspace/github.com/NielsVanh/staticSiteGenerator/public"
    copy_source_to_destination(scource, destination)
    
    from_path = "/home/niels/workspace/github.com/NielsVanh/staticSiteGenerator/content"
    temp_path = "/home/niels/workspace/github.com/NielsVanh/staticSiteGenerator/template.html"
    dest_path = "/home/niels/workspace/github.com/NielsVanh/staticSiteGenerator/public"
    generate_pages_recursive(from_path, temp_path, dest_path)

main()

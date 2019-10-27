from datetime import datetime
import os
import xml.etree.ElementTree as xml
import py7zlib

import time


class dataset_helper:

    def __init__(self):
        pass


def extract_data():
    path = "D://Masters//Sem 1//5751- Big Data//project//Final_project_stackexhange//windows_phone"
    for filename in os.listdir(path):
        data_source = os.path.join(path, filename)
        if filename == "PostLinks.xml":
            postlinks_file = data_source;
        elif filename == "Users.xml":
            users_file = data_source
        elif filename == "Posts.xml":
            posts_file = data_source

    return users_file, posts_file, postlinks_file



if __name__ == '__main__':
    path = "D://Masters//Sem 1//5751- Big Data//project//Final_project_stackexhange//windows_phone"
    data_source = "D:\Internship and placement\study material\leetcode github\Pegasus\Stage1"

    walk = os.walk(data_source)
    data_source_directories = [x for x in walk]
    data_source_directories = data_source_directories[0]

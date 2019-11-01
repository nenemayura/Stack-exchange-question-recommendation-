from datetime import datetime
import os
import xml.etree.ElementTree as xml
import py7zlib

import time


class dataset_helper:

    def __init__(self):
        pass


def extract_data():

    # path for the dataset
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


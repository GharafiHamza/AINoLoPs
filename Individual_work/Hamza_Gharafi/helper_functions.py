import pandas as pd
import numpy as np
import json
import os
import time

project_main_path = os.getcwd().split(os.sep)
project_main_path = project_main_path[:-2]
project_main_path = os.path.join(*project_main_path)
project_main_path = os.sep+os.path.join(project_main_path)
individual_work_path = os.path.join(project_main_path, 'Individual_work')
data_path = os.path.join(project_main_path, 'data')
users_metadata_path = os.path.join(data_path, 'users_metadata')
users_metadata_files = [os.path.join(users_metadata_path, i) for i in os.listdir(users_metadata_path)]
t5_data_path = os.path.join(data_path, 'subtask-5A-arabic')
lists_metadata_path = os.path.join(t5_data_path, 'lists_metadata')
lists_metadata_files = [os.path.join(lists_metadata_path, i) for i in os.listdir(lists_metadata_path)]
dev_rumors_path = os.path.join(t5_data_path, 'dev_rumors.json')
train_rumors_path = os.path.join(t5_data_path, 'train_rumors.json')
relevance_judgment_path = os.path.join(t5_data_path, 'relevance_judgments.txt')

users_json_map = pd.read_csv(os.path.join(individual_work_path, 'users_json_map.csv'))

def get_user_metadata(user_id, users_json_map=users_json_map, users_metadata_path=users_metadata_path):
    row = users_json_map.loc[users_json_map['user_id'] == user_id]
    file_name = row.file_name.item()
    file_name = os.path.join(users_metadata_path, file_name)
    file_df = pd.read_json(file_name)
    user_data = file_df.loc[file_df['user_id'] == user_id]
    return user_data

def print_help():
    print('''This file is purely a helper file to help us navigate through the data, and the following is some instruction or in some sort a manual on how to use it:
    "Note : I have loded the users_metadata directly into the 'data' directory inside the main directory i recomend you to do the same if not you'll have to adjust the paths appropreitly to align with your directory structure
    Project
       |___baseline
       |___evaluation
       |___scorer
       |___data
       |    |___subtask-5A-arabic
       |    |           |___lists_metadata
       |    |           |___dev_rumors.json
       |    |           |___train_rumors.json
       |    |           |___relevance_judgments.txt
       |    |___users_metadata
       |___Individual_work
       |         |___Hamza_Gharafi
       |         |        |___helper_functions.py
       |         |        |___ml_algo.py
       |         |___users_json_map.csv
       .
       .
       .
    -------------------------------------------------------------------------------------------------
    Paths
    -----
    In order for the paths generated in helper_functions to work correctly it's best to leave it in it's original location or add it to your individual_work personal directories now to the defiend paths:
    path_variable_name :::::::::: Location/Target
    -------------------::::::::::-----------------
    project_main_path  :::::::::: The path of the project directory that containes 'data' 'baseline' 'Individual_work'.....
    data_path          :::::::::: The path to the data directory inside the main project directory
    users_metadata_path:::::::::: The path to the users_metadata directory in the location said before and shown in the directory structure
    users_metadata_files::::::::: A list containing the path for each json file in the users_metadata directory
    t5_data_path       :::::::::: The path to subtask-5A-arabic directory inside data directory
    lists_metadata_path:::::::::: The path to lists metadata directory
    lists_metadata_files::::::::: A list containing the path for each json file in the lists directory
    dev_rumors_path    :::::::::: The path to the 'dev_rumors.json' file 
    train_rumors_path  :::::::::: The path to the 'train_rumors.json' file
    relevance_judgment_path:::::: The path to the 'relevance_judgment.txt' file
    individual_work_path::::::::: the path to the directory containing our personal work
    -------------------------------------------------------------------------------------------------
    Functions
    ---------
    get_users_metadata ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                        Inputs:
                            user_id            :::: The id of the tweeter user/authority
                            users_json_map     :::: The dataframe containing the user id and its respective json file
                            users_metadata_path:::: The path to users_metadata directory
                            "Note: If you maintain the folder schema shown before the users_json_map and the users_metadata_path will be given by default, but if change the schema you have to provide both the variables"
                        Output:
                            metadata of the user/authority having the user_id given as input
    -------------------------------------------------------------------------------------------------
    DFs
    ----
    users_json_map :::::::::: data frame containing each and every user_id matched with the file_name containing the user metadata
    ''')
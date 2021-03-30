# -*- coding: utf-8 -*-


import argparse
import time
import os
import pandas as pd
import ast
import json
import six
import glob
import numpy as np
from tqdm import tqdm



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', default='train', type=str, choices=['train','valid','test'])
    parser.add_argument('-news_dir', default='', type=str, help='target file to json')
    parser.add_argument('-output', default='', type=str, help='json output directory')
    
#    parser.random_state("-random_state", defalut="", type=int, help="random state")
    
    args = parser.parse_args()
    mode = args.mode
    news_dir = args.news_dir
    output = args.output
    
    # Initialize directory
    if not os.path.exists(output):
        os.makedirs(directory)
        
    if not news_dir.endswith("csv"):
        raise AssertionError("file is not a csv")
    
        ### main process ###
    mydf = pd.read_csv(news_dir)
    
    list_dic = []
    for idx, row in mydf.iterrows():
        raw = row['article_morp']
        target_idx = ast.literal_eval(row['extractive'])
        
        sentences = raw.split(' ./SF ')[:-1]
        src = [i.split(' ') for i in sentences]
        tgt = [a for i,a in enumerate(src) if i in target_idx]
        
        mydict = {}
        mydict['src'] = src
        mydict['tgt'] = tgt
        list_dic.append(mydict)
    
    temp = []
    for i,a in enumerate(tqdm(list_dic)):
        
        if (i+1)%6!=0:
            temp.append(a)
        else:
            filename = 'korean.'+mode+'.'+str(i//6)+'.json'
            with open(output+"/"+filename, "w", encoding='utf8') as json_file:
                json.dump(temp, json_file, ensure_ascii=False)
            temp = []

if __name__ == '__main__':
    main()

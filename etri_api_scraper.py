# -*- coding: utf-8 -*-

import argparse
import json
import os
import time
import urllib3
import jsonlines
from glob import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, default='', help='etri api key')
    parser.add_argument('--directory', type=str, default='output', help='JSON storage directory')
    parser.add_argument('--input', type=str, default='', help='input jsonl file path')
    parser.add_argument('--first_index', type=int, default=0, help='First index of articles')
    parser.add_argument('--last_index', type=int, default=42803, help='Last (latest) index of articles')

    args = parser.parse_args()
    api_key = args.api_key
    directory = args.directory
    input = args.input
    first_index = args.first_index
    last_index = args.last_index

    # Initialize directory
    if not os.path.exists(directory):
        os.makedirs(directory)
        

    ### main process ###
    
    with open(input, 'rb') as reader:
        mylist = list(jsonlines.Reader(reader))
    mylist = mylist[first_index:last_index]
    
    l = len(mylist)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    for idx,items in enumerate(mylist):
        target = ' '.join(items['article_original'])
        processed_text = do_lang(api_key,target)
        if processed_text.startswith('openapi error')==True:
            print('openapi error')
            break
        else:
            save_txt(directory, first_index, idx, processed_text)
        time.sleep(0.01)
        printProgressBar(idx + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        
def do_lang ( openapi_key, text ) :
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    requestJson = { "access_key": openapi_key, "argument": { "text": text, "analysis_code": "morp" } }
    http = urllib3.PoolManager()
    response = http.request( "POST", openApiURL, headers={"Content-Type": "application/json; charset=UTF-8"}, body=json.dumps(requestJson))
    
    json_data = json.loads(response.data.decode('utf-8'))
    json_result = json_data["result"]
    
    if json_result == -1:
        json_reason = json_data["reason"]
        if "Invalid Access Key" in json_reason:
            logger.info(json_reason)
            logger.info("Please check the openapi access key.")
            sys.exit()
        return "openapi error - " + json_reason
    else:
        json_data = json.loads(response.data.decode('utf-8'))
    
        json_return_obj = json_data["return_object"]
        
        return_result = ""
        json_sentence = json_return_obj["sentence"]
        for json_morp in json_sentence:
            for morp in json_morp["morp"]:
                return_result = return_result+str(morp["lemma"])+"/"+str(morp["type"])+" "

        return return_result

def save_txt(directory, first_index, idx, txt):
    with open(directory+str(first_index+idx), 'w', encoding='utf-8') as f:
        f.write(txt)

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
        
if __name__ == '__main__':
    main()

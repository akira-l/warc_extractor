import os, sys
import argparse

import openai
from openai import OpenAI
from http import HTTPStatus
import dashscope

import pdb 

def parse_args():
    parser = argparse.ArgumentParser(description='parameters')
    parser.add_argument('--data_path', dest='data_path',
                        default='', type=str, help='./flatten_data/ACM_part/2020-05_ACM_0001.warc.gz/1007996.txt')
    parser.add_argument('--output_path', dest='output_path',
                        default='', type=str, help='./flatten_data/ACM_part/2020-05_ACM_0001.warc.gz')
    parser.add_argument('--openai_key', dest='openai_key',
                        default='', type=str,) 
    args = parser.parse_args()
    return args


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_useful_information(text, api_key):
    text_len = len(text) 
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", 
    )
    gather = []
    for idx in range(text_len // 1000): 
        input_text = text[idx * 1000 : (idx + 1) *1000]
        completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f"Extract all meaningful and long context from the following text, ensuring the output only contains words from the given text and excludes any meaningless content:\n\n{input_text}"}],
        temperature=0.8,
        top_p=0.8
        )
        response = completion.model_dump_json()
        res = completion.to_dict() 
        output_text = res['choices'][0]['message']['content']
        gather.append(output_text) 

    return '\n'.join(gather)  


## Extract useful information using GPT-4
#def extract_useful_information(text, api_key):
#    response = openai.ChatCompletion.create(
#        model="gpt-4",
#        messages=[
#            {"role": "system", "content": "You are a helpful assistant."},
#            {"role": "user", "content": f"Extract all useful and long context from the following text:\n\n{text}"}
#        ],
#        max_tokens=1500,  # You can adjust the number of tokens as needed
#        n=1,
#        stop=None,
#        temperature=0.5
#    )
#    
#    return response.choices[0].message['content'].strip()

   
def main():
    args = parse_args()
    text = read_text_file(args.data_path)
    useful_information = extract_useful_information(text, args.openai_key)
    
    print("Extracted Information:")
    print(useful_information)

    target_name = args.data_path.split('/')[-1][:-4]
    write_file_name = os.path.join(args.output_path, target_name + 'useful.txt')  
    write_handle = open(write_file_name, 'a') 
    write_handle.write(useful_information) 
    write_handle.close() 

if __name__ == "__main__":
    main()


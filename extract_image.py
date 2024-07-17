import os
import argparse

from bs4 import BeautifulSoup
import requests

import pdb 

def parse_args():
    parser = argparse.ArgumentParser(description='parameters')
    parser.add_argument('--data_path', dest='data_path',
                        default='', type=str, help='./flatten_data/ACM_part/2020-05_ACM_0001.warc.gz/1007996.html')
    parser.add_argument('--output_path', dest='output_path',
                        default='', type=str, help='./flatten_data/ACM_part/2020-05_ACM_0001.warc.gz')
    args = parser.parse_args()
    return args


def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url}")
    else:
        print(f"Failed to download {url}")

def extract_images(html_file, output_folder):
    if output_folder == '': 
        output_root_list = html_file.split('/')[:-1] 
        output_root = '/'.join(output_root_list) 
        output_name = html_file.split('/')[-1].split('.')[0] + '_image'
        output_path = os.path.join(output_root, output_name) 
        if not os.path.exists(output_path): 
            os.makedirs(output_path) 
        output_folder = output_path 
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url:
                if img_url.startswith('http'):
                    download_image(img_url, output_folder)
                else:
                    print(f"Skipping non-http image: {img_url}")


if __name__ == '__main__': 
    args = parse_args()
    extract_images(args.data_path, args.output_path) 
    #html_file = './flatten_data/ACM_part/2020-05_ACM_0001.warc.gz/1007996.html'
    #output_folder = 'images'
    #extract_images(html_file, output_folder)


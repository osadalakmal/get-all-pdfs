#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import os
import requests
from tqdm import tqdm
import math
from urllib.parse import urlparse

soup = BeautifulSoup(requests.get(sys.argv[1]).content, 'html.parser')
papers = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and '.pdf' in href:
        if href[0] == '/':
            host = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(sys.argv[1]))
            papers.append(host + href)
        else:
            papers.append(href)
try:
    os.mkdir('pdfs')
except:
    pass
os.chdir('pdfs')
for paper in papers:
    print("Getting {}:\n".format(paper))
    r = requests.get(paper, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(os.path.basename(paper), 'wb') as f:
        total = math.ceil(total_size // block_size)
        for data in tqdm(r.iter_content(block_size), total=total,
                         unit='KB', unit_scale=True):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")
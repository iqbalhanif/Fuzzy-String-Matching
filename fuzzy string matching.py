
# Import Module
import requests
import bs4
import multiprocessing as mp
import numpy as np
import time
from difflib import SequenceMatcher


# Get Sample Data
sec_list_html = requests.get('https://www.sec.gov/rules/other/4-460list.htm').content
sec_list_soup = bs4.BeautifulSoup(sec_list_html, 'lxml')
companies_list = sec_list_soup.find_all('tr')[1:-1]
companies_list_clean = [str(x.text.strip()).lower() for x in companies_list]

companies_list_clean[:5]


# Acak beberapa huruf untuk uji coba fuzzy string matching
def switch_3_characters_randomly(name, seed = None):
    if seed:
        np.random.seed(seed)
    name_split = list(name)
    flip_indices = np.random.choice(len(name), 3, replace = False)
    a, b, c = flip_indices[0], flip_indices[1], flip_indices[2]
    name_split[a], name_split[b], name_split[c] = name_split[c], name_split[b], name_split[a]
    return ''.join(name_split)

synthetic_companies_list = list(map(switch_3_characters_randomly, companies_list_clean))
synthetic_companies_list[:5]


# Fungsi Fuzzy String Matching
def match_ratio(name1, name2):
    s = SequenceMatcher(None, name1, name2)
    return s.ratio()

def get_basic_fuzzy_matches(synthetic_name, threshold = 0.75):
    match_list = []
    flag = None
    for name1 in companies_list_clean:
        ratio = match_ratio(name1, synthetic_name)
        if ratio > threshold:
            if not flag:
                flag = 1
            match_list.append((synthetic_name, name1, ratio))
            
    if not flag:
        match_list.append((synthetic_name, None, 0))
            
    return match_list

matches = list(map(get_basic_fuzzy_matches, synthetic_companies_list[:50]))
matches[:5]


# Membuat pooled matches (mencocokkan satu string dengan beberapa string yang mirip)
pool = mp.Pool()
pooled_matches = list(pool.map(get_basic_fuzzy_matches, synthetic_companies_list[:50]))
pool.close()
pool.join()

pooled_matches[:20]
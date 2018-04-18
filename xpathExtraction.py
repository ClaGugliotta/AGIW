from lxml import etree
from matching import Matching
import json
import os
import comparator
import re
from jsonEncoder import MyEncoder
webpages_path = '/home/lollouno/Documenti/UNIVERSITA/AGIW/extractor/notebook/'
extract_path = '/home/lollouno/Documenti/UNIVERSITA/AGIW/extractor/notebookOurJson/'
keywords_file_name = "/home/lollouno/Documenti/UNIVERSITA/AGIW/xpathextractor/specification.json"
new_keyword_file_name = "/home/lollouno/Documenti/UNIVERSITA/AGIW/xpathextractor/specification1.json"

keyword_json = json.load(open(keywords_file_name))


def get_xpaths(htmlFile):
    """ Create a json file with all the xpaths found on a html file """
    file = open(htmlFile, 'r')
    content = file.read()
    file.close()
    xpaths = {}

    try:
        tree = etree.HTML(content)
        root = tree.getroottree()
        for e in tree.iter():
            matches = comparator.check_element_match_any_keyword(e, root)
            if matches:
                for matching in matches:
                    matching.page = htmlFile
                    if matching.attribute not in xpaths.keys():
                        xpaths[matching.attribute] = []#[{"path": matching.path, "file": matching.page, "match": matching.match}]
                    xpaths[matching.attribute].append(matching)#{"path": matching.path, "file": matching.page, "match": matching.match})
    except Exception:
        pass
    return xpaths


def merge_dicts(dict1, dict2):
    """ If the dicts have common keys, add the dict2's values to dict1's and return it """
    if not bool(dict2):
        return dict1
    elif not bool(dict1):
        return dict2
    for key1 in dict1.keys():
        for key2 in dict2.keys():
            if key2 == key1 and dict2.get(key2) not in dict1.get(key1):
                dict1.get(key1).extend(dict2[key2])
    return dict1


def save_extracted_info(xpaths,json_name):
    json_obj = {}
    for attribute in xpaths.keys():
        for match in xpaths[attribute]:
            # qui deve avvenire il processo di selezione
            json_obj[attribute] = match.match
    with open(json_name, 'w') as outfile:
        json.dump(json_obj, outfile)


def extract_full_keywords_from_structured_data(xpaths):
    new_keyword_json = keyword_json
    for attribute in xpaths.keys():
        for match in xpaths[attribute]:
            if re.compile(".*/(tr|li).*").match(str(match)) and len(match.text) < 30 and not match.is_shared and not comparator.match_all(match.keyword,match.text):
                new_keyword_json[attribute].append(match.text.strip().replace("\u00a0", ""))
    with open(new_keyword_file_name, 'w') as outfile:
        json.dump(new_keyword_json, outfile)

def print_xpaths(xpaths):
    for attribute in xpaths.keys():
        print("\tAttribute: " + attribute)
        for match in xpaths[attribute]:
            if  re.compile(".*/(tr|li).*").match(str(match)) and len(match.text) < 30:
                print("\t\t" + str(match))


def xpaths_extraction():
    if not os.path.isdir(extract_path):
        os.mkdir(extract_path)
    xpath_for_websites = {}
    current_folder_processing = ""
    for (path, domains, websites) in os.walk(webpages_path):
        for website in websites:
            if str(website).endswith("html"):
                domain = os.path.basename(path)
                print("Currently processing website: " + website + "\t of domain: " + domain)
                domain_path_name = extract_path  + domain
                if not os.path.isdir(domain_path_name):
                    os.mkdir(domain_path_name)
                if current_folder_processing != "" and current_folder_processing != domain_path_name:
                    print_xpaths(xpath_for_websites)
                    extract_full_keywords_from_structured_data(xpath_for_websites)
                    print("Processing...")
                    comparator.find_common_denominators(xpath_for_websites)
                    print("folder: " + current_folder_processing + '/xpaths.json')
                    with open(current_folder_processing + '/xpaths.json', 'w') as outfile:
                        json.dump(xpath_for_websites, outfile, cls=MyEncoder)
                    xpath_for_websites = {}
                current_folder_processing = domain_path_name

                html_file = path + '/' + website
                xpaths = get_xpaths(html_file)
                save_extracted_info(xpaths,current_folder_processing + "/" + str(website).replace(".html", ".json"))
                xpath_for_websites = merge_dicts(xpaths,xpath_for_websites)

xpaths_extraction()


def get_specs():
    specsFile = json.load(open('specification.json'))
    specs = {}
    for key in specsFile.keys():
        specs[key] = specsFile.get(key)
    return specs




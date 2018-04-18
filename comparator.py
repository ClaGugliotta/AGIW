import json
import re
from re import match
import tqdm
from matching import Matching

keyword_file = "/home/lollouno/Documenti/UNIVERSITA/AGIW/xpathextractor/specification.json"
data = json.load(open(keyword_file))


# Questa funzione restituisce una lista di "match" a partire da un elemento HTML da sottoporre a confronto con l'insieme
# di keyword del file keyword_file. Inoltre tra i parametri e' richiesta la radice dell'HTML (per trovare l'xpath).
# Un match e' rappresentato dai seguenti campi:

# Text: il testo all'interno dell'elemento HTML sottoposto al confronto
# Match: la porzione del testo (text) che effettivamente combacia con l'keyword
# Atribute: l'attributo da cui e' stata presa l'keyword (cpu/ram/trademark...)
# Path: l'xpath dell'elemento HTML sottoposto al confronto
# Start: l'indice del carattere del testo (text) a cui inizia il matching
# Stop: l'indice del carattere del testo (text) in cui finisce il matching
# Is_shared: un valore booleano che indica se l'elemento HTML contiene keywords relative a diversi attributi
def check_element_match_any_keyword(element, root):
    matched = []
    for attribute in data.keys():
        for keyword in list(data[attribute]):
            start, stop = check_element_match_given_keyword(element, keyword)
            if start != -1:
                match = keyword
                if match.startswith("/"):
                    match = str(element.text)[start:stop].replace(" ", "")
                matched.append(Matching(element.text, match, keyword, attribute, root.getpath(element), start, stop, False))
    return check_attribute_redundancy(matched)


def check_attribute_redundancy(matched):
    for l, matchingl in enumerate(matched):
        list_of_common_attributes = [matchingl.start, matchingl.stop]
        for i, matchingi in enumerate(matched):
            if i != l and matchingi.path == matchingl.path and matchingi.attribute != matchingl.attribute:
                # this element has many attributes
                matchingi.is_shared = True
                matchingl.is_shared = True
                matched[i] = matchingi
                matched[l] = matchingl
            if i != l and matchingi.path == matchingl.path and matchingi.attribute == matchingl.attribute:
                # the attribute is a composition of previous attributes
                list_of_common_attributes = [min(list_of_common_attributes[0], matchingi.start), max(list_of_common_attributes[1], matchingi.stop)]
                matchingl.match = matchingl.text[list_of_common_attributes[0]:list_of_common_attributes[1]]
                matched[l] = matchingl
                matched.pop(i)
    return matched


def check_element_match_given_keyword(element,keyword):
    text_to_check = depunctuate_text(element.text)
    if keyword.startswith("/"):
        regex = str(keyword[1:])
        # il flag I indica che non si deve considerare maiuscolo e minuscolo diversamente
        pattern = re.compile(regex, re.I)
        # per le regex non viene effettuata la de-punteggiatura (principalmente per evitare problemi con i numeri)
        match = pattern.search(text_to_check)#str(element.text))
        if match:
            return match.start(match.pos), match.end(match.pos)
        else:
            return -1,-1
    elif keyword.lower() in text_to_check.lower():
        start = text_to_check.lower().find(keyword.lower())
        return start, start+len(keyword)
    else:
        return -1, -1


def match_all(text,keyword):
    text_to_check = depunctuate_text(text)
    if keyword.startswith("/"):
        regex = str(keyword[1:])
        # il flag I indica che non si deve considerare maiuscolo e minuscolo diversamente
        pattern = re.compile(regex, re.I)
        # per le regex non viene effettuata la de-punteggiatura (principalmente per evitare problemi con i numeri)
        match = pattern.search(text_to_check)  # str(element.text))
        if match and  match.start(match.pos) == 0 and match.end(match.pos) == len(text):
            return True
        else:
            return False
    elif keyword.lower() == text_to_check.lower():
        return True
    else:
        return False


def find_common_denominators(matches):
    groups = []
    for attribute1 in tqdm.tqdm(matches):
        for matchingi in tqdm.tqdm(matches[attribute1]):
            if not matchingi.is_shared:
                for attribute2 in matches:
                    for matchingl in matches[attribute2]:
                        if matchingl.page != matchingi.page and matchingi.attribute != matchingl.attribute:
                            lmc_path = longest_common_start(matchingi.path,  matchingl.path)
                            if not matchingi.lmc_match or len(lmc_path) > len(matchingi.lmc_path):
                                matchingi.lmc_match = matchingl
                                matchingi.lmc_path = lmc_path

                #print("Path: " + matchingi.path + "\tLMC Path:" + matchingi.lmc_path + "\t(attributes:" + matchingi.attribute + "," + matchingi.lmc_match.attribute + ")")

def longest_common_start(str1, str2):
    strf = str1
    while str1 != str2:
        str1 = str1[:str(str1).rfind("/")]
        str2 = str2[:str(str2).rfind("/")]
    return strf


def depunctuate_text(text):
    return str(text)\
        .replace(". ", "  ")\
        .replace(", ", "  ")\
        .replace("; ", "  ")\
        .replace(": ", "  ")\
        .replace(" .", "  ")\
        .replace(" ,", "  ")\
        .replace(" ;", "  ")\
        .replace(" :", "  ")\
        .replace(")", " ")\
        .replace("]", " ")\
        .replace("}", " ")\
        .replace("(", " ")\
        .replace("[", " ")\
        .replace("{", " ")\
        .replace("\\", " ")\
        .replace("/", " ")\
        .replace("!", " ")\
        .replace("?", " ")\
        .replace("=", " ")\
        .replace("&", " ")
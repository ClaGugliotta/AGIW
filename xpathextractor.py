import requests
from lxml import html
import comparator


pageContent=requests.get('http://thiscov.com/product/198187')


tree = html.fromstring(pageContent.content)
root = tree.getroottree()
tot = 0
for e in tree.iter():
    matched = comparator.check_element_match_any_anchor(e, root)

    for matching in matched:
        #
        print(matching.text + '\t(shared:' + str(matching.is_shared) + ')\n\t' + matching.match + " (" + str(matching.start) + "," + str(matching.stop) + ")" + '\t('
              + matching.attribute + ')\n\t\t' + matching.path)
        tot += len(matched)

print("total matches: " + str(tot))
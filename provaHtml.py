import lxml
from lxml.html.clean import Cleaner

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter
cleaner.kill_tags = ['head', 'script', 'header', 'href', 'footer']

print (lxml.html.tostring(cleaner.clean_html(lxml.html.parse('/home/caiocesare/PycharmProjects/script/1.html'))))


class Matching:
    # Text: il testo all'interno dell'elemento HTML sottoposto al confronto
    text = ""
    # Match: la porzione del testo (text) che effettivamente combacia con l'keyword
    match = ""
    # keyword: la keyword che ha matchato il testo (text)
    keyword = ""
    # Atribute: l'attributo da cui e' stata presa l'keyword (cpu/ram/trademark...)
    attribute = ""
    # Path: l'xpath dell'elemento HTML sottoposto al confronto
    path = ""
    # Start: l'indice del carattere del testo (text) a cui inizia il matching
    start = -1
    # Stop: l'indice del carattere del testo (text) in cui finisce il matching
    stop = 1
    # Is_shared: un valore booleano che indica se l'elemento HTML contiene keywords relative a diversi attributi
    is_shared = ""
    # page: un identificativo della pagina web da cui il match e' stato estratto (un link o il nome del file html)
    page = ""
    # longest match common path: all'interno dello stesso dominio, questo e' l'xpath piu' lungo comune a due match con
    # dirverso attributo
    lmc_path = ""
    # longest match common path match: all'interno dello stesso dominio, questo e' il match relativo al precedente campo
    lmc_match = None

    def __init__(self, text, match, keyword, attribute, path, start, stop, is_shared):
        self.text = text
        self.match = match
        self.keyword = keyword
        self.attribute = attribute
        self.path = path
        self.start = start
        self.stop = stop
        self.is_shared = is_shared

    def __str__(self):
        return "text:" + self.text + " match: " + self.match + " attribute: " + self.attribute + " path: " + self.path + " start: " + str(self.start) + " stop: " + str(self.stop) + " is_shared: " + str(self.is_shared) + " page: " + str(self.page)

   # def __dict__(self):
    #    return {"text": self.text, "match": self.match, "attribute:": self.attribute, "path": self.path,
    #            "start": self.start, "stop": self.stop, "is_shared": self.is_shared, "page": self.page, "lmc_path": self.lmc_path}
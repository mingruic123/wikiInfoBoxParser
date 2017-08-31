from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys

def main():
    for url in sys.argv[1:]:
        print(url)
        page = urlopen(url)
        soup = BeautifulSoup(page)

        infobox = soup.find('table', class_ = 'infobox vcard')
        tr = infobox.find_all("tr")
        mapWithLink = {}
        mapWithoutLink = {}
        for t in tr:
            #find relation
            rel = ""
            th = t.find("th")
            if(th is not None):
               rel = th.getText()

            #find attributes
            td = t.find("td")
            if (td is not None):
                links = td.find_all('a')
                for l in links:
                    attr2 = ""
                    link = ""
                    if (l is not None):
                        link = l.get('href')
                    attr2 = l.getText().strip()
                    print(rel + " -> " + attr2 + " -> " + link)
                    mapWithLink[(rel, attr2)] =  link

                attr1 = td.getText().strip()
                split = attr1.splitlines()
                for s in split:
                    s = re.sub("\(.*?\)", "", s).strip() # remove noise in "()"
                    if((rel, s) not in mapWithLink):
                        mapWithoutLink[(rel, s)] = None
                        try:
                            print(rel + " -> " + s)
                        except:
                            print("Decoding error")

if __name__ == "__main__":
    main()


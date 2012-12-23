import urllib
import webbrowser

DO_BROWSER=True

good_names_f = open('out.txt')
good_names = [x.strip() for x in good_names_f.read().split('\n')]
good_names = [x for x in good_names if x]

for i in range(len(good_names)):
    name = good_names[i]
    url = 'http://www.linkedin.com/search?search=+&reset=+&keywords=' + urllib.quote_plus(name)
    if DO_BROWSER:
        webbrowser.open(url, new=2) # 2 == tab
    else:
        print url

    if ((i % 10) == 9):
        pause = raw_input("Keep going? Press enter for yes, Ctrl-C for no.")

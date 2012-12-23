#!usr/bin/python

import lxml.html

s = open('GPO-PLUMBOOK-2012.htm').read()
h = lxml.html.fromstring(s)
text = h.cssselect('pre')[0].text_content()
lines = text.split('\n')

sections = []

for i in range(len(lines)):
    this_line = lines[i]
    if ((this_line == '--------------------------------------------------------------------------------------------------------------------------------------------------------') and
        ('Level' in lines[i+1]) and
        ('Name of Incumbent' in lines[i+2])):
        this_section_start = (i-1)
        # find the end...
        end_marker = ['--------------------------------------------------------------------------------------------------------------------------------------------------------', '', '']
        possible_end_pos = i+3
        while True:
            possible_end_lines = [x.strip()
                                  for x in
                                  lines[possible_end_pos:possible_end_pos+3]]
            assert (len(possible_end_lines) == len(end_marker))
            if possible_end_lines == end_marker:
                break
            possible_end_pos += 1

        if 'UNITED STATES AGENCY FOR INTERNATIONAL DEVELOPMENT' == lines[i-1].strip():
            assert ( (possible_end_pos-i) > 10) # reasonably long

        sections.append(lines[this_section_start:possible_end_pos])

care_about_sections = ['UNITED STATES AGENCY FOR INTERNATIONAL DEVELOPMENT', 'DEPARTMENT OF STATE', 'Office of the Secretary of Defense']

def get_names(l):
    for line in l:
        if not line.strip():
            continue
        if len(line) > 91:
            name = line[54:91]
            yield name

good_names = []

for k in care_about_sections:
    found = False
    for as_l in sections:
        if as_l[0].strip() == k:
            found = as_l
    assert found

    good_names.extend(get_names(found))

good_names = [x.replace(".", " ").strip()
              for x in good_names]

blacklist = set(['Vacant', 'do', 'Career Incumbent',
                 '-------------------------------------',
                 'Name of Incumbent'])

good_names = [x for x in good_names
              if x not in blacklist]


import webbrowser
import urllib

DO_BROWSER = False

for i in range(len(good_names)):
    name = good_names[i]
    url = 'http://www.linkedin.com/search?search=+&reset=+&keywords=' + urllib.quote_plus(name)
    if DO_BROWSER:
        webbrowser.open(url, new=2) # 2 == tab
    else:
        print url

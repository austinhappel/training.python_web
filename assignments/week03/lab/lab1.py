from bs4 import BeautifulSoup

fh = open('class.html', 'r')
parsed = BeautifulSoup(fh)


def makehtml(mylist):
    ret = '<ul>'
    for val in mylist:
        ret += '<li><a href="' + val['url'] + '">' + val['title'] + '</a></li>'

    ret += '</ul>'
    return ret


def sort_entries(parsed_page):

    entries = parsed_page.find_all('div', class_='feedEntry')
    dj_entries = []
    pgsql_entries = []
    other_entries = []

    for e in entries:
        anchor = e.find('a')
        paragraph = e.find('p', 'discreet')
        title = anchor.text.strip()
        url = anchor.attrs['href']

        try:
            p = paragraph.text.strip()

            if (p.lower().find('django') > -1):
                dj_entries.append({'title': title, 'url': url})
            elif (p.lower().find('postgres') > -1):
                pgsql_entries.append({'title': title, 'url': url})
            else:
                other_entries.append({'title': title, 'url': url})
        except AttributeError:
            other_entries.append({'title': title, 'url': url})

    return (pgsql_entries, dj_entries, other_entries)

pgsql, django, other = sort_entries(parsed)

html = '<!doctype html>\n<html>'
html += '<h1>pgsql ( ' + str(len(pgsql)) + ')</h1>'
html += str(makehtml(pgsql).encode('unicode-escape'))
html += '<h1>django ( ' + str(len(django)) + ')</h1>'
html += str(makehtml(django).encode('unicode-escape'))
html += '<h1>other ( ' + str(len(other)) + ')</h1>'
html += str(makehtml(other).encode('unicode-escape'))
html += '</html>'

f = open('result.html', 'w')
f.write(html)
f.close()

print 'done. open result.html.'

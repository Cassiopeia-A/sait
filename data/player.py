from data.parser import search
from bs4 import BeautifulSoup
import codecs


def play(data, title):
    f = codecs.open("templates/player.html", 'r', 'utf8')
    html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    soup.h1.string = title
    soup.h2.string = 'Часть 1'
    soup.audio['src'] = data[0]["url"]
    soup.find('div', id='playlist').clear()

    for i, part in enumerate(data):
        url = part["url"]

        btn = soup.new_tag('button')
        btn['class'] = "track"
        btn['name'] = url
        btn['onclick'] = f"changeTrack('{url}', 'Часть {i + 1}', {i})"
        btn.string = f'Часть {i + 1}'

        soup.find('div', id='playlist').append(btn)

    file2 = open(f'templates/{title}.html', "w+", encoding='utf-8')
    file2.write(soup.prettify())


if __name__ == '__main__':
    play(search('Мертвые души'), 'Мертвые души')

from requests import get
from bs4 import BeautifulSoup as bs


def search(search_message):
    url = f'https://m.knigavuhe.org/search/?q={"+".join(search_message.split(" "))}'

    soup = bs(get(url).text, "lxml")

    book_list = soup.find_all('span', class_='bookkitemm')

    new_url = ''
    for book in book_list:
        res = book.find('a', class_='bookkitem_cover')['href']
        if not book.find('span', class_='bookkitem_litres_icon'):
            new_url = f'https://m.knigavuhe.org{res}'
            break

    page = bs(get(new_url).text, "lxml")
    files_parser = page.find_all('script')[-3].text.split('var player ='
                                                   ' new BookPlayer'
                                                          '')[1].split('cur.'
                                                                       'bookPlayer'
                                                                               ' = player'
                                                                               '')[0].split(', ')[1][1:-1].split('}')
    files = []
    for file in files_parser:
        if file:
            res = {}
            str_data = file.split('{')[1]
            for s in str_data.split(','):
                for_dict = s.split(':')
                key = for_dict[0][1:-1]
                if len(for_dict) == 2:
                    value = for_dict[1]
                    if value.startswith('"'):
                        value = value[1:-1]
                    else:
                        value = float(value)
                else:
                    value = f'{for_dict[1]}:{for_dict[2]}'[1:-1]

                res[key] = value
            files.append(res)
    return files


if __name__ == '__main__':
    search('Двадцать тысяч лье под водой')

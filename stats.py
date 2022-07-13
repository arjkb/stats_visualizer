from bs4 import BeautifulSoup

def extract_date_posts():
    file_contents = None
    with open('inp.html', 'r') as f:
        file_contents = f.read()
    # print(file_contents)

    posts = {}
    soup = BeautifulSoup(file_contents, 'html.parser')
    # print(soup.prettify())
    divs = soup.find_all('div')
    date_in_consideration = None
    for div in divs:
        cls = div['class'][0]
        if cls == 'date':
            date_in_consideration = div.get_text().strip()
            if date_in_consideration not in posts:
                posts[date_in_consideration] = []
        elif cls == 'post':
            posts[date_in_consideration]  = list(map(lambda link: link.get_text().strip(), div.find_all('a')))
    return posts

def main():
    posts_by_date = extract_date_posts()
    print(posts_by_date)
    

if __name__ == '__main__':
    main()
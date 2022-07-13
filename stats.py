import datetime
from bs4 import BeautifulSoup

month_lengths = {
    1: 31, 2: 28, 3:31, 4: 30, 5: 31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31
}

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

def next_day():
    start_date = datetime.date(2021, 1, 1)
    days = 0
    yield start_date + datetime.timedelta(days=days)
    days += 1

def main():
    posts_by_day = extract_date_posts()
    print(posts_by_day)

    # start date seems to be May 2011, so let's start from 2011
    letter = ''
    for year in range(2011, datetime.date.today().year + 1):
        is_leap = (year % 4) == 0
        for month in range(1, 12+1):
            month_length = 29 if month == 2 and is_leap else month_lengths[month]
            print(f"\n {year} {month:2}: ", end="")
            for day in range(1, month_length + 1):
                date = (datetime.datetime(year, month, day)).strftime("%A, %B %-d, %Y")
                # print(date)
                letter = ' '
                if date in posts_by_day:
                    count = len(posts_by_day[date])
                    if count > 1:
                        letter = 'X'
                    elif count == 1:
                        letter = '+'
                    else:
                        letter = '-'
                print(letter, end='')
    print("\n")

if __name__ == '__main__':
    main()
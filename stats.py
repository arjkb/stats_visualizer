# Arjun Krishna Babu
# 13 July 2022

import datetime
from bs4 import BeautifulSoup

# there's a library to figure this out,
# but I want to minimize dependencies
month_lengths = {
    1: 31, 2: 28, 3:31, 4: 30, 5: 31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31
}

def extract_date_posts(filename):
    file_contents = None
    with open(filename, 'r') as f:
        file_contents = f.read()

    posts = {}
    divs = BeautifulSoup(file_contents, 'html.parser').find_all('div')
    date_in_consideration = None
    for div in divs:
        cls = div['class'][0]
        # it's a date in a <div>, with the posts of that date in
        # an adjacent (NOT child) <div>
        #
        # 1. Grab the date
        # 2. Grab the posts on that date
        if cls == 'date':
            date_in_consideration = div.get_text().strip()
            if date_in_consideration not in posts:
                posts[date_in_consideration] = []
        elif cls == 'post':
            # store all post titles from that date
            posts[date_in_consideration]  = list(map(lambda link: link.get_text().strip(), div.find_all('a')))
    return posts

def main():
    posts_by_day = extract_date_posts('inp.html')
    print(posts_by_day)

    # start date seems to be May 2011, so let's start from 2011
    today = datetime.date.today()
    letter = ''
    for year in range(2011, today.year + 1):
        for month in range(1, 12 + 1):
            month_length = 29 if month == 2 and ((year % 4) == 0) else month_lengths[month] # handle leap year February
            print(f"\n {year} {month:2}: ", end="")
            for day in range(1, month_length + 1):
                date = (datetime.datetime(year, month, day)).strftime("%A, %B %-d, %Y")
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

            if year == today.year and month == (today.month):
                # avoid unnecessarily looking into the future
                break

    print("\n")

if __name__ == '__main__':
    main()
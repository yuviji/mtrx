from bs4 import BeautifulSoup
import requests
import string
import json

cleaned_string = lambda s: ''.join(filter(lambda x: x in set(string.printable), s))

def async_scrape(url: string) -> dict:
    # url should be like "https://www.yelp.com/biz/reading-terminal-market-philadelphia"
    html_content = requests.get(url.split('?')[0] + '?sort_by=date_desc').content
    soup = BeautifulSoup(html_content, "html.parser")

    business_info = {}

    header = soup.select_one('h1').find_parent('div').find_parent('div')
    business_info['business_name'] = cleaned_string(header.find('h1').text)
    business_info['business_cost'] = '$' * header.text.count('$')
    business_info['business_rating'] = float(cleaned_string(header.find('div').next_sibling.find('div').next_sibling.find('span').text))
    business_info['business_tags'] = cleaned_string(header.find('div').find_next_siblings('span')[2].text).split(', ')
    business_info['business_description'] = cleaned_string(soup.find('section', {'aria-label': 'About the Business'}).find_all('p')[-1].text)
    business_info['business_address'] = cleaned_string(soup.select_one('a:-soup-contains("Get Directions")').find_parent('p').find_next_sibling('p').text)
    business_info['business_reviews'] = []

    num_pages = tuple(map(int, cleaned_string(soup.find('div', {'aria-label': 'Pagination navigation'}).find('div').next_sibling.text).split(' of ')))
    num_pages = (num_pages[0], min(10, num_pages[1]))
    print(num_pages)

    for i in range(num_pages[1]):
        html_content = requests.get(url + f'?start={i * 10}&sort_by=date_desc').content
        soup = BeautifulSoup(html_content, "html.parser")
        
        navbar = soup.find('div', {'aria-label': 'Pagination navigation'})
        print(tuple(map(int, cleaned_string(navbar.find('div').next_sibling.text).split(' of '))))

        reviews = [i.find('div') for i in navbar.previous_sibling.find_all('li')[:-1]]
        for review in reviews:
            review_data = {}
            review_data['reviewer_id'] = cleaned_string(review.find('a')['href'].split('=')[-1])
            rating_element = review.find('div').next_sibling.find('div').find('div')
            review_data['review_rating'] = float(cleaned_string(rating_element.find('span').find('div')['aria-label']).split(' ')[0])
            review_data['review_date'] = cleaned_string(rating_element.next_sibling.find('span').text)
            review_data['review_content'] = cleaned_string(review.find('p').text)
            try:
                review_data['elite'] = (len(review.find_all('a', {'href': '/elite'})) > 0)
            except:
                review_data['elite'] = False
            business_info['business_reviews'].append(review_data)
        
    with open('async_business.json', 'w') as json_file:
        json.dump(business_info, json_file, indent=4)
    return business_info
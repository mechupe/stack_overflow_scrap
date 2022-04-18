import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.1.686 Yowser/2.5 Safari/537.36'}


def parse_tags_page(page_number):
    """
    Parses page with tags, e.g. https://stackoverflow.com/tags?page=2&tab=popular

    :param page_number: number of page which shall be parsed
    :return: tags in from of dictionary
    """
    url = f'https://stackoverflow.com/tags?page={page_number}&tab=popular'
    response = requests.get(url, headers=HEADERS)
    soap = bs(response.content, 'html.parser')
    items = soap.find_all('div', class_='s-card')

    tags = dict()
    for item in items:
        try:
            value = \
                item.find('div', class_="mt-auto d-flex jc-space-between fs-caption fc-black-400").get_text().split()[0]
            tags[item.find('a', class_="post-tag").get_text(strip=True)] = value
        except AttributeError:
            continue

    return tags


def parse_tags(page_number):
    """
    Calls function @ref parse_tags_page and convert its output to dataframe

    :param page_number: number of page which shall be parsed
    :return: data frame of tags
    """
    tags = parse_tags_page(page_number)
    df_tags = pd.DataFrame(tags.values(), index=tags.keys(), columns=['amount_of_questions'])
    df_tags.reset_index(inplace=True)
    df_tags.rename(columns={'index': 'tags'}, inplace=True)
    return df_tags


def parse_questions_page(link):
    """
    Parse page of questions

    :param link: link to questions page, which shall be parsed
    :return: list of parsed questions
    """
    try:
        response = requests.get(link, headers=HEADERS, timeout=60)
    except requests.exceptions.Timeout:
        return

    soap = bs(response.content, 'html.parser')
    items = soap.find_all('div', class_='question-summary')

    def thousand(x):
        return int(x[:x.index('k')]) * 1000 if 'k' in x else (int(x) if x != '' else 0)

    pattern_id = re.compile('question-summary-(\d*)')
    pattern_views = re.compile('(\d*k*) views')
    pattern_answer = re.compile('(\d*)answer')

    questions = list()
    for item in items:
        try:
            answers_accepted = False
            answers = 0
            try:
                answers = int(pattern_answer.search(item.find('div', class_='answered').get_text())[1])
            except AttributeError:
                pass
            try:
                answers = int(pattern_answer.search(item.find('div', class_='answered-accepted').get_text())[1])
                answers_accepted = True
            except AttributeError:
                pass
            date = item.find('span',class_ = 'relativetime')
            vote = item.find('span', class_='vote-count-post')
            views = item.find('div', class_='views')
            questions.append({'id': pattern_id.search(item['id'])[1],
                              'vote': int(vote.get_text()), 'answer': answers,
                              'views': thousand(
                                  pattern_views.search(views.get_text())[1]),
                              'accepted': answers_accepted,
                              'date': date['title'][:10]})
        except AttributeError:
            continue

    return questions


def parse_questions(page_number, current_tag):
    """
    Parse page of questions

    :param page_number: page number which shall be parsed
    :param current_tag: name of tag
    :return: data frame questions and related statistic
    """
    link = f'https://stackoverflow.com/questions/tagged/{current_tag}?tab=newest&page={page_number}&pagesize=50'
    df = pd.DataFrame(parse_questions_page(link))
    if not df.empty:
        df.insert(0, 'tag', current_tag)
    return df

__author__ = 'Tohei'


import string


def movie_link_generator():
    """ generate list of links cover all movie in boxofficemojo.com  """
    urls=[]
    abc_movie_links=[]
    for i in string.ascii_uppercase:
        url = 'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' + str(i) + '&p=.htm'
        urls.append(url)
        for n in range(2,11):
            url2 = 'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' + str(i) + '&page=' + str(n) + '&p=.htm'
            urls.append(url2)

    for url in urls:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        try :
            link_data = ["http://www.boxofficemojo.com" + str(link.get('href')) for link in soup.find_all('a')]
            abc_movie_link_data = filter(lambda x:'movies/?id' in x, link_data)
            abc_movie_links.extend(abc_movie_link_data)
        except :
            pass

    return abc_movie_links





#######################################################################################

import time
import urllib2
import re
import pandas
from random import randint
from bs4 import BeautifulSoup

soups = []
all_movie_data = []
all_df = pandas.DataFrame()
all_movie_df = pandas.DataFrame()
concatenated = pandas.DataFrame()
headers = ["rating", "domestic_total_gross", "widest_release", "genre", "movie_title", "distributor", "runtime", "release_date"]


def movie_link2soups(links):
    """ movie links to soups to dataframe """
    almovie_df = pandas.DataFrame()
    for link in links:
        url = link
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            movie_dictionary = get_all_data(soup)
            movie_df = pandas.DataFrame(movie_dictionary.items())
            movie_dt = movie_df.T
            movie_dt.columns = headers
            data = movie_dt[1:]
            almovie_df = almovie_df.append(data)

        except:
            pass
            time.sleep(randint(2,9)/5.5)

    return almovie_df


def get_movie_title(soup):
    """ get movie title from soup """
    title_string = soup.find("title").text
    title_string = title_string.split("(")[0].strip()
    return title_string


def get_movie_value(soup, field_name):
    """
    takes a string attribute of a movie on the page, and return the string in the next sibling object
    (the value for that attribute)
    """
    obj = soup.find(text = re.compile(field_name))
    if not obj:
        return None
    next_sibling = obj.findNextSibling()

    if next_sibling:
        return next_sibling.text
    else:
        next_sibling = obj.find_next().text.encode('ascii','ignore') #
        return next_sibling     #


def get_all_data(gsoup):

    headers2 = ["movie title", "domestic total gross", "distributor", "Genre", "release date", "runtime", "rating", "widest release"]
    title_string = get_movie_title(gsoup)
    dtg = get_movie_value(gsoup, "Domestic Total")
    disb = get_movie_value(gsoup, "Distributor")
    genre = get_movie_value(gsoup, "Genre:")
    runtime = get_movie_value(gsoup, "Runtime")
    rating = get_movie_value(gsoup, "MPAA Rating")
    release_date = get_movie_value(gsoup, "Release Date")
    widest_release = get_movie_value(gsoup, "Widest")
    movie_dict = dict(zip(headers2, [title_string, dtg, disb, genre, release_date, runtime, rating, widest_release]))
    return movie_dict


###############################################################################

weekly_movie_links = []


def weekly_link_generator(week_links):
    """ generate weekly gross data links in boxofficemojo.com  """

    for link in week_links:
        somelink = link.replace("?id=", "?page=weekly&id=")
        weekly_movie_links.append(somelink)

    return weekly_movie_links


import numpy

movie_wk_dic = {}


def weekly_link2df(links):

    for link in links:
        url = link
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            title = get_movie_title(soup)
            weekly_data = [a.text for a in soup.find(class_="chart-wide").find_all('font')]
            no_dupe_data = cleanup_dup(weekly_data)
            week_array = numpy.array(no_dupe_data)
            week_array = numpy.reshape(week_array, (len(week_array)/9, 9))
            df = pandas.DataFrame(week_array[1:,:],columns=week_array[0,:])
            weekly_df = df.iloc[:,[2,4]]  ## extract weeklygross, theaters, index is week
            movie_wk_dic[title] = weekly_df
        except:
            pass
    return movie_wk_dic


def cleanup_dup(weekly_data):
    num_elements = len(weekly_data)
    no_dupe_elements =[weekly_data[0]]
    for i in range(num_elements-1):
        if weekly_data[i] == '-':
            no_dupe_elements.append(weekly_data[i+1])
        elif weekly_data[i] != weekly_data[i+1]:
            no_dupe_elements.append(weekly_data[i+1])
        else:
            pass

    assert len(no_dupe_elements) % 9 == 0     ## list can be divided by 9
    return no_dupe_elements
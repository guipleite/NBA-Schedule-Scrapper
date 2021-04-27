import mechanicalsoup
# from bs4 import BeautifulSoup
from requests_html import HTMLSession
import dateutil.parser
import datetime
import sys

def get_games(date):
    '''
        Get NBA games on a particular day
        The data is being screapped from the espn.com site
        date:   YYYYMMDD format
    '''

    games_dict = {}
    gameIndex = 0

    browser.open("https://www.espn.com/nba/schedule/_/date/"+date) # URL containig the games for the given date 

    # Opening the link
    schedule_link = browser.find_link()
    browser.follow_link(schedule_link)

    page = browser.get_current_page() # get the page source code
    games = page.find(class_="schedule has-team-logos align-left") # select only the tag that contains the games' info
    desc_all = games.find_all('small') # Game description

    # return games_dict
    for game in games.find_all('tr'):
        teams = []

        contents = game.find_all('td')
        for content in contents:
            for td in content.find_all('abbr'):
                teams.append(td.get('title'))

        if contents:
            element_list = str(contents[2]).split('>')
            gameId = str(element_list[1][52:-36]) # Isolates the game ID
            date = str(element_list[0][41:-1]) # Isolates the result
            time = str(dateutil.parser.parse(date))[:-9] # Converts date time from ISO 8601:

            teams.reverse() # Inverts the order to use the Home vs. Away format
            games_dict[gameId] = teams , time # Adds the game to a dictionary using the ID as key

            gameIndex+=1

    return games_dict

def get_results(date):
    '''
        Get the results NBA games on a particular day
        The data is being screapped from the espn.com site
        date:   YYYYMMDD format
    '''

    games_dict = {}
    gameIndex = 0

    browser.open("https://www.espn.com/nba/schedule/_/date/"+date) # URL containig the games for the given date 

    # Opening the link
    schedule_link = browser.find_link()
    browser.follow_link(schedule_link)

    page = browser.get_current_page() # get the page source code
    games = page.find(class_="schedule has-team-logos align-left") # select only the tag that contains the games' info

    for game in games.find_all('tr'):
        teams = []

        contents = game.find_all('td')
        for content in contents:
            for td in content.find_all('abbr'):
                teams.append(td.get('title'))

        if contents:
            element_list = str(contents[2]).split('>')
            gameId = str(element_list[1][28:-37]) # Isolates the game ID
            result = str(element_list[2][:-3]) # Isolates the result

            teams.reverse() # Inverts the order to use the Home vs. Away format
            games_dict[gameId] = teams , result # Adds the game to a dictionary using the ID as key

            gameIndex+=1

    return games_dict

def main(date):
    '''
    date:   DD/MM/YYYY format
    '''

    now = datetime.datetime.now()

    # Changing the date format to use in the URL
    date_split = date.split('/')
    date = [date_split[2],date_split[1],date_split[0]]
    date = ''.join(date)

    #Checking if the given date is in the past
    if now.year > int(date_split[2]) or now.month > int(date_split[1]) or now.day > int(date_split[0]):
        return get_results(date)    

    else:
        return get_games(date)

if __name__ == "__main__":

    session = HTMLSession()
    browser = mechanicalsoup.StatefulBrowser()
    browser.addheaders = [('User-agent', 'Firefox')]

    # print(main(str(sys.argv[1])))
    print(main(str("28/04/2021")))



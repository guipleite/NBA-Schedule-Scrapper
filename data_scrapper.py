import mechanicalsoup
from requests_html import HTMLSession
import dateutil.parser
import datetime

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

    for game in games.find_all(class_="has-results"):
        teams = []
        teams_t = game.find_all('span')  # Locate the team names

        # Cleanig up the  tags, etc...
        for team in teams_t:
            teams.append(str(team)[6:-7])

        teams.reverse() # Inverts the order to use the Home vs. Away format
       
        time_and_id = str(game.find_all('td')[2]) # Locates a tag that contains both the game ID and time
    
        time_ISO  = time_and_id[41:-107] # Isolates the time the game will happen
        time = str(dateutil.parser.parse(time_ISO))[:-9] # Converts date time from ISO 8601:

        gameId = str(time_and_id[110:-46]) # Isolates the game ID

        games_dict[gameId] = teams , time , str(desc_all[gameIndex])[7:-8] # Adds the game to a dictionary using the ID as key

        gameIndex+=1

    print(games_dict)

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

    desc_all = games.find_all('small') # Game description

    for game in games.find_all(class_="has-results"):
        teams = []
        teams_t = game.find_all('span')  # Locate the team names

        # Cleanig up the  tags, etc...
        for team in teams_t:
            teams.append(str(team)[6:-7])

        teams.reverse() # Inverts the order to use the Home vs. Away format
        
        result_and_id = game.find_all('td') # Locates a tag that contains both the game ID and the result
        element_list = str(result_and_id[2]).split('>')
        gameId = str(element_list[1][26:-37]) # Isolates the game ID
        result = str(element_list[2][:-3]) # Isolates the result

        games_dict[gameId] = teams , result , str(desc_all[gameIndex])[7:-8] # Adds the game to a dictionary using the ID as key

        gameIndex+=1

    print(games_dict)

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
        get_results(date)    

    else:
        get_games(date)

if __name__ == "__main__":

    
    session = HTMLSession()
    browser = mechanicalsoup.StatefulBrowser()
    browser.addheaders = [('User-agent', 'Firefox')]


    date = "25/08/2020"

    main(date)


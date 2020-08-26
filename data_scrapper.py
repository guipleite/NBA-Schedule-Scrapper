import mechanicalsoup
from requests_html import HTMLSession
import dateutil.parser

session = HTMLSession()
browser = mechanicalsoup.StatefulBrowser()
browser.addheaders = [('User-agent', 'Firefox')]

def get_games(date):
    '''
        Get NBA games on a particular day
        The data is being screapped from the espn.com site
        date:   DD/MM/YYYY format
    '''

    # Changing the date format to use in the URL
    date_split = date.split('/')
    date = [date_split[2],date_split[1],date_split[0]]
    date = ''.join(date)

    browser.open("https://www.espn.com/nba/schedule/_/date/"+date) # URL containig the games for the given date 

    # Opening the link
    schedule_link = browser.find_link()
    browser.follow_link(schedule_link)

    games_dict = {}
    gameIndex = 0

    page = browser.get_current_page() # get the page source code

    games = page.find(class_="schedule has-team-logos align-left")     # select only the tag that contains the games' info

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

        games_dict[gameId] = teams , time , str(desc_all[gameIndex])[7:-8] # Adds the game to a dictionary using the ID as index

        gameIndex+=1

    return games_dict


date = "26/08/2020"

get_games(date)

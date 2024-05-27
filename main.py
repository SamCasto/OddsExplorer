#Author: Samuel Casto
#Description: Streamlit site that gets betting information from TheOdds API and displays it for 
#   users to make more beneficial bets for themselves.
#Goals: 
#   1. Add some kind of cache function for the league data page to limit API calls
#   2. Add more scores check functionality and maybe a way to limit the API calls
#   3. Clean up word choice across site

import streamlit as st
import requests
import pandas as pd
from keys import API_KEY




#api key moved to file calles keys.py 

#api endpoint construction
SPORT = 'americanfootball_nfl'
REGIONS = 'us'
MARKETS = 'h2h,spreads,totals'
BOOKMAKERS = 'betmgm,draftkings,fanduel,williamhill_us'
API_ENDPOINT = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}&bookmakers={BOOKMAKERS}'

#Team selection for team specific odds
TEAMS = [
    'Arizona Cardinals','Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 
    'Chicago Bears', 'Cincinnati Bengals',
    'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
    'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts',
    'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers',
    'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots',
    'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles',
    'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers',
    'Tennessee Titans', 'Washington Football Team'
]

#Team dictionary for holding relevant info
TEAMS_COLUMNS = ["H2H Price","Spread Price","Spread Total","Over Price","Under Price","Over/Under Line"]
TEAMS_PRICE = { #goes h2h price, spread price, spread number, over price, under price, over under number
    'Arizona Cardinals': [0, 0, 0, 0, 0, 0],
    'Atlanta Falcons': [0, 0, 0, 0, 0, 0],
    'Baltimore Ravens': [0, 0, 0, 0, 0, 0],
    'Buffalo Bills': [0, 0, 0, 0, 0, 0],
    'Carolina Panthers': [0, 0, 0, 0, 0, 0],
    'Chicago Bears': [0, 0, 0, 0, 0, 0],
    'Cincinnati Bengals': [0, 0, 0, 0, 0, 0],
    'Cleveland Browns': [0, 0, 0, 0, 0, 0],
    'Dallas Cowboys': [0, 0, 0, 0, 0, 0],
    'Denver Broncos': [0, 0, 0, 0, 0, 0],
    'Detroit Lions': [0, 0, 0, 0, 0, 0],
    'Green Bay Packers': [0, 0, 0, 0, 0, 0],
    'Houston Texans': [0, 0, 0, 0, 0, 0],
    'Indianapolis Colts': [0, 0, 0, 0, 0, 0],
    'Jacksonville Jaguars': [0, 0, 0, 0, 0, 0],
    'Kansas City Chiefs': [0, 0, 0, 0, 0, 0],
    'Las Vegas Raiders': [0, 0, 0, 0, 0, 0],
    'Los Angeles Chargers': [0, 0, 0, 0, 0, 0],
    'Los Angeles Rams': [0, 0, 0, 0, 0, 0],
    'Miami Dolphins': [0, 0, 0, 0, 0, 0],
    'Minnesota Vikings': [0, 0, 0, 0, 0, 0],
    'New England Patriots': [0, 0, 0, 0, 0, 0],
    'New Orleans Saints': [0, 0, 0, 0, 0, 0],
    'New York Giants': [0, 0, 0, 0, 0, 0],
    'New York Jets': [0, 0, 0, 0, 0, 0],
    'Philadelphia Eagles': [0, 0, 0, 0, 0, 0],
    'Pittsburgh Steelers': [0, 0, 0, 0, 0, 0],
    'San Francisco 49ers': [0, 0, 0, 0, 0, 0],
    'Seattle Seahawks': [0, 0, 0, 0, 0, 0],
    'Tampa Bay Buccaneers': [0, 0, 0, 0, 0, 0],
    'Tennessee Titans': [0, 0, 0, 0, 0, 0],
    'Washington Football Team': [0, 0, 0, 0, 0, 0],
}
#Radio button options for books
RADIO_BOOKS = ['BetMGM','DraftKings','FanDuel','Caesar\'s']

#Multiselect box options for odds to find
MARKET_SELECT = ['h2h','spreads','totals']

#Table columns for NFL League Data
TABLE_COLUMNS = ['h2h price','spread price','spread value','over value','under value','over/under price']


#Every comment after this will be a feature needed to satisfy requirements for the app assignment

#Map element
#Not sure how we are going to include this but likely stadium address somehow

#function to highlight the winning score in a data frame object
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: #b4fab4 ' if v else '' for v in is_max]

#actual app
def main():
    #Setting title and header for page
    st.title("Odds Explorer")
    
    #Success Box, Info Box, Error Box
    #Success and Error will be used when retrieving data
    st.info(''':red[DISCLAIMER: Gambling involves risk. Please only gamble with funds that you can comfortably 
        afford to lose. Call 1-800-GAMBLER if you or a loved one has a gambling problem to seek help.]''',icon="❗")
    

    #Creating sidebar to select flight search option
    sidebar = ["Specific NFL Team Data","NFL League Data","Scores Check","Site Info","Roadmap",]
    category = st.sidebar.selectbox("Options",sidebar,index=3)


    if(category == 'Specific NFL Team Data'):
        #Need to set up header
        st.header("Explore Odds for a Specific NFL Team")
        #Selectbox for NFL team, Multi selectbox will be for odds(h2h,spreads,totals) 
        #user is looking up only a single team and will use a selectbox
        selectedTeam = st.selectbox(label='Select the team:',options=TEAMS,index=None)
        #We need to know what odds to look for
        marketSelect = st.multiselect(label="Select the markets to find:",options=MARKET_SELECT)
        #1 Button widget
        #Will be go button on a particular page to return results
        #we need a go button so we know when our user has selected all their information
        go = st.button(label="Get results")
        if(go and marketSelect and selectedTeam):
            #we have team and book as strings to put into a table
            #while marketSelect is a list of strings
            #our table should have the columns of the markets and rows of the sports book(s)
            #st.write(marketSelect)
            #st.write(team)
            #st.write(book)

            #Dictionary that will hold the data relevant to the specific team
            SPEC_TEAM = {#book prices going mgm, draftkings, fanduel, ceasars 
                "h2h":[0,0,0,0],
                "spreads":[0,0,0,0],
                "spread line":[0,0,0,0],
                "over":[0,0,0,0],
                "under":[0,0,0,0],
                "total line":[0,0,0,0],
                }
            #we can't pass the marketSelect option directly into the API so based off its value we 
            #have to define marketPass into something the API will accept
            if set(marketSelect) == {"h2h"}:
                marketPass = 'h2h'
            elif set(marketSelect) == {"spreads"}:
                marketPass = 'spreads'
            elif set(marketSelect) == {"totals"}:
                marketPass = 'totals'
            elif set(marketSelect) == {"h2h","spreads"}:
                marketPass = 'h2h,spreads'
            elif set(marketSelect) == {"spreads","totals"}:
                marketPass = 'spreads,totals'
            elif set(marketSelect) == {"h2h","totals"}:
                marketPass = 'h2h,totals'
            elif set(marketSelect) == {"h2h","spreads","totals"}:
                marketPass = 'h2h,spreads,totals'

            #st.write(marketPass)
            #api call here with our updated data
            callURL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={marketPass}&bookmakers={BOOKMAKERS}&oddsFormat=american'
            callData = requests.get(callURL).json()
            #We've called the api and callData has our request, now we need to parse it
            matchFlag = False #for when we find our wanted team once
            for id in callData: #iterating over our JSON we recieved
                #we need to save the name of the bookmaker to update the right spot in the list
                for bookie in id['bookmakers']:
                        sportsbook = bookie['key']
                        if sportsbook == 'betmgm':
                            index = 0
                        elif sportsbook == 'fanduel':
                            index = 2
                        elif sportsbook == 'draftkings':
                            index = 1
                        elif sportsbook == 'williamhill_us':
                            index = 3
                        for market in bookie['markets']:
                            #we have the name of the book and the market key, now we just need to
                            #get and update the right values with it
                            marketKey = market['key']
                            for outcome in market['outcomes']:
                                #we are going to iterate over both outcomes and seeing if the name
                                #matches the team name selected. If so then we will grab enter
                                #another if statement tree based on marketKey value
                                if outcome['name'] == selectedTeam:
                                    #we found a match and just need to update the info based on
                                    #the marketKey
                                    price = outcome['price']
                                    SPEC_TEAM[marketKey][index] = price
                                    if marketKey == 'spreads':
                                        point = outcome['point']
                                        SPEC_TEAM['spread line'][index] = point
                                    break
                                elif outcome['name'] == "Over":
                                    if id['home_team'] == selectedTeam or id['away_team'] == selectedTeam:
                                        over = outcome['price']
                                        total = outcome['point']
                                        SPEC_TEAM['over'][index] = over
                                        SPEC_TEAM['total line'][index] = total
                                elif outcome['name'] == 'Under':
                                    if id['home_team'] == selectedTeam or id['away_team'] == selectedTeam:
                                        under = outcome['price']
                                        SPEC_TEAM['under'][index] = under

            #Our table uses the sportsbooks as the columns and the markets as the index. Based 
            #on our number of markets we will need to update the above code to grab the data
            #only for the specific team. We will display the over under total and the spread
            #for the specific team so we can only grab the prices when parsing otherwise making
            #the table would be a pain in the ass
            if set(marketSelect) == {"h2h"}:
                table = pd.DataFrame({"h2h":SPEC_TEAM['h2h']})
            elif set(marketSelect) == {"spreads"}:
                table = pd.DataFrame({"spreads":SPEC_TEAM['spreads'], "spreads line":SPEC_TEAM['spread line']})
            elif set(marketSelect) == {"totals"}:
                table = pd.DataFrame({"over":SPEC_TEAM['over'],"under":SPEC_TEAM['under'],"total":SPEC_TEAM['total line']})
            elif set(marketSelect) == {"h2h","spreads"}:
                table = pd.DataFrame({"h2h":SPEC_TEAM['h2h'],"spreads":SPEC_TEAM['spreads'], "spreads line":SPEC_TEAM['spread line']})
            elif set(marketSelect) == {"spreads","totals"}:
                table = pd.DataFrame({"spreads":SPEC_TEAM['spreads'], "spreads line":SPEC_TEAM['spread line'],"over":SPEC_TEAM['over'],"under":SPEC_TEAM['under'],"total":SPEC_TEAM['total line']})
            elif set(marketSelect) == {"h2h","totals"}:
                table = pd.DataFrame({"h2h":SPEC_TEAM['h2h'],"over":SPEC_TEAM['over'],"under":SPEC_TEAM['under'],"total":SPEC_TEAM['total line']})
            elif set(marketSelect) == {"h2h","spreads","totals"}:
                table = pd.DataFrame({"h2h":SPEC_TEAM['h2h'],"spreads":SPEC_TEAM['spreads'], "spreads line":SPEC_TEAM['spread line'],"over":SPEC_TEAM['over'],"under":SPEC_TEAM['under'],"total":SPEC_TEAM['total line']})
            #Formatting the table
            table = table.transpose()
            table.index.name = selectedTeam
            table.set_axis(RADIO_BOOKS,axis=1,)
            #writing the table
            st.dataframe(data=table,use_container_width=True)

            st.write("Here is a visual representation of the values in relation to each other:")
            #Chart #1 Line chart
            #Line chart can be used to show the different moneylines by book makers
            st.scatter_chart(table,size=150,use_container_width=True,height=400,color=['#f50505','#0509f5','#05f5e9','#aeba02'])
           
        elif(go and not marketSelect):
            #we need to print an error message that the user needs to select a market
            st.warning(f'Please be sure to select at least one market to get results.')
        elif(go and not team):
            st.warning(f'select team')

        #End of Specific Team Info Category
        #
        #

    elif(category == "NFL League Data"):
        #Here we will make a large API call and use only a specific sports book to compare
        #all the games lines
        #Need to set header
        st.header("Explore Odds on All Teams from a Sportsbook")
        #RadioButton to select sportsbooks
        #User will see all teams, now we need to know what book the user wants
        book = st.radio(label="Select which sports book to return results from:",options=RADIO_BOOKS,
                 index=0,horizontal=True)
        #based off our radio button book, we need to decide which book
        if(book == "BetMGM"):
            bookPass = 'betmgm'
        elif(book == "FanDuel"):
            bookPass = 'fanduel'
        elif(book == "DraftKings"):
            bookPass = 'draftkings'
        elif(book == "Caesar's"):
            bookPass = 'williamhill_us'

        go = st.button(label="Get bookmaker results")
        if(go):
            #so here we are calling the API and getting all the markets related to the book
            #called in the API
            #not letting the user pick markets this time around #yolo
            callURL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}&bookmakers={bookPass}&oddsFormat=american'
            callData = requests.get(callURL).json()
            
            #we need to parse our API return to find the price for the markets based on the team name
            #and create a dict to hold these prices
            for id in callData:
                for bookmaker in id["bookmakers"]:
                    for market in bookmaker["markets"]:
                        marketKey = market["key"]
                        for outcome in market["outcomes"]:
                            #at this point we have the marketKey, teamName, and price
                            #and need to create our first column for the table
                            if(marketKey == "h2h"):
                                price = outcome["price"]
                                teamName = outcome["name"]
                                for team, values in TEAMS_PRICE.items():
                                    if team == teamName:
                                        values[0] = price
                                        break
                            elif(marketKey == "spreads"):
                                #for spreads we also have to get the spread value
                                price = outcome["price"]
                                teamName = outcome["name"]
                                spread = outcome["point"]
                                for team, values in TEAMS_PRICE.items():
                                    if team == teamName:
                                        values[1] = price
                                        values[2] = spread
                                        break 
                            elif(marketKey == "totals"):
                                #for totals we also have to get over under price and value
                                #and assign it to each team
                                if(outcome["name"] == "Over"):
                                    #we have to iterate over this twice regardless to get the under
                                    #and we have to repeat this action to have each team have 
                                    #and over under value
                                    teamName = id["home_team"]
                                    price = outcome["price"]
                                    point = outcome["point"]
                                    for team, values in TEAMS_PRICE.items():
                                        if team == teamName:
                                            #over under price and point total
                                            values[3] = price
                                            values[5] = point
                                            break
                                    teamName = id["away_team"]
                                    for team, values in TEAMS_PRICE.items():
                                        if team == teamName:
                                            #over under price and point total
                                            values[3] = price
                                            values[5] = point
                                            break
                                elif(outcome["name"] == "Under"):
                                    #we iterated again to get ONLY the under
                                    teamName = id["away_team"]
                                    price = outcome["price"] #only need the under value
                                    for team, values in TEAMS_PRICE.items():
                                        if team == teamName:
                                            #over under price and point total
                                            values[4] = price
                                            break
                                    teamName = id["home_team"]
                                    price = outcome["price"] #only need the under value
                                    for team, values in TEAMS_PRICE.items():
                                        if team == teamName:
                                            #over under price and point total
                                            values[4] = price
                                            break
                                


                                
            
            
            #A table needs to be created using a dataFrame and the dataFrame is going to have several 
            #different sportsbooks data for the team selected
            #REFERENCE FOR THIS TABLE COLUMNS
            '''0 = h2h price
            1 = spread price
            2 = spread value
            3 = over value 
            4 = under value
            5 = over/under price'''
            #The table uses the list of TEAMS as an index and the markets for columns while the data
            #will be the price value from the JSON document for the team
            table = pd.DataFrame(data=TEAMS_PRICE)
            #Swap the team names to be the index
            table = table.transpose()
            #Add a name to the index in the top left corner of the eventual table
            table.index.name = "Team"
            #Team names are added now we need to remove unnessecary columns and 
            table.columns = TABLE_COLUMNS
            
            
            #and then we need to find out a way to inlude text input using one of the other API endpoints
            st.write(f"Bookmaker results for {book}")
            st.dataframe(data=table,use_container_width=True,height=400)

            
            #Chart 2 Bar chart
            #Showing the different prices for the sportsbooks represented as bars
            st.write("Here is a visual representation of the values in relation to each other:")
            st.bar_chart(data=table,use_container_width=True,height=600)
            
            #End of NFL League Data Category
            #
            #

    elif(category == "Site Info"):
        #updating header
        st.header("Site Information and Purpose")
        
        #Information about what the site does and should be used for
        st.write(f'''The purpose of this site is to allow users to find relevant sports betting data 
                on NFL games whether that is a single team across all sportsbooks or all NFL games
                from a single sportsbook. This site is not intended to be used to facilitate or 
                encourage excessive or irresponsible gambling behavior. It is crucial to approach 
                sports betting with caution and a responsible mindset. This site should not be 
                utilized as a platform for promoting or engaging in compulsive gambling habits.''')
         
        #Need info on how winnings are calculated
        st.subheader("What do Odds or Price mean:",divider="blue")
        st.write('''In betting, positive numbers (e.g., +200) on the moneyline signify the potential
                  profit on a \$100 bet, indicating that a +200 moneyline would yield a \$200 win on a
                  \$100 bet. Conversely, negative numbers (e.g., -150) indicate the amount you must
                  wager to win \$100, meaning a -150 moneyline requires a \$150 bet to secure a \$100
                  profit. These representations help bettors assess potential returns and risks in
                  terms of their betting unit.''')
         
        #Need info on what spread totals mean
        st.subheader("What do Spread Totals mean:",divider="blue")
        st.write('''In betting, spread totals are often expressed as positive or negative numbers,
                  and they represent the margin of victory or defeat a team must achieve. Positive 
                 numbers (e.g., +7.5) indicate the number of points an underdog can either lose by 
                 or win by for a bet to be successful. For example, a +7.5 spread means the team
                  can lose by seven points or win outright for a bet to win. Conversely, negative 
                 numbers (e.g., -4.5) represent the margin a favorite must win by to cover the 
                 spread. A -4.5 spread implies the favored team must win by at least five points 
                 for the bet to be successful. These spread total representations assist bettors 
                 in evaluating potential returns and risks based on a standardized unit.
                    ''')
         
        #Need info on what over under totals mean
        st.subheader("What do Over Under Totals mean:",divider="blue")
        st.write('''In betting, over/under, or totals, are expressed as a line representing the 
                 combined score of both teams in a game. For instance, a totals line of 200 points 
                 means bettors can wager on whether the actual combined score will be over or under 
                 200 points. If you bet the over and the final score surpasses 200 points, your bet 
                 wins; if it falls below, you lose. Conversely, if you bet the under and the final 
                 score is less than 200 points, your bet is successful. 
                    ''')
         
        #Need info on what a 0 means in our tables, there is no value 
        st.subheader("What does the data in my tables mean:",divider="blue")
        st.write('''H2H Price stands for the head to head or moneyline odds for that team. 
                 The Spread Price stands for the spread odds for that team. The Over and Under Price
                 stand for the over and under odds for that team respectively. If there is a 0 value
                 in one of the tables, there are several options for why. The team could be on their bye
                 week or have already finished their game for the week, and the sportsbook hasn't 
                 made the team's next odds. The sportsbook for some reason could not be taking bets
                 for that particular market and team.
                    ''')
         
        
        #API information
        st.subheader("API Information",divider="blue")
        st.write('''The API used to make this app was the odds-api. You can check out their 
                 website at: [https://the-odds-api.com/.](https://the-odds-api.com/) I would like 
                 to take the time to thank them because using this API has been really fun and a 
                 great learning experience. Just a heads up, this API can be costly with the number
                 of calls you might need to make given their formula and the other ways to use their
                 API as well as there being a hard limit on the free plan. The normal formula for 
                 these API calls are number of markets * number of regions. ''')
             
        #End of Site Info Category
        #
        #
        
    elif category == "Roadmap":
        st.header("Roadmap of Planned Future Updates")

        st.subheader("Current as of 12/9/2023:",divider="blue")
        st.write("1. Update code to use cache functions to allow API calls to persist.")
        st.write("2. Move score finder to it's own page and look into extra functionality that could be added.")
        st.write("3. Maybe find out how to use the damn CSS styles with this stuff to make the page look better.")
        st.write("4. See if there is a way to get more NFL scores for the Scores Check page.")
        st.caption("The order of the updates does not determine the order they will be implemented.")

        #End of Roadmap Category
        #
        #
    
    elif category == "Scores Check":
        st.header("NFL Scores within 3 days")

        st.write('''The API call currently being used only retrieves NFL scores from at most, 
                 the past 3 days. I will look into using a different API call if possible or
                 if I should use a different API altogether to get these scores.''')
        stop = False
        selCheck = st.button("Check Scores")
        if selCheck and stop:
            callURL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/scores/?daysFrom=3&apiKey={API_KEY}'
            callData = requests.get(callURL).json()
            #iterating over the response to build our dataframe to display
            tempTable = {}
            scores = pd.DataFrame(tempTable)
            for id in callData:
                #st.write(id['completed'])
                #Only returning completed games
                if id['completed']:
                    homeTeam = id['home_team']
                    awayTeam = id['away_team']
                    homeScore = id['scores'][1]['score']
                    awayScore = id['scores'][0]['score']

                    newRow = {'Home Team':homeTeam,'Home Score':homeScore,'Away Score':awayScore,'Away Team':awayTeam}
                    scores = scores.append(newRow, ignore_index=True)
            scores['Home Score'] = pd.to_numeric(scores['Home Score'])
            scores['Away Score'] = pd.to_numeric(scores['Away Score'])
            styled_scores = scores.style.apply(highlight_max, subset=['Home Score', 'Away Score'], axis=1)
            st.dataframe(styled_scores,use_container_width=True,height=300,hide_index=True)   
        
        #End of Scores Check Category
        #
        #
        

    #1 Checkbox widget
    #Will be used to display gambling terms
    #definition checkboxes
    unitDef = st.sidebar.checkbox("Unit Definition")
    bookDef = st.sidebar.checkbox("Sportsbook Definition")
    marketDef = st.sidebar.checkbox("Market Definition")
    betDef = st.sidebar.checkbox("Bet Definitions")
    #container holding definitions under the checkboxes in the sidebar
    checkBoxDef = st.sidebar.container()
    #writing checkbox definitions if the button is clicked
    if(unitDef):
        checkBoxDef.write('''A unit represents a specific currency amount that is used to measure 
                             a bet's relative size. For example, if you choose a betting unit of \$10, 
                             then betting two units would have you risking \$20.''')
    if(bookDef):
        checkBoxDef.write('''An establishment that takes bets on sporting events and pays out winnings
                          for winning bets. Losing bets funds are kept by the sportsbook. ''')
    if(marketDef):
        checkBoxDef.write('''Markets are the various types of wagers people can bet on. Specifically for 
                          this application we have h2h, spreads, and totals. These represent moneyline,
                          points handicaps, and over/under.''')
    if(betDef):
        checkBoxDef.write('''Moneyline betting is betting on the winner of the contest. Points 
                          handicaps betting is betting on the amount a team will either win by or 
                          lose by. Over under betting is betting on the amount of points scored
                          by either team or combined by both teams.''' )
    
#starting the web app
if __name__ == "__main__":
    main()
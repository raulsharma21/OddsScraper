import sys
import pandas as pd
from Bwin.get2 import getBwinFootball
from Unibet.get import getUnibetFootball
from Netbet.get import getNetbetFootball

from fuzzywuzzy import process, fuzz
from unidecode import unidecode
import spacy
nlp = spacy.load("en_core_web_sm")

bwinFootball = None
unibetFootball = None
netbetFootball = None
df = None

def find_most_similar(input_string, standard_strings):
    input_doc = nlp(input_string)
    most_similar_string = None
    highest_similarity = -1

    for standard_string in standard_strings:
        similarity = input_doc.similarity(nlp(standard_string))
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_string = standard_string
    
    return most_similar_string, highest_similarity

def getStandardGamesSet():
    # standard_games = []
    # for i in range(0, len(bwinFootball["Team 1"])):
    #     row = bwinFootball.iloc[i]
    #     game_string = unidecode(row['Team 1']) + ' ' + unidecode(row['Team 2'])
    #     standard_games.append(game_string)

    standard_games_set = set()
    for i in range(0, len(bwinFootball["Team 1"])):
        row = bwinFootball.iloc[i]
        game_string = unidecode(row['Team 1']) + ' ' + unidecode(row['Team 2'])
        standard_games_set.add(game_string)
    return standard_games_set

def matchUnibet(standard_games_set,df):
    
    home = [None] * len(df['Team 1'])
    draw = [None] * len(df['Team 1'])
    away = [None] * len(df['Team 1'])
    count = 0
    for i in range (0, len(unibetFootball["Team 1"])):
        unibet_row = unibetFootball.iloc[i]
        team1 = unidecode(unibet_row['Team 1'])
        team2 = unidecode(unibet_row['Team 2'])
        game = team1 + ' ' + team2
        if'(W)' in game:
            game = game.replace('(W)', 'Women')

        result = process.extract(game, standard_games_set, limit=1)
        best_match, similarity_score = result[0]

        if similarity_score>86:
            # df_row = df[(df['Team 1'] + ' ' + df['Team 2']) == best_match]
            index = (df['Team 1'] + ' ' + df['Team 2']).eq(best_match).idxmax()
            

            # print('Accepted: ')
            # print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
            # print()

            if not pd.isnull(index):
                count += 1
                home[index] = unibet_row["Home Odds"]
                draw[index] = unibet_row["Draw Odds"]
                away[index] = unibet_row["Away Odds"]
                
            else:
                print("Best Match Not found in Dataframe")
        # else:
        #     print('Rejcted: ')
        #     print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
        #     print()

    df["Unibet Home Odds"] = home
    df["Unibet Draw Odds"] = draw
    df["Unibet Away Odds"] = away
    print("Unibet Accepted: " + str(count))

    # for i in range (0, len(unibetFootball["Team 1"])):
    #     unibet_row = unibetFootball.iloc[i]
    #     team1 = unidecode(unibet_row['Team 1'])
    #     team2 = unidecode(unibet_row['Team 2'])

        

    #     game = team1 + ' ' + team2
    #     if'(W)' in game:
    #         game = game.replace('(W)', 'Women')

    #     result = process.extract(game, standard_games_set, limit=1)
    #     best_match, similarity_score = result[0]


    #     if similarity_score>86:

    #         bwin_row = bwinFootball[(bwinFootball['Team 1'] + ' ' + bwinFootball['Team 2']) == best_match]

    #         if not bwin_row.empty:
                
    #             data.append([bwin_row["Team 1"].iloc[0], bwin_row["Team 2"].iloc[0], unibet_row["Home Odds"],unibet_row["Draw Odds"],unibet_row["Away Odds"],bwin_row["Home Odds"].iloc[0],bwin_row["Draw Odds"].iloc[0],bwin_row["Away Odds"].iloc[0]])
    #             # if similarity_score < 93:
    #             #     print('Accepted: ')
    #             #     print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
    #             #     print()
    #         else:
    #             print("Best Match Not found in Bwin")
    #     # else:
    #     #     print('Rejcted: ')
    #     #     print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
    #     #     print()

def matchNetbet(standard_games_set,df):
    home = [None] * len(df['Team 1'])
    draw = [None] * len(df['Team 1'])
    away = [None] * len(df['Team 1'])
    count = 0
    for i in range (0, len(netbetFootball["Team 1"])):
        netbet_row = netbetFootball.iloc[i]
        team1 = unidecode(netbet_row['Team 1'])
        team2 = unidecode(netbet_row['Team 2'])
        game = team1 + ' ' + team2
        if'(Wom)' in game:
            game = game.replace('(W)', 'Women')

        result = process.extract(game, standard_games_set, limit=1)
        best_match, similarity_score = result[0]

        if similarity_score>86:
            # df_row = df[(df['Team 1'] + ' ' + df['Team 2']) == best_match]
            index = (df['Team 1'] + ' ' + df['Team 2']).eq(best_match).idxmax()
            if 'Santa Hel' in game:
                print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
                print()

            # print('Accepted: ')
            # print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
            # print()
            

            if not pd.isnull(index):
                count += 1
                home[index] = netbet_row["Home Odds"]
                draw[index] = netbet_row["Draw Odds"]
                away[index] = netbet_row["Away Odds"]
                
            else:
                print("Best Match Not found in Dataframe")
        # else:
        #     print('Rejcted: ')
        #     print(unidecode(game) + ' ' + best_match + ' ' + str(similarity_score))
        #     print()

    df["Netbet Home Odds"] = home
    df["Netbet Draw Odds"] = draw
    df["Netbet Away Odds"] = away
    print("Netbet Accepted: " + str(count))
            
    

def initializeDataframes():
    global bwinFootball, unibetFootball, netbetFootball
    unibetFootball = getUnibetFootball()
    unibetFootball.to_pickle('unibet_df.pkl')

    netbetFootball= getNetbetFootball()
    netbetFootball.to_pickle('netbet_df.pkl')

    # while True:
    #     user_input = input("Is your region set to the US (y/n): ")
        
    #     if user_input.lower() == 'y':
    #         print("Continuing...")
    #         break
    #         # Your code to continue goes here
            
    #     elif user_input.lower() == 'n':
    #         print("Terminating script.")
    #         sys.exit()
        
    #     else:
    #         print("Invalid input. Please enter 'y' to continue, 'n' to terminate, or any other key to retry.")

    bwinFootball = getBwinFootball()
    bwinFootball.to_pickle('bwin_df.pkl')

    # bwinFootball = pd.read_pickle('bwin_df.pkl')
    # unibetFootball = pd.read_pickle('unibet_df.pkl')
    # netbetFootball = pd.read_pickle('netbet_df.pkl')

    # print(bwinFootball.to_string())
    # print(netbetFootball.to_string())
    # print(unibetFootball.to_string())



def retrieveAllData():
    global df
    initializeDataframes()

    standard_games_set = getStandardGamesSet()
    columns_to_include = ["Team 1", "Team 2", "Home Odds", "Draw Odds", "Away Odds"]
    df = bwinFootball[columns_to_include].copy()
    new_column_names = ["Team 1", "Team 2", "Bwin Home Odds", "Bwin Draw Odds", "Bwin Away Odds"]
    df = df.rename(columns=dict(zip(df.columns, new_column_names)))

    matchNetbet(standard_games_set, df)    
    matchUnibet(standard_games_set, df)

    df.to_csv('output.csv', index=False)

    print('Bwin Length: ' + str(len(bwinFootball["Team 1"])))
    print('Unibet Length: ' + str(len(unibetFootball["Team 1"])))
    print('Netbet Length: ' + str(len(netbetFootball["Team 1"])))
    print('Matched Length: '+ str(len(df["Team 1"])))

def printBetAndProfit(bet_home, bet_draw, bet_away, profit_home, profit_draw, profit_away):
    print("Bet sizes: Home - {:.2f}, Draw - {:.2f}, Away - {:.2f}".format(bet_home, bet_draw, bet_away))
    print("Profits: Home - {:.2f}, Draw - {:.2f}, Away - {:.2f}".format(profit_home, profit_draw, profit_away))
    print()

def checkForArbitrage():
    opportunities_found = 0
    for index, row in df.iterrows():

        best_home = 0
        best_draw = 0
        best_away = 0

        bet_home = 0
        bet_draw = 0
        bet_away = 0

        for column in df.columns:
            if 'Home' in column and row[column] is not None:
                value = pd.to_numeric(row[column], errors='coerce')  
                if not pd.isna(value) and best_home < value:
                    best_home = value
            elif 'Draw' in column and row[column] is not None:
                value = pd.to_numeric(row[column], errors='coerce')
                if not pd.isna(value) and best_draw < value:
                    best_draw = value
            elif 'Away' in column and row[column] is not None:
                value = pd.to_numeric(row[column], errors='coerce')
                if not pd.isna(value) and best_away < value:
                    best_away = value

        implied_probability = 1/best_home + 1/best_draw + 1/best_away 
        if implied_probability < 1:
            opportunities_found += 1

            total_investment = 100  # Total amount to invest (you can change this)
            implied_prob_home = 1 / best_home
            implied_prob_draw = 1 / best_draw
            implied_prob_away = 1 / best_away

            # Calculate bet sizes based on implied probabilities
            bet_home = (total_investment * implied_prob_home) / implied_probability
            bet_draw = (total_investment * implied_prob_draw) / implied_probability
            bet_away = (total_investment * implied_prob_away) / implied_probability

            profit_home = bet_home * best_home - total_investment
            profit_draw = bet_draw * best_draw - total_investment
            profit_away = bet_away * best_away - total_investment

            
            print("ARBITRAGE!!!!")
            print(row['Team 1'] + ' ' + row['Team 2'])
            print(str(best_home) + ' ' + str(best_draw) + ' ' + str(best_away))  
            print('Implied Probability: ' + str(implied_probability))
            printBetAndProfit(bet_home, bet_draw, bet_away, profit_home, profit_draw, profit_away)



            print()

    if(opportunities_found == 0):
        print("No opportunities found") 
                



retrieveAllData()
checkForArbitrage()
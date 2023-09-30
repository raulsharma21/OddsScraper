from Bwin.get2 import getBwinFootball
from Netbet.get import getNetbetFootball
from Unibet.get import getUnibetFootball
import pandas as pd
import sys

from fuzzywuzzy import process, fuzz

from unidecode import unidecode


unibetFootball = getUnibetFootball()

while True:
    user_input = input("Is your region set to the US (y/n): ")
    
    if user_input.lower() == 'y':
        print("Continuing...")
        break
        # Your code to continue goes here
        
    elif user_input.lower() == 'n':
        print("Terminating script.")
        sys.exit()
    
    else:
        print("Invalid input. Please enter 'y' to continue, 'n' to terminate, or any other key to retry.")

bwinFootball = getBwinFootball()
# netbetFootball = getNetbetFootball()

standard_names = []
standard_names.extend(bwinFootball["Team 1"].tolist())
standard_names.extend(bwinFootball["Team 2"].tolist())


data = []


# for team in unibetFootball["Team 1"]:
#     print(team + " " + process.extractOne(team, standard_names)[0] + " " + str(process.extractOne(team, standard_names)[1]))
for i in range (0, len(unibetFootball["Team 1"])):
    unibet_row = unibetFootball.iloc[i]
    team1 = unibet_row['Team 1']
    team2 = unibet_row['Team 2']

    result1 = process.extract(unidecode(team1), standard_names,limit=1)
    best_match1, similarity_score1 = result1[0]

    result2 = process.extract(unidecode(team2), standard_names,limit=1)
    best_match2, similarity_score2 = result2[0]


    if similarity_score1>86 and similarity_score2>86:

        bwin_row = bwinFootball[(bwinFootball['Team 1'] == best_match1) & (bwinFootball['Team 2'] == best_match2)]

        if not bwin_row.empty:
            
            data.append([best_match1, best_match2, unibet_row["Home Odds"],unibet_row["Draw Odds"],unibet_row["Away Odds"],bwin_row["Home Odds"].iloc[0],bwin_row["Draw Odds"].iloc[0],bwin_row["Away Odds"].iloc[0]])
        else:
            print("Best Match Not found in Bwin")
    else:
        print('Rejcted: ' + team1 + ' ' + best_match1)

        

    
columns = ["Team 1", "Team 2", "Unibet Home Odds", "Unibet Draw Odds", "Unibet Away Odds", "Bwin Home Odds", "Bwin Draw Odds", "Bwin Away Odds"]
df = pd.DataFrame(data, columns=columns)

print(df.to_string())

print(len(bwinFootball["Team 1"]))
print(len(unibetFootball["Team 1"]))


    
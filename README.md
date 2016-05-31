# CS434 Final Project
## Learning to rank using League of Legends player data

The goal of this project is to use League of Legends player ranked stats to work with a machine learning algorithm. Specifically, we want to use a learning-to-rank algorithm. Instead of predicting the exact rank of a particular player, we will score a set of player and see if we can rank them properly. 

### Data format
Our data will be collected using the [Riot Games API](https://developer.riotgames.com/api/methods) (note: you need a League of Legends game account to get an API key) using the Ranked data for the 2015 season. A typical dump from this method would result in something like this:

    {
        "id": 110,
        "stats": {
            "totalDeathsPerSession": 70,
            "totalSessionsPlayed": 13,
            "totalDamageTaken": 225796,
            "totalQuadraKills": 0,
            "totalTripleKills": 2,
            "totalMinionKills": 2839,
            "maxChampionsKilled": 14,
            "totalDoubleKills": 8,
            "totalPhysicalDamageDealt": 2432161,
            "totalChampionKills": 97,
            "totalAssists": 71,
            "mostChampionKillsPerSession": 14,
            "totalDamageDealt": 2527195,
            "totalFirstBlood": 0,
            "totalSessionsLost": 9,
            "totalSessionsWon": 4,
            "totalMagicDamageDealt": 93558,
            "totalGoldEarned": 173531,
            "totalPentaKills": 0,
            "totalTurretsKilled": 14,
            "mostSpellsCast": 0,
            "maxNumDeaths": 10,
            "totalUnrealKills": 0
        }
    }

Each ranked request uses a player ID and grabs this stat block for each in-game Champion (indicated by the "id" field at the top) they have data for. We'll aggregate this data and create one set of data per player, which will represent the features of our data. 

### Target

The target is the ranked status of the specified player. We can get this data from the API as well:
 
    {"28983665": [{
        "queue": "RANKED_SOLO_5x5",
        "name": "Poppy's Archons",
        "entries": [{
            "leaguePoints": 26,
            "isFreshBlood": false,
            "isHotStreak": false,
            "division": "V",
            "isInactive": false,
            "isVeteran": false,
            "losses": 231,
            "playerOrTeamName": "Skedader",
            "playerOrTeamId": "28983665",
            "wins": 230
        }],
        "tier": "DIAMOND"
    }]}


The specific piece we want is the "tier" field, which is the ranking of the player in the season. 

## Running the program

You'll need to create another file, `secrets.py`, which will contain your API key like so:
```
API_KEY = "<api key from https://developer.riotgames.com/ >"
```

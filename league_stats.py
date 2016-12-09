#
# Benjamin Siriprayook
# 8/12/16
# LEAGUE STATS
# 580121
# RGAPI-cbb79528-bec1-4266-bfdb-e9dd97ab5e93
# 

import requests, json

myAPI_Key = "RGAPI-cbb79528-bec1-4266-bfdb-e9dd97ab5e93"
region = "oce"

def getSummonerID(summonerName):
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + myAPI_Key
	response = requests.get(url)
	return response.json()

def getRecentGames(summonerID):
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.3/game/by-summoner/" + str(summonerID) + "/recent?api_key=" + myAPI_Key
	response = requests.get(url)
	return response.json()

#execution starts here
sumName = (str)(input("Enter OCE summoner name: "))
IDresponse = getSummonerID(sumName)
sumID = IDresponse[sumName]["id"]
print (sumID)
historyResponse = getRecentGames(sumID)
print (historyResponse)
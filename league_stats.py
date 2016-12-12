#
# Benjamin Siriprayook
# 8/12/16
# LEAGUE STATS
# 580121
# RGAPI-cbb79528-bec1-4266-bfdb-e9dd97ab5e93
# 

import requests, json, sys

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

def getMatch(gameID):
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + str(gameID) + "?includeTimeline=yes&api_key=" + myAPI_Key
	response = requests.get(url)
	return response.json()

def grabPlayerStats(game):
	playerLane = game["stats"]["playerPosition"]
	timePlayed = game["stats"]["timePlayed"]


def grabMatchStats(game, sumID):
	matchLength = game["matchDuration"]
	for player in game["participantIdentities"]:
		if player["player"]["summonerId"] == sumID:
			gameID = player["participantId"] # gets game player ID (between 1-10)
			break
	for participant in game["participants"]:
		if participant["participantId"] == gameID:
			teamID = participant["teamId"]
			# get participant stats
			kills = participant["stats"]["kills"]
			deaths = participant["stats"]["deaths"]
			assists = participant["stats"]["assists"]
			goldEarned = participant["stats"]["goldEarned"]
			champLV = participant["stats"]["champLevel"]
			firstBlood = participant["stats"]["firstBloodKill"]
			firstBloodAssist = participant["stats"]["firstBloodAssist"]
			firstTower = participant["stats"]["firstTowerKill"]
			firstTowerAssist = participant["stats"]["firstTowerAssist"]
			firstInhibitor = participant["stats"]["firstInhibitorKill"]
			firstInhibitorAssist = participant["stats"]["firstInhibitorAssist"]
			inhibitorKills = participant["stats"]["inhibitorKills"]
			towerKills = participant["stats"]["towerKills"]
			largestMultiKill = participant["stats"]["largestMultiKill"]
			largestKillingSpree = participant["stats"]["largestKillingSpree"]
			numDoubleKills = participant["stats"]["doubleKills"]
			numTripleKills = participant["stats"]["tripleKills"]
			numQuadraKills = participant["stats"]["quadraKills"]
			numPentaKills = participant["stats"]["pentaKills"]
			totalDmg = participant["stats"]["totalDamageDealt"]
			totalDmgtoChamps = participant["stats"]["totalDamageDealtToChampions"]
			totalDmgTaken = participant["stats"]["totalDamageTaken"]
			totalTimeCCDealt = participant["stats"]["totalTimeCrowdControlDealt"]
			MinionKills = participant["stats"]["minionsKilled"]
			NeutralMinionKills = participant["stats"]["neutralMinionsKilled"]
			NeutralTeamJungleKills = participant["stats"]["neutralMinionsKilledTeamJungle"]
			NeutralEnemyJungleKills = participant["stats"]["neutralMinionsKilledEnemyJungle"]
			wardsPlaced = participant["stats"]["wardsPlaced"]
			wardsKilled = participant["stats"]["wardsKilled"]
			visionWardsBought = participant["stats"]["visionWardsBoughtInGame"]
			winner = participant["stats"]["winner"]


#execution starts here
for sumName in sys.argv[1:]:
	print (sumName)
	IDresponse = getSummonerID(sumName)
	sumID = IDresponse[sumName]["id"]
	print (sumID)
	historyResponse = getRecentGames(sumID) # max 10 games in history
	for currGame in historyResponse["games"]:
		if currGame["gameType"] == "MATCHED_GAME" and currGame["gameMode"] == "CLASSIC":
			if currGame["subType"] == "NORMAL":
				print ("normal game")
			elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
				grabPlayerStats(currGame)
				gameID = currGame["gameId"]
				print (gameID)
				matchResponse = getMatch(gameID)
				grabMatchStats(matchResponse, sumID)
			else:
				continue
		else:
			continue


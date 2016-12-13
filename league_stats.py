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
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + str(gameID) + "?includeTimeline=True&api_key=" + myAPI_Key
	response = requests.get(url)
	return response.json()

def grabPlayerStats(game):
	playerLane = game["stats"]["playerPosition"]
	timePlayed = game["stats"]["timePlayed"]
	return timePlayed

def grabMatchStats(game, sumID, duration):
	matchLength = duration
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
			totalCS = participant["stats"]["minionsKilled"]
			NeutralMinionKills = participant["stats"]["neutralMinionsKilled"]
			teamJngCS = participant["stats"]["neutralMinionsKilledTeamJungle"]
			enemyJngCS = participant["stats"]["neutralMinionsKilledEnemyJungle"]
			wardsPlaced = participant["stats"]["wardsPlaced"]
			wardsKilled = participant["stats"]["wardsKilled"]
			visionWardsBought = participant["stats"]["visionWardsBoughtInGame"]
			winner = participant["stats"]["winner"]
			# participant timeline stats
			if participant["timeline"]["lane"] == "BOTTOM" or participant["timeline"]["lane"] == "JUNGLE":
				CSperMin10 = participant["timeline"]["creepsPerMinDeltas"]["zeroToTen"]
				CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["tenToTwenty"]
				xpPerMin10 = participant["timeline"]["xpPerMinDeltas"]["zeroToTen"]
				xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["tenToTwenty"]
				dmgTakenPerMin10 = participant["timeline"]["damageTakenPerMinDeltas"]["zeroToTen"]
				dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["tenToTwenty"]
				goldPerMin10 = participant["timeline"]["goldPerMinDeltas"]["zeroToTen"]
				goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["tenToTwenty"]
				if matchLength > 2400:
					CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["thirtyToEnd"]
					CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
					xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
					xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["thirtyToEnd"]
					dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
					dmgTakenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["thirtyToEnd"]
					goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
					goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["thirtyToEnd"]
				elif matchLength > 1800:
					CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
					xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
					dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
					goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
			else:				
				CSperMin10 = participant["timeline"]["creepsPerMinDeltas"]["zeroToTen"]
				CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["tenToTwenty"]
				CSdiffPerMin10 = participant["timeline"]["csDiffPerMinDeltas"]["zeroToTen"]
				CSdiffPerMin20 = participant["timeline"]["csDiffPerMinDeltas"]["tenToTwenty"]
				xpPerMin10 = participant["timeline"]["xpPerMinDeltas"]["zeroToTen"]
				xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["tenToTwenty"]
				xpDiffPerMin10 = participant["timeline"]["xpDiffPerMinDeltas"]["zeroToTen"]
				xpDiffPerMin20 = participant["timeline"]["xpDiffPerMinDeltas"]["tenToTwenty"]
				dmgTakenPerMin10 = participant["timeline"]["damageTakenPerMinDeltas"]["zeroToTen"]
				dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["tenToTwenty"]
				dmgDiffPerMin10 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["zeroToTen"]
				dmgDiffPerMin20 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["tenToTwenty"]
				goldPerMin10 = participant["timeline"]["goldPerMinDeltas"]["zeroToTen"]
				goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["tenToTwenty"]
				if matchLength > 2400:
					CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["thirtyToEnd"]
					CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
					CSdiffPerMin20 = participant["timeline"]["csDiffPerMinDeltas"]["twentyToThirty"]
					CSdiffPerMin30 = participant["timeline"]["csDiffPerMinDeltas"]["thirtyToEnd"]
					xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
					xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["thirtyToEnd"]
					xpDiffPerMin20 = participant["timeline"]["xpDiffPerMinDeltas"]["twentyToThirty"]
					xpDiffPerMin30 = participant["timeline"]["xpDiffPerMinDeltas"]["thirtyToEnd"]
					dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
					dmgTakenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["thirtyToEnd"]
					dmgDiffPerMin20 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["twentyToThirty"]
					dmgDiffPerMin30 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["thirtyToEnd"]
					goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
					goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["thirtyToEnd"]
				elif matchLength > 1800:
					CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
					CSdiffPerMin20 = participant["timeline"]["csDiffPerMinDeltas"]["twentyToThirty"]
					xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
					xpDiffPerMin20 = participant["timeline"]["xpDiffPerMinDeltas"]["twentyToThirty"]
					dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
					dmgDiffPerMin20 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["twentyToThirty"]
					goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
	numFrames = len(game["timeline"]["frames"])
	#for i in range(0, numFrames):
	#	timelineInfo[]

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
				gameID = currGame["gameId"]
				print (gameID)
			elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
				duration = grabPlayerStats(currGame)
				gameID = currGame["gameId"]
				print (gameID)
				matchResponse = getMatch(gameID)
				grabMatchStats(matchResponse, sumID, duration)
			else:
				continue
		else:
			continue


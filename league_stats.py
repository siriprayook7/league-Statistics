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
visionWard = 2055 # i.e control ward item id
roleTop = 1
roleMid = 2
roleJungle = 3
roleBot = 4

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
			totalJngCS = participant["stats"]["neutralMinionsKilled"]
			teamJngCS = participant["stats"]["neutralMinionsKilledTeamJungle"]
			enemyJngCS = participant["stats"]["neutralMinionsKilledEnemyJungle"]
			wardsPlaced = participant["stats"]["wardsPlaced"]
			wardsKilled = participant["stats"]["wardsKilled"]
			visionWardsBought = participant["stats"]["visionWardsBoughtInGame"]
			winner = participant["stats"]["winner"]
			# participant timeline stats
			if participant["timeline"]["lane"] == "BOTTOM" or participant["timeline"]["lane"] == "JUNGLE":
				botLaneRole = participant["timeline"]["role"]
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
			break

	# TEAM stats (stats not included in API)
	totalTeamKills = 0
	totalTeamDeaths = 0
	totalTeamAssists = 0
	totalTeamCS = 0
	totalTeamGold = 0
	totalTeamWardsPlaced = 0
	totalTeamWardsDestroyed = 0
	totalTeamVisionWards = 0
	totalTeamDmg = 0
	totalTeamDmgToChamps = 0
	totalTeamDmgTaken = 0
	firstDragTime = 0
	firstTowerTime = 0
	firstSightstoneTime = 0
	firstVisionWardTime = 0
	matchTotalDrags = 0
	matchTotalBarons = 0

	# TEAM Stats
	for side in game["teams"]:
		if side["teamId"] == teamID:
			numBarons = side["baronKills"]
			numDrags = side["dragonKills"]
			numHeralds = side["riftHeraldKills"]
			numTowers = side["towerKills"]
			numInhibs = side["inhibitorKills"]
			firstBlood = side["firstBlood"]
			firstBaron = side["firstBaron"]
			firstDrag = side["firstDragon"]
			firstTower = side["firstTower"]
			firstInhib = side["firstInhibitor"]
		else:
			enemyNumBarons = side["baronKills"]
			enemyNumDrags = side["dragonKills"]
			enemyNumHeralds = side["riftHeraldKills"]
			enemyNumTowers = side["towerKills"]
			enemyNumInhibs = side["inhibitorKills"]
	matchTotalDrags = numDrags + enemyNumDrags
	matchTotalBarons = numBarons + enemyNumBarons

	for person in game["participants"]:
		if person["teamId"] == teamID:
			totalTeamKills += person["stats"]["kills"]
			totalTeamDeaths += person["stats"]["deaths"]
			totalTeamAssists += person["stats"]["assists"]
			totalTeamCS += person["stats"]["minionsKilled"]
			totalTeamGold += person["stats"]["goldEarned"]
			totalTeamWardsPlaced += person["stats"]["wardsPlaced"]
			totalTeamWardsDestroyed += person["stats"]["wardsKilled"]
			totalTeamVisionWards += person["stats"]["visionWardsBoughtInGame"]
			totalTeamDmg += person["stats"]["totalDamageDealt"]
			totalTeamDmgToChamps += person["stats"]["totalDamageDealtToChampions"]
			totalTeamDmgTaken += person["stats"]["totalDamageTaken"]

	# PLAYER timeline Stats (per minute frames)
	# extract time related stats here e.g. first drag time, first tower time
	timeline_gold = []
	timeline_cs = []
	timeline_jngCS = []
	timeline_xp = []
	for interval in game["timeline"]["frames"][1:]: # skips initial frame
		timeline_gold.append(interval["participantFrames"][str(gameID)]["totalGold"])
		timeline_cs.append(interval["participantFrames"][str(gameID)]["minionsKilled"])
		timeline_jngCS.append(interval["participantFrames"][str(gameID)]["jungleMinionsKilled"])
		timeline_xp.append(interval["participantFrames"][str(gameID)]["xp"])
		if numDrags != 0 and firstDragTime == 0: 
			for event in interval["events"]:
				if event["eventType"] == "ELITE_MONSTER_KILL":
					if event["monsterType"] == "DRAGON":
						if game["participants"][(event["killerId"]-1)]["teamId"] == teamID:
							firstDragTime = event["timestamp"] # in milliseconds
							break
		elif numTowers != 0 and firstTowerTime == 0:
			for x in interval["events"]:
				if x["eventType"] == "BUILDING_KILL":
					if x["teamId"] != teamID: # if its not your own tower being destroyed
						firstTowerTime = x["timestamp"] # in milliseconds
						break
		elif visionWardsBought != 0 and firstVisionWardTime == 0:
			for y in interval["events"]:
				if y["eventType"] == "ITEM_PURCHASED":
					if y["participantId"] == gameID and y["itemId"] == visionWard:
						firstVisionWardTime = y["timestamp"] # in milliseconds
						break
#execution starts here
for sumName in sys.argv[1:]:
	print (sumName)
	IDresponse = getSummonerID(sumName)
	sumID = IDresponse[sumName]["id"]
	historyResponse = getRecentGames(sumID) # max 10 games in history
	for currGame in historyResponse["games"]:
		if currGame["gameType"] == "MATCHED_GAME" and currGame["gameMode"] == "CLASSIC":
			if currGame["subType"] == "NORMAL":
				print ("normal game")
				gameID = currGame["gameId"]
			elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
				duration = grabPlayerStats(currGame)
				gameID = currGame["gameId"]
				print (gameID)
				matchResponse = getMatch(gameID)
				grabMatchStats(matchResponse, sumID, duration)
			else:
				continue
		else:
			print ("other GameMode")
			continue


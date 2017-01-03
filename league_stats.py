#
# Benjamin Siriprayook
# 8/12/16
# LEAGUE STATS
# 580121
# client ID: 696143935174-8090lf614qrfuknegrj8j5khit32s9dq.apps.googleusercontent.com
# client Secret: HNyRfEPupPSGNVbEOjK_YlPt  

import requests, json, sys, gspread
from oauth2client.service_account import ServiceAccountCredentials

myAPI_Key = "RGAPI-cbb79528-bec1-4266-bfdb-e9dd97ab5e93"
region = "oce"
visionWard = 2055 # i.e control ward item id
Sightstone = 2049 # item id
roleTop = 1
roleMid = 2
roleJungle = 3
roleBot = 4
roleSupport = 5

# league id
imawizardm8 = "554402"
imBS = "580121"
Rhetorikal = "287733"
JARVIS = "555214"
manbones2 = "566065"
Teesang = "327213"
jawsmoney = "509083"
kugeku = "564390"
Dugtrio = "570809"
SmoothCactus = "5500803"
Piangle = "564395"
leagueIDs = [imawizardm8, imBS, Rhetorikal, JARVIS, manbones2, Teesang, jawsmoney, kugeku, Dugtrio, SmoothCactus, Piangle]

def getSummonerID(summonerName):
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + myAPI_Key
	response = requests.get(url)
	return response.json()

def getChampionName(champID):
	url = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + str(champID) + "?api_key=" + myAPI_Key
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
	if playerLane == roleBot:
		role = game["stats"]["playerRole"]
		if role == 2:
			playerLane = roleSupport
	# timePlayed = game["stats"]["timePlayed"]
	return playerLane

def grabMatchStats(game, sumID, lane, sheet, gameResponse):
	matchLength = game["matchDuration"]
	for player in game["participantIdentities"]:
		if player["player"]["summonerId"] == sumID:
			gameID = player["participantId"] # gets game player ID (between 1-10)
			break
	for participant in game["participants"]:
		if participant["participantId"] == gameID:
			teamID = participant["teamId"]
			championID = participant["championId"]
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
			totalMinionCS = participant["stats"]["minionsKilled"]
			totalJngCS = participant["stats"]["neutralMinionsKilled"]
			teamJngCS = participant["stats"]["neutralMinionsKilledTeamJungle"]
			enemyJngCS = participant["stats"]["neutralMinionsKilledEnemyJungle"]
			wardsPlaced = participant["stats"]["wardsPlaced"]
			wardsKilled = participant["stats"]["wardsKilled"]
			visionWardsBought = participant["stats"]["visionWardsBoughtInGame"]
			winner = participant["stats"]["winner"]
			# participant timeline stats
			# if participant["timeline"]["lane"] == "BOTTOM" or participant["timeline"]["lane"] == "JUNGLE":
			# 	botLaneRole = participant["timeline"]["role"]
			# 	CSperMin10 = participant["timeline"]["creepsPerMinDeltas"]["zeroToTen"]
			# 	CSperMin20 = participant["timeline"]["creepsPerMinDeltas"]["tenToTwenty"]
			# 	xpPerMin10 = participant["timeline"]["xpPerMinDeltas"]["zeroToTen"]
			# 	xpPerMin20 = participant["timeline"]["xpPerMinDeltas"]["tenToTwenty"]
			# 	dmgTakenPerMin10 = participant["timeline"]["damageTakenPerMinDeltas"]["zeroToTen"]
			# 	dmgTakenPerMin20 = participant["timeline"]["damageTakenPerMinDeltas"]["tenToTwenty"]
			# 	goldPerMin10 = participant["timeline"]["goldPerMinDeltas"]["zeroToTen"]
			# 	goldPerMin20 = participant["timeline"]["goldPerMinDeltas"]["tenToTwenty"]
			# 	if matchLength > 2400:
			# 		CSperMin40 = participant["timeline"]["creepsPerMinDeltas"]["thirtyToEnd"]
			# 		CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
			# 		xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
			# 		xpPerMin40 = participant["timeline"]["xpPerMinDeltas"]["thirtyToEnd"]
			# 		dmgTakenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
			# 		dmgTakenPerMin40 = participant["timeline"]["damageTakenPerMinDeltas"]["thirtyToEnd"]
			# 		goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
			# 		goldPerMin40 = participant["timeline"]["goldPerMinDeltas"]["thirtyToEnd"]
			# 	elif matchLength > 1800:
			# 		CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
			# 		xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
			# 		dmgTakenPerMin40kenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
			# 		goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
			# else:				
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
				CSperMin40 = participant["timeline"]["creepsPerMinDeltas"]["thirtyToEnd"]
				CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
				CSdiffPerMin30 = participant["timeline"]["csDiffPerMinDeltas"]["twentyToThirty"]
				CSdiffPerMin40 = participant["timeline"]["csDiffPerMinDeltas"]["thirtyToEnd"]
				xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
				xpPerMin40 = participant["timeline"]["xpPerMinDeltas"]["thirtyToEnd"]
				xpDiffPerMin30 = participant["timeline"]["xpDiffPerMinDeltas"]["twentyToThirty"]
				xpDiffPerMin40 = participant["timeline"]["xpDiffPerMinDeltas"]["thirtyToEnd"]
				dmgTakenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
				dmgTakenPerMin40 = participant["timeline"]["damageTakenPerMinDeltas"]["thirtyToEnd"]
				dmgDiffPerMin30 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["twentyToThirty"]
				dmgDiffPerMin40 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["thirtyToEnd"]
				goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
				goldPerMin40 = participant["timeline"]["goldPerMinDeltas"]["thirtyToEnd"]
			elif matchLength > 1800:
				CSperMin30 = participant["timeline"]["creepsPerMinDeltas"]["twentyToThirty"]
				CSdiffPerMin30 = participant["timeline"]["csDiffPerMinDeltas"]["twentyToThirty"]
				xpPerMin30 = participant["timeline"]["xpPerMinDeltas"]["twentyToThirty"]
				xpDiffPerMin30 = participant["timeline"]["xpDiffPerMinDeltas"]["twentyToThirty"]
				dmgTakenPerMin30 = participant["timeline"]["damageTakenPerMinDeltas"]["twentyToThirty"]
				dmgDiffPerMin30 = participant["timeline"]["damageTakenDiffPerMinDeltas"]["twentyToThirty"]
				goldPerMin30 = participant["timeline"]["goldPerMinDeltas"]["twentyToThirty"]
				CSperMin40 = 0
				CSdiffPerMin40 = 0
				xpPerMin40 = 0
				xpDiffPerMin40 = 0
				dmgTakenPerMin40 = 0
				dmgDiffPerMin40 = 0
				goldPerMin40 = 0
			else:
				CSperMin40 = 0
				CSperMin30 = 0
				CSdiffPerMin30 = 0
				CSdiffPerMin40 = 0
				xpPerMin30 = 0
				xpPerMin40 = 0
				xpDiffPerMin30 = 0
				xpDiffPerMin40 = 0
				dmgTakenPerMin30 = 0
				dmgTakenPerMin40 = 0
				dmgDiffPerMin30 = 0
				dmgDiffPerMin40 = 0
				goldPerMin30 = 0
				goldPerMin40 = 0
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
	totalTeamTimeCCDealt = 0
	firstDeath = 0
	firstDragTime = 0
	firstTowerTime = 0
	laneTowerTime = 0
	rift_HeraldTime = 0
	firstSightstoneTime = 0
	firstVisionWardTime = 0
	numTowerAssists = 0
	numInhibAssists = 0
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
			totalTeamCS += person["stats"]["neutralMinionsKilled"]
			totalTeamGold += person["stats"]["goldEarned"]
			totalTeamWardsPlaced += person["stats"]["wardsPlaced"]
			totalTeamWardsDestroyed += person["stats"]["wardsKilled"]
			totalTeamVisionWards += person["stats"]["visionWardsBoughtInGame"]
			totalTeamDmg += person["stats"]["totalDamageDealt"]
			totalTeamDmgToChamps += person["stats"]["totalDamageDealtToChampions"]
			totalTeamDmgTaken += person["stats"]["totalDamageTaken"]
			totalTeamTimeCCDealt += person["stats"]["totalTimeCrowdControlDealt"]

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

		if numTowers != 0 and firstTowerTime == 0:
			for x in interval["events"]:
				if x["eventType"] == "BUILDING_KILL":
					if x["teamId"] != teamID: # if its not your own tower being destroyed
						firstTowerTime = x["timestamp"] # in milliseconds

		if lane == roleTop:
			if numTowers != 0 and laneTowerTime == 0:
				for w in interval["events"]:
					if w["eventType"] == "BUILDING_KILL":
						if w["laneType"] == "TOP_LANE" and w["towerType"] == "OUTER_TURRET":
							laneTowerTime = w["timestamp"]

		elif lane == roleMid:
			if numTowers != 0 and laneTowerTime == 0:
				for w in interval["events"]:
					if w["eventType"] == "BUILDING_KILL":
						if w["laneType"] == "MID_LANE" and w["towerType"] == "OUTER_TURRET":
							laneTowerTime = w["timestamp"]

		elif lane == roleBot or lane == roleSupport:
			if numTowers != 0 and laneTowerTime == 0:
				for w in interval["events"]:
					if w["eventType"] == "BUILDING_KILL":
						if w["laneType"] == "BOT_LANE" and w["towerType"] == "OUTER_TURRET":
							laneTowerTime = w["timestamp"]

		if numHeralds != 0 and rift_HeraldTime == 0:
			for y in interval["events"]:
				if y["eventType"] == "ELITE_MONSTER_KILL":
					if y["monsterType"] == "RIFTHERALD":
						rift_HeraldTime = y["timestamp"] # in milliseconds

		if visionWardsBought != 0 and firstVisionWardTime == 0:
			for z in interval["events"]:
				if z["eventType"] == "ITEM_PURCHASED":
					if z["participantId"] == gameID and z["itemId"] == visionWard:
						firstVisionWardTime = z["timestamp"] # in milliseconds

		if lane == roleSupport and firstSightstoneTime == 0:
			for v in interval["events"]:
				if v["eventType"] == "ITEM_PURCHASED":
					if v["participantId"] == gameID and v["itemId"] == Sightstone:
						firstSightstoneTime = v["timestamp"] # in milliseconds

		if firstBlood == "false" and firstDeath == 0:
			for u in interval["events"]:
				if u["eventType"] == "CHAMPION_KILL":
					if u["victimId"] == gameID:
						firstDeath = False
					else:
						firstDeath = True

		if numTowers != 0:
			for t in interval["events"]:
				if t["eventType"] == "BUILDING_KILL":
					if t["buildingType"] == "TOWER_BUILDING" and t["teamId"] != teamID:
						if "assistingParticipantIds" in t:
							if gameID in t["assistingParticipantIds"]:
								numTowerAssists += 1

		if numInhibs != 0:
			for s in interval["events"]:
				if s["eventType"] == "BUILDING_KILL":
					if s["buildingType"] == "INHIBITOR_BUILDING" and s["teamId"] != teamID:
						if "assistingParticipantIds" in s:
							if gameID in s["assistingParticipantIds"]:
								numInhibAssists += 1


	# check if you played with anyone from gga
	playedWith = []
	for noob in leagueIDs:
		if noob == sumID:
			continue
		else:
			for playerDto in gameResponse["fellowPlayers"]:
				if noob == str(playerDto["summonerId"]) and playerDto["teamId"] == teamID:
					playedWith.append(noob)

	# get champ name
	championResponse = getChampionName(championID)
	champName = championResponse["name"]

	# send data to sheets
	updateSheet(sheet,str(sumID),teamID,lane,matchLength,kills,deaths,assists,
		goldEarned,champLV,firstBlood,firstBloodAssist,firstDeath,firstTower,firstTowerAssist,
		firstInhibitor,firstInhibitorAssist,towerKills,inhibitorKills,numTowerAssists,numInhibAssists,
		largestMultiKill,largestKillingSpree,numDoubleKills,numTripleKills,numQuadraKills,numPentaKills,
		totalDmg,totalDmgtoChamps,totalDmgTaken,totalTimeCCDealt,totalMinionCS,
		totalJngCS,teamJngCS,enemyJngCS,wardsPlaced,wardsKilled,visionWardsBought,winner,
		CSperMin10,CSperMin20,CSperMin30,CSperMin40,CSdiffPerMin10,CSdiffPerMin20,
		CSdiffPerMin30,CSdiffPerMin40,xpPerMin10,xpPerMin20,xpPerMin30,xpPerMin40,
		xpDiffPerMin10,xpDiffPerMin20,xpDiffPerMin30,xpDiffPerMin40,dmgTakenPerMin10,
		dmgTakenPerMin20,dmgTakenPerMin30,dmgTakenPerMin40,dmgDiffPerMin10,dmgDiffPerMin20,
		dmgDiffPerMin30,dmgDiffPerMin40,goldPerMin10,goldPerMin20,goldPerMin30,
		goldPerMin40,totalTeamKills,totalTeamDeaths,totalTeamAssists,totalTeamCS,
		totalTeamGold,totalTeamWardsPlaced,totalTeamWardsDestroyed,totalTeamVisionWards,
		totalTeamDmg,totalTeamDmgToChamps,totalTeamDmgTaken,totalTeamTimeCCDealt,
		firstDragTime,firstTowerTime,laneTowerTime,firstVisionWardTime,firstSightstoneTime,
		numDrags,numBarons,numHeralds,firstDrag,matchTotalDrags,rift_HeraldTime,
		numTowers,numInhibs,timeline_gold,timeline_cs,timeline_jngCS,timeline_xp,
		playedWith,champName)

def accessRankedExcelDoc():
	scope = ["https://spreadsheets.google.com/feeds"]
	credentials = ServiceAccountCredentials.from_json_keyfile_name("leagueSTATS-69cc883763dc.json", scope)
	gd = gspread.authorize(credentials)
	# updateExcel(gd)
	return gd

def accessNormalsExcelDoc():
	scope = ["https://spreadsheets.google.com/feeds"]

def checkHistory(gd,playerID,matchID):
	spreadSheet = gd.open("League Statistics")
	general = spreadSheet.worksheet("Overview")

	playerCell = general.find(playerID)
	playerHistory = general.row_values(playerCell.row)
	if matchID in playerHistory[1:]:
		return False
	else:
		return True

def updateHistory(gd,playerID,newGameID):
	spreadSheet = gd.open("League Statistics")
	general = spreadSheet.worksheet("Overview")

	playerCell = general.find(playerID)
	playerHistory = general.row_values(playerCell.row)
	nextFreeColumn = playerHistory.index('') + 1
	
	nextCell = general.cell(playerCell.row,nextFreeColumn)
	nextCell.value = newGameID
	general.update_cell(nextCell.row,nextCell.col,nextCell.value)

def updateExcel(gd):
	spreadSheet = gd.open("League Statistics")
	general = spreadSheet.worksheet("TOP")

	playerColumn = 6

	CS_list = general.findall("Total CS per min")
	CSDiff_list = general.findall("Total CS Diff per min")
	XP_list = general.findall("Total XP per min")
	XPdiff_list = general.findall("Total XP Diff per min")
	DmgTaken_list = general.findall("Total Damage Taken per min")
	DmgTakenDiff_list = general.findall("Total Damage Taken Diff per min")

	csPM_list = [23.4,-23.6,-10.3444,10.323]
	csDiffPM_list = [23.4,-23.6,-10.3444,10.323]
	xpPM_list = [23.4,-23.6,-10.3444,10.323]
	xpDiffPM_list = [23.4,-23.6,-10.3444,10.323]
	dmgTakenPM_list = [23.4,-23.6,-10.3444,10.323]
	dmgDiffPM_list = [23.4,-23.6,-10.3444,10.323]
	for i in range(0,4):
		CS_cell = general.cell(CS_list[i].row,playerColumn)
		CSDiff_cell = general.cell(CSDiff_list[i].row,playerColumn)
		XP_cell = general.cell(XP_list[i].row,playerColumn)
		XPdiff_cell = general.cell(XPdiff_list[i].row,playerColumn)
		DmgTaken_cell = general.cell(DmgTaken_list[i].row,playerColumn)
		DmgTakenDiff_cell = general.cell(DmgTakenDiff_list[i].row,playerColumn)
		
		CS_cell.value = float(CS_cell.value) + csPM_list[i]
		CSDiff_cell.value = float(CSDiff_cell.value) + csDiffPM_list[i]
		XP_cell.value = float(XP_cell.value) + xpPM_list[i]
		XPdiff_cell.value = float(XPdiff_cell.value) + xpDiffPM_list[i]
		DmgTaken_cell.value = float(DmgTaken_cell.value) + dmgTakenPM_list[i]
		DmgTakenDiff_cell.value = float(DmgTakenDiff_cell.value) + dmgDiffPM_list[i]

		update_cells = [CS_cell,CSDiff_cell,XP_cell,XPdiff_cell,DmgTaken_cell,DmgTakenDiff_cell]
		general.update_cells(update_cells)

	
	# currCell = general.cell(cell_list[0].row,2)
	# currCell.value = int(currCell.value) + 1					# total Tower Assists
	# cellsToUpdate.append(currCell)

	# val = general.acell("A2")
	# sName = general.acell("A1")
	# print (sName.value + ": " + str(val.value))
	# val.value = int(val.value) + 4
	# general.update_acell("A2",val.value)
	# print ("new val = " + str(val.value))
	# lane = spreadSheet.worksheet("TOP")
	# val = lane.acell("A1")
	# print ("top val = " + str(val.value))

def updateSheet(gd,sumID,tID,role,matchDuration,kills,deaths,assists,gold,champLV, 
	FB,FBa,FD,fTower,fTowerA,fInhib,fInhibA,numTower,NumInhib,numTowerA,numInhibA,
	largestMK,largestKS,numDoubles,numTriple,numQuadra,numPenta,
	totalDmg,totalDmgTC,totalDmgT,totalCC,totalMinions,totalJngCS,
	totalTeamJngCS,totalEnemyJngCS,wards,wardKills,visionWards,win,
	csPM10,csPM20,csPM30,csPM40,csDiff10,csDiff20,csDiff30,csDiff40,
	xpPM10,xpPM20,xpPM30,xpPM40,xpDiff10,xpDiff20,xpDiff30,xpDiff40,
	dmgT10,dmgT20,dmgT30,dmgT40,dmgTDiff10,dmgTDiff20,dmgTDiff30,dmgTDiff40,
	gold10,gold20,gold30,gold40,
	totalTKills,totalTDeaths,totalTAssists,totalTCS,totalTGold,
	totalTWards,totalTWardKills,totalTVisionWards,totalTDmg,
	totalTDmgTC,totalTDmgT,totalTCC,
	firstDragTime,firstTowerTime,laneTowerTime,firstVisionWardTime,firstSSTime,
	numTDrags,numTBarons,numHerald,firstDrag,totalDrags,heraldTime,
	numTTower,numTInhibs,TLgold,TLcs,TLjngCS,TLxp,playedWith,champName):
	spreadSheet = gd.open("League Statistics")
	if role == roleTop:
		general = spreadSheet.worksheet("TOP")
	elif role == roleMid:
		general = spreadSheet.worksheet("MID")
	elif role == roleJungle:
		general = spreadSheet.worksheet("JUNGLE")
	elif role == roleBot:
		general = spreadSheet.worksheet("ADC")
	else:
		general = spreadSheet.worksheet("SUPPORT")

	if sumID == imawizardm8:
		playerColumn = 2 # i.e. Column B
	elif sumID == imBS:
		playerColumn = 3
	elif sumID == Rhetorikal:
		playerColumn = 4
	elif sumID == JARVIS:
		playerColumn = 5
	elif sumID == manbones2:
		playerColumn = 6
	elif sumID == Teesang:
		playerColumn = 7
	elif sumID == jawsmoney:
		playerColumn = 8
	elif sumID == kugeku:
		playerColumn = 9
	elif sumID == Dugtrio:
		playerColumn = 10
	elif sumID == SmoothCactus:
		playerColumn = 11
	elif sumID == Piangle:
		playerColumn = 12

	### Player Total Statistics ###

	cellsToUpdate = []

	totalGamesPlayed = general.find("Total Games Played")
	currCell = general.cell(totalGamesPlayed.row,playerColumn)
	currCell.value = int(currCell.value) + 1							# total Games Played
	cellsToUpdate.append(currCell)

	if win:
		print("win")
		totalWins = general.find("Total Wins")
		currCell = general.cell(totalWins.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total Wins
		cellsToUpdate.append(currCell)
	else:
		totalLosses = general.find("Total Losses")
		currCell = general.cell(totalLosses.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total Losses
		cellsToUpdate.append(currCell)

	totalKills = general.find("Total Kills")
	currCell = general.cell(totalKills.row,playerColumn)
	currCell.value = int(currCell.value) + kills						# total Kills
	cellsToUpdate.append(currCell)

	totalDeaths = general.find("Total Deaths")
	currCell = general.cell(totalDeaths.row,playerColumn)
	currCell.value = int(currCell.value) + deaths						# total Deahts
	cellsToUpdate.append(currCell)

	totalAssists = general.find("Total Assists")
	currCell = general.cell(totalAssists.row,playerColumn)
	currCell.value = int(currCell.value) + assists						# total Assists
	cellsToUpdate.append(currCell)

	totalGoldEarned = general.find("Total Gold Earned")
	currCell = general.cell(totalGoldEarned.row,playerColumn)
	currCell.value = int(currCell.value) + gold							# total Gold Earned
	cellsToUpdate.append(currCell)

	totalTowerKills = general.find("Total Tower Kills")
	currCell = general.cell(totalTowerKills.row,playerColumn)
	currCell.value = int(currCell.value) + numTower						# total Tower Kills
	cellsToUpdate.append(currCell)

	totalInhibitorKills = general.find("Total Inhibitor Kills")
	currCell = general.cell(totalInhibitorKills.row,playerColumn)
	currCell.value = int(currCell.value) + NumInhib						# total Inhibitor Kills
	cellsToUpdate.append(currCell)

	totalDoubleKills = general.find("Total Double Kills")
	currCell = general.cell(totalDoubleKills.row,playerColumn)
	currCell.value = int(currCell.value) + numDoubles					# total Double Kills
	cellsToUpdate.append(currCell)

	totalTripleKills = general.find("Total Triple Kills")
	currCell = general.cell(totalTripleKills.row,playerColumn)
	currCell.value = int(currCell.value) + numTriple					# total Triple Kills
	cellsToUpdate.append(currCell)

	totalQuadraKills = general.find("Total Quadra Kills")
	currCell = general.cell(totalQuadraKills.row,playerColumn)
	currCell.value = int(currCell.value) + numQuadra					# total Quadra Kills
	cellsToUpdate.append(currCell)

	totalPentaKills = general.find("Total Penta Kills")
	currCell = general.cell(totalPentaKills.row,playerColumn)
	currCell.value = int(currCell.value) + numPenta						# total Penta Kills
	cellsToUpdate.append(currCell)

	totalWardsPlaced = general.find("Total Wards Placed")
	currCell = general.cell(totalWardsPlaced.row,playerColumn)
	currCell.value = int(currCell.value) + wards						# total wards placed
	cellsToUpdate.append(currCell)

	totalWardsKilled = general.find("Total Wards Killed")
	currCell = general.cell(totalWardsKilled.row,playerColumn)
	currCell.value = int(currCell.value) + wardKills					# total ward Kills
	cellsToUpdate.append(currCell)

	totalVisionWards = general.find("Total Vision Wards Bought")
	currCell = general.cell(totalVisionWards.row,playerColumn)
	currCell.value = int(currCell.value) + visionWards					# total vision wards bought
	cellsToUpdate.append(currCell)

	# totalCS = general.find("Total CS")
	# currCell = general.cell(totalCS.row,playerColumn)
	# currCell.value = int(currCell.value) + 							
	# cellsToUpdate.append(currCell)

	totalMinionCS = general.find("Total Minion CS")
	currCell = general.cell(totalMinionCS.row,playerColumn)
	currCell.value = int(currCell.value) + totalMinions					# total Minion CS
	cellsToUpdate.append(currCell)

	totalJungleCS = general.find("Total Jungle CS")
	currCell = general.cell(totalJungleCS.row,playerColumn)
	currCell.value = int(currCell.value) + totalJngCS					# total Jungle CS
	cellsToUpdate.append(currCell)

	totalTeamJungleCS = general.find("Total Team Jungle CS")
	currCell = general.cell(totalTeamJungleCS.row,playerColumn)
	currCell.value = int(currCell.value) + totalTeamJngCS				# total Team Jungle CS
	cellsToUpdate.append(currCell)

	totalEnemyJungleCS = general.find("Total Enemy Jungle CS")
	currCell = general.cell(totalEnemyJungleCS.row,playerColumn)
	currCell.value = int(currCell.value) + totalEnemyJngCS				# total Enemy Jungle CS
	cellsToUpdate.append(currCell)

	totalDmgDealt = general.find("Total Dmg Dealt")
	currCell = general.cell(totalDmgDealt.row,playerColumn)
	currCell.value = int(currCell.value) + totalDmg						# total Damage Dealt
	cellsToUpdate.append(currCell)

	totalDmgToChamps = general.find("Total Dmg To Champs")
	currCell = general.cell(totalDmgToChamps.row,playerColumn)
	currCell.value = int(currCell.value) + totalDmgTC					# total Damage To Champs
	cellsToUpdate.append(currCell)

	totalDmgTaken = general.find("Total Dmg Taken")
	currCell = general.cell(totalDmgTaken.row,playerColumn)
	currCell.value = int(currCell.value) + totalDmgT					# total Damage Taken
	cellsToUpdate.append(currCell)

	totalTimeCCDealt = general.find("Total Time CC Dealt")
	currCell = general.cell(totalTimeCCDealt.row,playerColumn)
	currCell.value = int(currCell.value) + totalCC						# total Time Crowd Crontrol Dealt
	cellsToUpdate.append(currCell)

	if FB:
		totalFirstBloods = general.find("Total First Bloods")
		currCell = general.cell(totalFirstBloods.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total First Bloods
		cellsToUpdate.append(currCell)

	if FBa:
		totalFBassists = general.find("Total First Blood Assists")
		currCell = general.cell(totalFBassists.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total First Blood Assists
		cellsToUpdate.append(currCell)

	if FD:
		totalFirstDeaths = general.find("Total First Deaths")
		currCell = general.cell(totalFirstDeaths.row,playerColumn)
		currCell.value = int(currCell.value) + 1							# total First Deaths
		cellsToUpdate.append(currCell)

	if fTower:
		totalFirstTowerKills = general.find("Total First Tower Kills")
		currCell = general.cell(totalFirstTowerKills.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total first Tower Kills
		cellsToUpdate.append(currCell)

	if fTowerA:
		totalFTassists = general.find("Total First Tower Assists")
		currCell = general.cell(totalFTassists.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total first Tower Assists
		cellsToUpdate.append(currCell)

	if fInhib:
		totalFirstInhibKills = general.find("Total First Inhibitor Kills")
		currCell = general.cell(totalFirstInhibKills.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total first Inhibitor Kills
		cellsToUpdate.append(currCell)

	if fInhibA:
		totalFIassist = general.find("Total First Inhibitor Assists")
		currCell = general.cell(totalFIassist.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total first Inhibitor assists
		cellsToUpdate.append(currCell)

	if tID == 100:
		totalBlueSide = general.find("Total Blue Side Games")
		currCell = general.cell(totalBlueSide.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total Blue Side Games
		cellsToUpdate.append(currCell)
		if win:
			totalBlueWins = general.find("Total Blue Side Wins")
			currCell = general.cell(totalBlueWins.row,playerColumn)
			currCell.value = int(currCell.value) + 1					# total Blue Side Wins
			cellsToUpdate.append(currCell)
	else:
		totalRedSide = general.find("Total Red Side Games")
		currCell = general.cell(totalRedSide.row,playerColumn)
		currCell.value = int(currCell.value) + 1						# total Red Side Games
		cellsToUpdate.append(currCell)	
		if win:
			totalRedWins = general.find("Total Red Side Wins")
			currCell = general.cell(totalRedWins.row,playerColumn)
			currCell.value = int(currCell.value) + 1					# total Red Side Wins
			cellsToUpdate.append(currCell)

	if role == roleJungle:
		if firstDrag:
			totalFirstDrags = general.find("Total First Dragons")
			currCell = general.cell(totalFirstDrags.row,playerColumn)
			currCell.value = int(currCell.value) + 1					# total First Dragons
			cellsToUpdate.append(currCell)

		totalDrags = general.find("Total Dragons")
		currCell = general.cell(totalDrags.row,playerColumn)
		currCell.value = int(currCell.value) + numTDrags				# total Dragon Kills
		cellsToUpdate.append(currCell)

		totalHeralds = general.find("Total Rift Heralds")
		currCell = general.cell(totalHeralds.row,playerColumn)
		currCell.value = int(currCell.value) + numHerald				# total Rift Herald Kills
		cellsToUpdate.append(currCell)

	### Team Totals for participation averages calculations ###
	totalTeamKills = general.find("Total Team Kills")
	currCell = general.cell(totalTeamKills.row,playerColumn)
	currCell.value = int(currCell.value) + totalTKills					# total Team Kills
	cellsToUpdate.append(currCell)

	totalTeamDeaths = general.find("Total Team Deaths")
	currCell = general.cell(totalTeamDeaths.row,playerColumn)
	currCell.value = int(currCell.value) + totalTDeaths					# total Team Deaths
	cellsToUpdate.append(currCell)

	totalTeamAssists = general.find("Total Team Assists")
	currCell = general.cell(totalTeamAssists.row,playerColumn)
	currCell.value = int(currCell.value) + totalTAssists				# total Team Assists
	cellsToUpdate.append(currCell)

	totalTeamGold = general.find("Total Team Gold")
	currCell = general.cell(totalTeamGold.row,playerColumn)
	currCell.value = int(currCell.value) + totalTGold					# total Team Gold
	cellsToUpdate.append(currCell)

	totalTeamDmg = general.find("Total Team Dmg")
	currCell = general.cell(totalTeamDmg.row,playerColumn)
	currCell.value = int(currCell.value) + totalTDmg					# total Team Damage
	cellsToUpdate.append(currCell)

	totalTeamDmgToChamps = general.find("Total Team Dmg to Champs")
	currCell = general.cell(totalTeamDmgToChamps.row,playerColumn)
	currCell.value = int(currCell.value) + totalTDmgTC					# total Team Damage To Champs
	cellsToUpdate.append(currCell)

	totalTeamDmgTaken = general.find("Total Team Dmg Taken")
	currCell = general.cell(totalTeamDmgTaken.row,playerColumn)
	currCell.value = int(currCell.value) + totalTDmgT					# total Team Damage Taken
	cellsToUpdate.append(currCell)

	totalTeamCCTimeDealt = general.find("Total Team CC Time dealt (secs)")
	currCell = general.cell(totalTeamCCTimeDealt.row,playerColumn)
	currCell.value = int(currCell.value) + totalTCC						# total team CC time dealt
	cellsToUpdate.append(currCell)

	totalTeamWardsPlaced = general.find("Total Team Wards Placed")
	currCell = general.cell(totalTeamWardsPlaced.row,playerColumn)
	currCell.value = int(currCell.value) + totalTWards					# total Team Wards Placed
	cellsToUpdate.append(currCell)

	totalTeamWardsKilled = general.find("Total Team Wards Killed")
	currCell = general.cell(totalTeamWardsKilled.row,playerColumn)
	currCell.value = int(currCell.value) + totalTWardKills				# total Team Ward Kills
	cellsToUpdate.append(currCell)

	totalTeamVisionWards = general.find("Total Team Vision Wards Bought")
	currCell = general.cell(totalTeamVisionWards.row,playerColumn)
	currCell.value = int(currCell.value) + totalTVisionWards			# total Team Vision Wards Bought
	cellsToUpdate.append(currCell)

	totalTeamCS = general.find("Total Team CS")
	currCell = general.cell(totalTeamCS.row,playerColumn)
	currCell.value = int(currCell.value) + totalTCS						# total Team CS 
	cellsToUpdate.append(currCell)

	totalTeamTowers = general.find("Total Team Towers Killed")
	currCell = general.cell(totalTeamTowers.row,playerColumn)
	currCell.value = int(currCell.value) + numTTower					# total Team Towers
	cellsToUpdate.append(currCell)

	totalTeamInhibs = general.find("Total Team Inhibitors Killed")
	currCell = general.cell(totalTeamInhibs.row,playerColumn)
	currCell.value = int(currCell.value) + numTInhibs					# total Team Inhibitors
	cellsToUpdate.append(currCell)

	totalTimeFirstVW = general.find("Total Time for First Vision Ward Buy (ms)")
	if firstVisionWardTime == 0:
		avgTimeFirstVW = general.find("Avg. Time First Vision Ward Bought (mins)")
		averageTimeCell = general.cell(avgTimeFirstVW.row,playerColumn)
		firstVisionWardTime = averageTimeCell.value
	currCell = general.cell(totalTimeFirstVW.row,playerColumn)
	currCell.value = int(currCell.value) + firstVisionWardTime			# total Time for First Vision Ward
	cellsToUpdate.append(currCell)

	if role == roleSupport:
		totalTimeFirstSS = general.find("Total Time for SightStone Buy (ms)")
		currCell = general.cell(totalTimeFirstSS.row,playerColumn)
		currCell.value = int(currCell.value) + firstSSTime 				# total Time for First SightStone
		cellsToUpdate.append(currCell)

	if firstTowerTime == 0:
		avgTimeFirstT = general.find("Avg. Time First Tower Killed")
		averageTimeCell = general.cell(avgTimeFirstT.row,playerColumn)
		firstTowerTime = averageTimeCell.value
	totalTimeFirstTower = general.find("Total Time for First Tower Kill (ms)")
	currCell = general.cell(totalTimeFirstTower.row,playerColumn)
	currCell.value = int(currCell.value) + firstTowerTime				# total Time for First Tower
	cellsToUpdate.append(currCell)

	if role == roleJungle:
		if numTDrags == 0:
			avgTimeFirstDrag = general.find("Avg. Time First Dragon")
			averageTimeCell = general.cell(avgTimeFirstDrag.row,playerColumn)
			firstDragTime = averageTimeCell.value
		totalTimeFirstDrag = general.find("Total Time for First Dragon (ms)")
		currCell = general.cell(totalTimeFirstDrag.row,playerColumn)
		currCell.value = int(currCell.value) + firstDragTime			# total first Dragon time
		cellsToUpdate.append(currCell)

		if numHerald == 0:
			avgTimeFirstHerald = general.find("Avg. Time Rift Herald")
			averageTimeCell = general.cell(avgTimeFirstHerald.row,playerColumn)
			heraldTime = averageTimeCell.value
		totalTimeFirstHerald = general.find("Total Time for First Rift Herald (ms)")
		currCell = general.cell(totalTimeFirstHerald.row,playerColumn)
		currCell.value = int(currCell.value) + heraldTime				# total Rift Herald Time
		cellsToUpdate.append(currCell)

		totalMatchDragons = general.find("Total Game Dragons")
		currCell = general.cell(totalMatchDragons.row,playerColumn)
		currCell.value = int(currCell.value) + totalDrags				# total Match Dragons
		cellsToUpdate.append(currCell)

	else:
		if laneTowerTime == 0:
			avgTimeOuterLaneT = general.find("Avg. Time Outer Lane Tower Killed")
			averageTimeCell = general.cell(avgTimeOuterLaneT.row,playerColumn)
			laneTowerTime = averageTimeCell.value
		totalTimeOuterTower = general.find("Total Time for Outer Lane Tower Kill (ms)")
		currCell = general.cell(totalTimeOuterTower.row,playerColumn)
		currCell.value = int(currCell.value) + laneTowerTime			# total time Outer Tower Killed
		cellsToUpdate.append(currCell)

	totalTowerAssists = general.find("Total Tower Assists")
	currCell = general.cell(totalTowerAssists.row,playerColumn)
	currCell.value = int(currCell.value) + numTowerA					# total Tower Assists
	cellsToUpdate.append(currCell)

	totalInhibAssists = general.find("Total Inhibitor Assists")
	currCell = general.cell(totalInhibAssists.row,playerColumn)
	currCell.value = int(currCell.value) + numInhibA					# total Inhibitor Assists
	cellsToUpdate.append(currCell)

	totalChampLV = general.find("Total Champ Level")
	currCell = general.cell(totalChampLV.row,playerColumn)
	currCell.value = int(currCell.value) + champLV						# total Champ LV
	cellsToUpdate.append(currCell)

	totalKillingSpree = general.find("Total Killing Spree")
	currCell = general.cell(totalKillingSpree.row,playerColumn)
	currCell.value = int(currCell.value) + largestKS					# total largest Killing Spree
	cellsToUpdate.append(currCell)

	totalGameTime = general.find("Total Game Time (secs)")
	currCell = general.cell(totalGameTime.row,playerColumn)
	currCell.value = int(currCell.value) + matchDuration				# total match length
	cellsToUpdate.append(currCell)

	### timeline per 10min stats ###

	CS_list = general.findall("Total CS per min")
	CSDiff_list = general.findall("Total CS Diff per min")
	XP_list = general.findall("Total XP per min")
	XPdiff_list = general.findall("Total XP Diff per min")
	DmgTaken_list = general.findall("Total Damage Taken per min")
	DmgTakenDiff_list = general.findall("Total Damage Taken Diff per min")

	csPM_list = [csPM10,csPM20,csPM30,csPM40]
	csDiffPM_list = [csDiff10,csDiff20,csDiff30,csDiff40]
	xpPM_list = [xpPM10,xpPM20,xpPM30,xpPM40]
	xpDiffPM_list = [xpDiff10,xpDiff20,xpDiff30,xpDiff40]
	dmgTakenPM_list = [dmgT10,dmgT20,dmgT30,dmgT40]
	dmgDiffPM_list = [dmgTDiff10,dmgTDiff20,dmgTDiff30,dmgTDiff40]
	for i in range(0,4):
		CS_cell = general.cell(CS_list[i].row,playerColumn)
		CSDiff_cell = general.cell(CSDiff_list[i].row,playerColumn)
		XP_cell = general.cell(XP_list[i].row,playerColumn)
		XPdiff_cell = general.cell(XPdiff_list[i].row,playerColumn)
		DmgTaken_cell = general.cell(DmgTaken_list[i].row,playerColumn)
		DmgTakenDiff_cell = general.cell(DmgTakenDiff_list[i].row,playerColumn)
		
		CS_cell.value = float(CS_cell.value) + csPM_list[i]
		CSDiff_cell.value = float(CSDiff_cell.value) + csDiffPM_list[i]
		XP_cell.value = float(XP_cell.value) + xpPM_list[i]
		XPdiff_cell.value = float(XPdiff_cell.value) + xpDiffPM_list[i]
		DmgTaken_cell.value = float(DmgTaken_cell.value) + dmgTakenPM_list[i]
		DmgTakenDiff_cell.value = float(DmgTakenDiff_cell.value) + dmgDiffPM_list[i]

		cellsToUpdate.append(CS_cell)
		cellsToUpdate.append(CSDiff_cell)
		cellsToUpdate.append(XP_cell)
		cellsToUpdate.append(XPdiff_cell)
		cellsToUpdate.append(DmgTaken_cell)
		cellsToUpdate.append(DmgTakenDiff_cell)

		#update_cells = [CS_cell,CSDiff_cell,XP_cell,XPdiff_cell,DmgTaken_cell,DmgTakenDiff_cell]
		# general.update_cell(CS_cell.row,CS_cell.col,CS_cell.value)
		# general.update_cell(CSDiff_cell.row,CSDiff_cell.col,CSDiff_cell.value)
		# general.update_cell(XP_cell.row,XP_cell.col,XP_cell.value)
		# general.update_cell(XPdiff_cell.row,XPdiff_cell.col,XPdiff_cell.value)
		# general.update_cell(DmgTaken_cell.row,DmgTaken_cell.col,DmgTaken_cell.value)
		# general.update_cell(DmgTakenDiff_cell.row,DmgTakenDiff_cell.col,DmgTakenDiff_cell.value)

	if matchDuration > 2400:
		totalGamesOver30 = general.find("30 - end mins - Total Games")
		currCell = general.cell(totalGamesOver30.row,playerColumn)
		currCell.value = int(currCell.value) + 1
		cellsToUpdate.append(currCell)
	elif matchDuration > 1800:
		totalGamesOver20 = general.find("20-30 mins - Total Games")
		currCell = general.cell(totalGamesOver20.row,playerColumn)
		currCell.value = int(currCell.value) + 1
		cellsToUpdate.append(currCell)

	### timeline per minute statistics ###

	if len(TLgold) < 30:
		timelineLength = len(TLgold)
	else:
		timelineLength = 30

	timelineGold = general.findall("Gold")
	timelineXP = general.findall("XP")
	timelineCS = general.findall("CS")
	timelineJngCS = general.findall("Jungle CS")

	for x in range(0,timelineLength):
		if x > 19:
			timelineGameTotal = general.cell((timelineGold[x].row-1),playerColumn)
			timelineGameTotal.value = int(timelineGameTotal.value) + 1
			cellsToUpdate.append(timelineGameTotal)
		goldTL_Cell = general.cell(timelineGold[x].row,playerColumn)
		xpTL_Cell = general.cell(timelineXP[x].row,playerColumn)
		csTL_Cell = general.cell(timelineCS[x].row,playerColumn)
		jngCSTL_Cell = general.cell(timelineJngCS[x].row,playerColumn)

		goldTL_Cell.value = int(goldTL_Cell.value) + TLgold[x]
		xpTL_Cell.value = int(xpTL_Cell.value) + TLxp[x]
		csTL_Cell.value = int(csTL_Cell.value) + TLcs[x]
		jngCSTL_Cell.value = int(jngCSTL_Cell.value) + TLjngCS[x]

		#timelineUpdate = [goldTL_Cell,xpTL_Cell,csTL_Cell,jngCSTL_Cell]
		cellsToUpdate.append(goldTL_Cell)
		cellsToUpdate.append(xpTL_Cell)
		cellsToUpdate.append(csTL_Cell)
		cellsToUpdate.append(jngCSTL_Cell)

	### who you played with statistics ###

	if len(playedWith) > 0:
		for partner in playedWith:
			buddy = general.find(partner)
			numGamesTogether = general.cell((buddy.row+1),playerColumn)
			numGamesTogether.value = int(numGamesTogether.value) + 1
			cellsToUpdate.append(numGamesTogether)
			if win:
				numWinsTogether = general.cell((buddy.row+2),playerColumn)
				numWinsTogether.value = int(numWinsTogether.value) + 1
				cellsToUpdate.append(numWinsTogether)

	### which champion you played statistics ###
	if sumID == imawizardm8:
		findName = "imawizardm8 - champs"
	elif sumID == imBS:
		findName = "imBS - champs"
	elif sumID == Rhetorikal:
		findName = "Rhetorikal - champs"
	elif sumID == JARVIS:
		findName = "JARVIS - champs"
	elif sumID == manbones2:
		findName = "manbones2 - champs"
	elif sumID == Teesang:
		findName = "Teesang - champs"
	elif sumID == jawsmoney:
		findName = "jawsmoney - champs"
	elif sumID == kugeku:
		findName = "kugeku - champs"
	elif sumID == Dugtrio:
		findName = "Dugtrio - champs"
	elif sumID == SmoothCactus:
		findName = "SmoothCactus - champs"
	elif sumID == Piangle:
		findName = "Piangle - champs"

	playerChamps = general.find(findName)
	champList = general.row_values(playerChamps.row)

	if champName in champList:
		champColumn = champList.index(champName) + 1 # because columns start at 1 in google sheets, not 0
		champGames = general.cell((playerChamps.row+1),champColumn)
		if win:
			champWins = general.cell((playerChamps.row+2),champColumn)
			champWins.value = int(champWins.value) + 1
			cellsToUpdate.append(champWins)
		champKills = general.cell((playerChamps.row+3),champColumn)
		champDeaths = general.cell((playerChamps.row+4),champColumn)
		champAssists = general.cell((playerChamps.row+5),champColumn)
		champCS = general.cell((playerChamps.row+6),champColumn)

		champGames.value = int(champGames.value) + 1
		champKills.value = int(champKills.value) + kills
		champDeaths.value = int(champDeaths.value) + deaths
		champAssists.value = int(champAssists.value) + assists
		champCS.value = int(champCS.value) + totalMinions + totalJngCS

		updateChampStats = [champGames,champKills,champDeaths,champAssists,champCS]
	else:
		nextFreeColumn = champList.index('') + 1
		champCell = general.cell(playerChamps.row,nextFreeColumn)
		champGames = general.cell((playerChamps.row+1),nextFreeColumn)
		if win:
			champWins = general.cell((playerChamps.row+2),nextFreeColumn)
			champWins.value = 1
			cellsToUpdate.append(champWins)
		else:
			champWins = general.cell((playerChamps.row+2),nextFreeColumn)
			champWins.value = 0
			cellsToUpdate.append(champWins)
		champKills = general.cell((playerChamps.row+3),nextFreeColumn)
		champDeaths = general.cell((playerChamps.row+4),nextFreeColumn)
		champAssists = general.cell((playerChamps.row+5),nextFreeColumn)
		champCS = general.cell((playerChamps.row+6),nextFreeColumn)

		champCell.value = champName
		champGames.value = 1
		champKills.value = kills
		champDeaths.value = deaths
		champAssists.value = assists
		champCS.value = totalMinions + totalJngCS

		updateChampStats = [champCell,champGames,champKills,champDeaths,champAssists,champCS]

	# update everything
	general.update_cells(cellsToUpdate)
	#general.update_cells(update_cells)
	#general.update_cells(timelineUpdate)
	general.update_cells(updateChampStats)
	print ("finished updating sheet")

# def updatePlayerTotals():
# 	# totals

# def updateOtherTotals():
# 	# row 425

# def update10minTimeline():
# 	# row 448

# def updateTimeline():
# 	# row 480

# def updateChampsPlayed():
# 	# row 632

##########################################################################################################
######                        execution starts here                                                 ######
##########################################################################################################
sheet = accessRankedExcelDoc()
#updateExcel(sheet)

for sumName in sys.argv[1:]:
	IDresponse = getSummonerID(sumName)
	sumID = IDresponse[sumName]["id"]
	if str(sumID) in leagueIDs:
		# print ("match!:" + str(sumName))
		historyResponse = getRecentGames(sumID) # max 10 games in history
		for currGame in historyResponse["games"]:
			if currGame["gameType"] == "MATCHED_GAME" and currGame["gameMode"] == "CLASSIC":
				if currGame["subType"] == "NORMAL":
					lanePosition = grabPlayerStats(currGame)
					gameID = currGame["gameId"]
					print ("normal game ~ id: " + str(gameID))
				elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
					lanePosition = grabPlayerStats(currGame)
					gameID = currGame["gameId"]
					if checkHistory(sheet,str(sumID),str(gameID)):
						print("ranked game ~ id: " + str(gameID))
						matchResponse = getMatch(gameID)
						grabMatchStats(matchResponse, sumID, lanePosition, sheet, currGame)
						updateHistory(sheet,str(sumID),str(gameID))
					else:
						print("DONE BEFORE ranked game ~ id: " + str(gameID))
				else:
					continue
			else:
				print ("other Game Mode")



		# if int(last) in gameID_List and int(last) != lastgame:
		# 	lastGameIndex = gameID_List.index(int(last)) + 1
		# 	for currGame in historyResponse["games"][lastGameIndex:]:
		# 		if currGame["gameType"] == "MATCHED_GAME" and currGame["gameMode"] == "CLASSIC":
		# 			if currGame["subType"] == "NORMAL":
		# 				lanePosition = grabPlayerStats(currGame)
		# 				gameID = currGame["gameId"]
		# 				print ("normal game ~ id: " + str(gameID))
		# 				updateHistoryOldest(sheet,str(sumID),gameID)
		# 			elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
		# 				lanePosition = grabPlayerStats(currGame)
		# 				gameID = currGame["gameId"]
		# 				print ("ranked game ~ id: " + str(gameID) + "lane: " + str(lanePosition))
		# 				matchResponse = getMatch(gameID)
		# 				# rankedSheet = accessRankedExcelDoc()
		# 				# grabMatchStats(matchResponse, sumID, lanePosition, rankedSheet, currGame)
		# 				updateHistoryOldest(sheet,str(sumID),gameID)
		# 			else:
		# 				continue
		# 		else:
		# 			print ("other GameMode")
		# 			updateHistoryOldest(sheet,str(sumID),currGame["gameId"])
		# 			continue
		# else:
		# 	print ("all good")
	# 	for currGame in historyResponse["games"]:
	# 		if currGame["gameType"] == "MATCHED_GAME" and currGame["gameMode"] == "CLASSIC":
	# 			if currGame["subType"] == "NORMAL":
	# 				lanePosition = grabPlayerStats(currGame)
	# 				gameID = currGame["gameId"]
	# 				print ("normal game ~ id: " + str(gameID))
	# 			elif currGame["subType"] == "RANKED_SOLO_5x5" or "RANKED_FLEX_SR":
	# 				lanePosition = grabPlayerStats(currGame)
	# 				gameID = currGame["gameId"]
	# 				print ("ranked game ~ id: " + str(gameID) + "lane: " + str(lanePosition))
	# 				matchResponse = getMatch(gameID)
	# 				rankedSheet = accessRankedExcelDoc()
	# 				grabMatchStats(matchResponse, sumID, lanePosition, rankedSheet, currGame)
	# 			else:
	# 				continue
	# 		else:
	# 			print ("other GameMode")
	# 			continue
	# else:
	# 	print("non-matching summoner name: " + str(sumName))


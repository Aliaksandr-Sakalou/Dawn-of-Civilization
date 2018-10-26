from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = []

def isReborn(iPlayer):
	return gc.getPlayer(iPlayer).isReborn()
	
def getOrElse(dDictionary, key, default):
	if key in dDictionary: return dDictionary[key]
	return default
	
def getArea(iPlayer, tRectangle, dExceptions, bReborn=None, dChangedRectangle={}, dChangedExceptions={}):
	if bReborn is None: bReborn = isReborn(iPlayer)
	tBL, tTR = tRectangle[iPlayer]
	lExceptions = getOrElse(dExceptions, iPlayer, [])
	
	if bReborn:
		if iPlayer in dChangedRectangle:
			tBL, tTR = dChangedRectangle[iPlayer]
			lExceptions = getOrElse(dChangedExceptions, iPlayer, [])
	
	left, bottom = tBL
	right, top = tTR		
	return [(x, y) for x in range(left, right+1) for y in range(bottom, top+1) if (x, y) not in lExceptions]

def getCapital(iPlayer, bReborn=None):
	if bReborn is None: bReborn = isReborn(iPlayer)
	if bReborn and iPlayer in dChangedCapitals:
		return dChangedCapitals[iPlayer]
	return tCapitals[iPlayer]
	
def getRespawnCapital(iPlayer, bReborn=None):
	if iPlayer in dRespawnCapitals: return dRespawnCapitals[iPlayer]
	return getCapital(iPlayer, bReborn)
	
def getNewCapital(iPlayer, bReborn=None):
	if iPlayer in dNewCapitals: return dNewCapitals[iPlayer]
	return getRespawnCapital(iPlayer, bReborn)
	
def getBirthArea(iPlayer):
	return getArea(iPlayer, tBirthArea, dBirthAreaExceptions)
	
def getBirthRectangle(iPlayer, bExtended = None):
	if bExtended is None: bExtended = isExtendedBirth(iPlayer)
	if iPlayer in dChangedBirthArea and bExtended:
		return dChangedBirthArea[iPlayer]
	return tBirthArea[iPlayer]
	
def getBirthExceptions(iPlayer):
	if iPlayer in dBirthAreaExceptions: return dBirthAreaExceptions[iPlayer]
	return []
	
def getCoreArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tCoreArea, dCoreAreaExceptions, bReborn, dChangedCoreArea, dChangedCoreAreaExceptions)
	
def getNormalArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tNormalArea, dNormalAreaExceptions, bReborn, dChangedNormalArea, dChangedNormalAreaExceptions)

def getBroaderArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tBroaderArea, {}, dChangedBroaderArea)
	
def getRespawnArea(iPlayer):
	if iPlayer in dRespawnArea: return getArea(iPlayer, dRespawnArea, {})
	return getNormalArea(iPlayer)
	
def getRebirthArea(iPlayer):
	if iPlayer in dRebirthArea: return getArea(iPlayer, dRebirthArea, dRebirthAreaExceptions)
	return getBirthArea(iPlayer)
	
def updateCore(iPlayer):
	lCore = getCoreArea(iPlayer)
	for x in range(iWorldX):
		for y in range(iWorldY):
			plot = gc.getMap().plot(x, y)
			if plot.isWater() or (plot.isPeak() and (x, y) not in lPeakExceptions): continue
			plot.setCore(iPlayer, (x, y) in lCore)
			
def isForeignCore(iPlayer, tPlot):
	x, y =  tPlot
	plot = gc.getMap().plot(x, y)
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		if plot.isCore(iLoopPlayer):
			return True
	return False
	
def isExtendedBirth(iPlayer):
	if gc.getGame().getActivePlayer() == iPlayer: return False
	
	# add special conditions for extended AI flip zones here
	if iPlayer == iOttomans and pByzantium.isAlive(): return False
	
	return True
			
def init():
	for iPlayer in range(iNumPlayers):
		updateCore(iPlayer)
	
### Capitals ###

tCapitals = (
(0, 0), # Thebes
(0, 0), # Chang'an
(0, 0), # Babylon
(0, 0), # Harappa
(0, 0), # Athens
(0, 0), # Pataliputra
(0, 0), # Sur
(0, 0), # Tonga
(0, 0), # Persepolis
(0, 0), # Rome
(0, 0), # Thanjavur
(0, 0), # Aksum
(0, 0), # Seoul
(0, 0), # Tikal
(0, 0), # Constantinople
(0, 0), # Kyoto
(0, 0), # Oslo
(0, 0), # Orduqent
(0, 0), # Mecca
(0, 0), # Lhasa
(0, 0), # Palembang
(0, 0), # Cordoba
(0, 0), # Madrid
(0, 0), # Paris
(0, 0), # Angkor
(0, 0), # London
(0, 0), # Cologne
(0, 0), # Moskow
(0, 0), # Timbuktu
(0, 0), # Krakow
(0, 0), # Lisboa
(0, 0), # Cuzco
(0, 0), # Mailand
(0, 0), # Karakorum
(0, 0), # Tenochtitlan
(0, 0), # Delhi
(0, 0), # Sogut
(0, 0), # Ayutthaya
(0, 0), # Mbanza Kongo
(0, 0), # Amsterdam
(0, 0), # Berlin
(0, 0), # Washington
(0, 0), # Buenos Aires
(0, 0), # Rio de Janeiro
(0, 0), # Ottawa
)

dChangedCapitals = {
iChina : (0, 0),	# Beijing
iIndia : (0, 0),	# Delhi
iCarthage : (0, 0),	# Carthage
iPersia : (0, 0),	# Esfahan (Iran)
iTamils : (0, 0),	# Vijayanagara
iMaya : (0, 0),	# Bogota (Colombia)
iKhmer : (0, 0),	# Hanoi
iHolyRome : (0, 0),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = {
iJapan : (0, 0),	# Tokyo
iVikings : (0, 0),	# Stockholm
iHolyRome : (0, 0),	# Vienna
iItaly : (0, 0),	# Rome
iMongolia : (0, 0),	# Khanbaliq
iOttomans : (0, 0),	# Istanbul
}

# new capital locations on respawn
dRespawnCapitals = {
iEgypt : (0, 0),	# Cairo
iChina :  (0, 0),	# Beijing
iIndia : (0, 0),	# Delhi
iPersia : (0, 0),	# Esfahan
iEthiopia : (0, 0),	# Addis Ababa
iJapan : (0, 0),	# Tokyo
iVikings : (0, 0),	# Stockholm
iTurks: (0, 0), 	# Herat
iIndonesia : (0, 0),	# Jakarta
iMoors : (0, 0),	# Marrakesh
iHolyRome : (0, 0),	# Vienna
iInca : (0, 0),		# Lima
iItaly : (0, 0),	# Rome
iMughals : (0, 0),	# Karachi
iOttomans : (0, 0),	# Istanbul
}

### Birth Area ###

tBirthArea = (
((0, 0),	(0, 0)),	# Egypt
((0, 0),	(0, 0)), 	# China
((0, 0),	(0, 0)),	# Babylonia
((0, 0),	(0, 0)),	# Harappa
((0, 0),	(0, 0)),	# Greece
((0, 0),	(0, 0)),	# India
((0, 0),	(0, 0)),	# Carthage
((0, 0),	(0, 0)),	# Polynesia
((0, 0),	(0, 0)),	# Persia
((0, 0),	(0, 0)),	# Rome
((0, 0),	(0, 0)),	# Tamils
((0, 0),	(0, 0)),	# Ethiopia
((0, 0),	(0, 0)),	# Korea
((0, 0),	(0, 0)),	# Maya
((0, 0),	(0, 0)),	# Byzantium
((0, 0),	(0, 0)),	# Japan
((0, 0),	(0, 0)),	# Vikings
((0, 0), 	(0, 0)),	# Turks
((0, 0),	(0, 0)),	# Arabia
((0, 0),	(0, 0)),	# Tibet
((0, 0),	(0, 0)),	# Indonesia
((0, 0),	(0, 0)),	# Moors
((0, 0),	(0, 0)),	# Spain
((0, 0),	(0, 0)),	# France
((0, 0),	(0, 0)),	# Khmer
((0, 0),	(0, 0)),	# England
((0, 0),	(0, 0)),	# HolyRome
((0, 0),	(0, 0)),	# Russia
((0, 0),	(0, 0)),	# Mali
((0, 0),	(0, 0)),	# Poland
((0, 0),	(0, 0)),	# Portugal
((0, 0),	(0, 0)),	# Inca
((0, 0),	(0, 0)),	# Italy
((0, 0),	(0, 0)),	# Mongolia
((0, 0),	(0, 0)),	# Aztecs
((0, 0),	(0, 0)),	# Mughals
((0, 0),	(0, 0)),	# Ottomans
((0, 0), 	(0, 0)),	# Thailand
((0, 0),	(0, 0)),	# Congo
((0, 0),	(0, 0)),	# Netherlands
((0, 0),	(0, 0)),	# Germany
((0, 0),	(0, 0)),	# America
((0, 0),	(0, 0)),	# Argentina
((0, 0),	(0, 0)),	# Brazil
((0, 0),	(0, 0)),	# Canada
)

dChangedBirthArea = {
iPersia :	((0, 0),	(0, 0)),	# includes Assyria and Anatolia
iSpain : 	((0, 0),	(0, 0)),	# includes Catalonia
iInca : 	((0, 0),	(0, 0)),
iMongolia : 	((0, 0),	(0, 0)),	# 6 more west, 1 more south
iOttomans : 	((0, 0), 	(0, 0)), 	# includes Constantinople
iArgentina : 	((0, 0),	(0, 0)),	# includes Chile
}

dBirthAreaExceptions = {
iChina : [],
iBabylonia : [],
iHarappa : [],
iGreece : [],
iIndia : [],
iRome : [],
iByzantium : [],
iTurks : [],
iArabia : [],
iTibet : [],
iIndonesia : [],
iMoors : [],
iSpain : [],
iFrance : [],
iHolyRome : [],
iRussia : [],
iPoland : [],
iMongolia : [],
iMughals : [],
iOttomans : [],
iNetherlands : [],
iGermany : [],
iAmerica : [],
iArgentina : [],
iBrazil : [],
iCanada : [],
}

### Core Area ###

tCoreArea = (
((0, 0),	(0, 0)),	# Egypt
((0, 0),	(0, 0)),	# China
((0, 0),	(0, 0)),	# Babylonia
((0, 0),	(0, 0)),	# Harappa
((0, 0),	(0, 0)),	# Greece
((0, 0),	(0, 0)),	# India
((0, 0),	(0, 0)),	# Phoenicia
((0, 0),	(0, 0)),	# Polynesia
((0, 0),	(0, 0)),	# Persia
((0, 0),	(0, 0)),	# Rome
((0, 0),	(0, 0)),	# Tamils
((0, 0),	(0, 0)),	# Ethiopia
((0, 0),	(0, 0)),	# Korea
((0, 0),	(0, 0)),	# Maya
((0, 0),	(0, 0)),	# Byzantium
((0, 0),	(0, 0)),	# Japan
((0, 0),	(0, 0)),	# Vikings
((0, 0), 	(0, 0)),	# Turks
((0, 0),	(0, 0)),	# Arabia
((0, 0),	(0, 0)),	# Tibet
((0, 0),	(0, 0)),	# Indonesia
((0, 0),	(0, 0)),	# Moors
((0, 0),	(0, 0)),	# Spain
((0, 0),	(0, 0)),	# France
((0, 0),	(0, 0)),	# Khmer
((0, 0),	(0, 0)),	# England
((0, 0),	(0, 0)),	# HolyRome
((0, 0),	(0, 0)),	# Russia
((0, 0),	(0, 0)),	# Mali
((0, 0),	(0, 0)),	# Poland
((0, 0),	(0, 0)),	# Portugal
((0, 0),	(0, 0)),	# Inca
((0, 0),	(0, 0)),	# Italy
((0, 0),	(0, 0)),	# Mongolia
((0, 0),	(0, 0)),	# Aztecs
((0, 0),	(0, 0)),	# Mughals
((0, 0),	(0, 0)),	# Turkey
((0, 0),	(0, 0)),	# Thailand
((0, 0),	(0, 0)),	# Congo
((0, 0),	(0, 0)),	# Netherlands
((0, 0),	(0, 0)),	# Germany
((0, 0),	(0, 0)),	# America
((0, 0),	(0, 0)),	# Argentina
((0, 0),	(0, 0)),	# Brazil
((0, 0),	(0, 0)),	# Canada
)

dChangedCoreArea = {
<<<<<<< HEAD
iChina : 	((99, 42),	(107, 47)),
iGreece :	((65, 39), 	(69, 42)),
iIndia : 	((88, 33),	(91, 38)),
iPhoenicia:	((54, 37),	(60, 39)),
iMaya : 	((24, 26),	(31, 32)),	# Colombia
iByzantium :	((67, 44),	(69, 46)),
iJapan : 	((111, 41),	(116, 49)),
iTurks : 	((79, 37),	(85, 44)),
iArabia :	((73, 30),	(82, 36)),
iMoors : 	((51, 37),	(56, 39)),
iSpain : 	((49, 40),	(55, 46)),
iKhmer : 	((97, 35),	(102, 38)),
iHolyRome : 	((61, 46),	(66, 51)),
iItaly : 	((58, 40),	(63, 47)),
iMongolia : 	((95, 46),	(106, 52)),
iAztecs : 	((16, 35),	(19, 40)),	# Mexico
iMughals : 	((86, 37),	(94, 43)),
iOttomans : 	((67, 42),	(76, 47)),
iGermany : 	((58, 49),	(63, 55)),
}

dCoreAreaExceptions = {
iChina : [(99, 46), (99, 47), (104, 43), (105, 43), (106, 43), (107, 43), (105, 44), (106, 44), (106, 47)],
iHarappa : [(85, 41), (88, 37), (88, 38)],
iGreece : [(64, 45), (65, 45)],
iPersia : [(85, 37), (85, 38), (85, 39)],
iByzantium : [(71, 40)],
iTurks : [(84, 36), (84, 37), (85, 36), (85, 37), (85, 38), (85, 39)],
iArabia : [(72, 42), (73, 42), (74, 42), (77, 33), (78, 33), (77, 34), (78, 34), (76, 35), (77, 35), (78, 35), (76, 36), (77, 36), (78, 36), (76, 37), (77, 37), (78, 37)],
iTibet : [(98, 42)],
iIndonesia : [(100, 30), (101, 29), (101, 30)],
iSpain : [(49, 43), (49, 44), (50, 43), (50, 44)],
iFrance : [(51, 46), (52, 46), (55, 46), (57, 46)],
iHolyRome : [(64, 51), (64, 52), (64, 53), (64, 54)],
iRussia : [(68, 49), (68, 59), (69, 49), (69, 59), (70, 59), (71, 49)],
iPoland : [(63, 50), (64, 50)],
iMongolia : [(102, 47), (103, 47)],
iMughals : [(86, 43)],
iGermany : [(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51), (64, 49), (64, 50), (64, 51), (64, 52), (64, 53), (65, 49), (65, 51), (65, 52), (65, 53)],
iAmerica : [(23, 50), (27, 50), (29, 50), (30, 50)],
iArgentina : [(35, 12)],
iCanada : [(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
}

dChangedCoreAreaExceptions = {
iChina : [(99, 46), (99, 47), (106, 47)],
iGreece : [(64, 45), (65, 45), (66, 46)],
#iPersia : [], # Iran
iMaya : [(30, 26), (30, 27), (30, 28), (30, 29), (31, 26), (31, 27)], # Colombia
iSpain : [(49, 41), (49, 42), (49, 43), (49, 44), (50, 42), (50, 43), (50, 44), (55, 46)],
iKhmer : [(104, 39)],
iHolyRome : [(61, 51), (64, 51), (65, 51), (66, 51)],
iItaly : [(63, 46), (63, 47)],
iAztecs : [(19, 40)], # Mexico
iMughals : [(92, 43), (93, 43), (94, 42), (94, 43)],
iOttomans : [(67, 42), (70, 42), (71, 42), (73, 42), (74, 42), (75, 42)],
iGermany : [(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51)],
=======
iChina :	((0, 0),	(0, 0)),
iGreece :	((0, 0),	(0, 0)),
iIndia :	((0, 0),	(0, 0)),
iPhoenicia :	((0, 0),	(0, 0)),
iMaya :		((0, 0),	(0, 0)),	# Colombia
iByzantium :	((0, 0),	(0, 0)),
iJapan :	((0, 0), 	(0, 0)),
iTurks :	((0, 0), 	(0, 0)),
iArabia :	((0, 0),	(0, 0)),
iMoors :	((0, 0),	(0, 0)),
iSpain :	((0, 0),	(0, 0)),
iKhmer :	((0, 0),	(0, 0)),
iHolyRome :	((0, 0),	(0, 0)),
iItaly :	((0, 0),	(0, 0)),
iMongolia :	((0, 0),	(0, 0)),
iAztecs :	((0, 0),	(0, 0)),	# Mexico
iMughals :	((0, 0),	(0, 0)),
iOttomans :	((0, 0),	(0, 0)),
iGermany :	((0, 0),	(0, 0)),
}

dCoreAreaExceptions = {
iChina : [],
iBabylonia : [],
iHarappa : [],
iGreece : [],
iIndia : [],
iRome : [],
iByzantium : [],
iTurks : [],
iArabia : [],
iTibet : [],
iIndonesia : [],
iSpain : [],
iFrance : [],
iHolyRome : [],
iRussia : [],
iPoland : [],
iMongolia : [],
iMughals : [],
iOttomans : [],
iNetherlands : [],
iGermany : [],
iAmerica : [],
iArgentina : [],
iCanada : [],
}

dChangedCoreAreaExceptions = {
iChina : [],
iIndia : [],
iMaya : [], # Colombia
iArabia : [],
iKhmer:	[],
iMoors : [],
iSpain : [],
iHolyRome : [],
iItaly : [],
iMongolia : [],
iMughals : [],
iOttomans : [],
iGermany : [],
>>>>>>> map
}

### Normal Area ###

tNormalArea = (
((0, 0),	(0, 0)),	# Egypt
((0, 0),	(0, 0)),	# China
((0, 0),	(0, 0)),	# Babylonia
((0, 0),	(0, 0)), 	# Harappa
((0, 0),	(0, 0)),	# Greece
((0, 0),	(0, 0)),	# India
((0, 0),	(0, 0)),	# Carthage
((0, 0),	(0, 0)),	# Polynesia
((0, 0),	(0, 0)),	# Persia
((0, 0),	(0, 0)),	# Rome
((0, 0),	(0, 0)),	# Tamils
((0, 0),	(0, 0)),	# Ethiopia
((0, 0),	(0, 0)),	# Korea
((0, 0),	(0, 0)),	# Maya
((0, 0),	(0, 0)),	# Byzantium
((0, 0),	(0, 0)),	# Japan
((0, 0),	(0, 0)),	# Vikings
((0, 0), 	(0, 0)),	# Turks
((0, 0),	(0, 0)),	# Arabia
((0, 0),	(0, 0)),	# Tibet
((0, 0),	(0, 0)),	# Indonesia
((0, 0),	(0, 0)),	# Moors
((0, 0),	(0, 0)),	# Spain
((0, 0),	(0, 0)),	# France
((0, 0),	(0, 0)),	# Khmer
((0, 0),	(0, 0)),	# England
((0, 0),	(0, 0)),	# HolyRome
((0, 0),	(0, 0)),	# Russia
((0, 0),	(0, 0)),	# Mali
((0, 0),	(0, 0)),	# Poland
((0, 0),	(0, 0)),	# Portugal
((0, 0),	(0, 0)),	# Inca
((0, 0),	(0, 0)),	# Italy
((0, 0),	(0, 0)),	# Mongolia
((0, 0),	(0, 0)),	# Aztecs
((0, 0),	(0, 0)),	# Mughals
((0, 0),	(0, 0)),	# Ottomans
((0, 0),	(0, 0)),	# Thailand
((0, 0),	(0, 0)),	# Congo
((0, 0),	(0, 0)),	# Netherlands
((0, 0),	(0, 0)),	# Germany
((0, 0),	(0, 0)),	# America
((0, 0),	(0, 0)),	# Argentina
((0, 0),	(0, 0)),	# Brazil
((0, 0),	(0, 0)),	# Canada
)

dChangedNormalArea = {
iIndia : 	((0, 0),	(0, 0)),
iCarthage :	((0, 0),	(0, 0)),
iMaya : 	((0, 0),	(0, 0)),	# Colombia
iArabia : 	((0, 0),	(0, 0)),
iKhmer : 	((0, 0),	(0, 0)),
iHolyRome : 	((0, 0),	(0, 0)),
}

dNormalAreaExceptions = {
iChina : [],
iBabylonia : [],
iHarappa : [],
iGreece : [],
iIndia : [],
iPolynesia : [],
iPersia : [],
iRome : [],
iEthiopia : [],
iByzantium : [],
iJapan : [],
iVikings : [],
iTurks : [],
iArabia : [],
iSpain : [],
iTibet : [],
iIndonesia : [],
iMoors : [],
iSpain : [],
iFrance : [],
iKhmer:	[],
iHolyRome : [],
iRussia : [],
iPoland : [],
iInca : [],
iItaly : [],
iMongolia : [],
iMughals : [],
iOttomans : [],
iThailand : [],
iNetherlands : [],
iGermany : [],
iAmerica : [],
iArgentina : [],
iBrazil : [],
iCanada : [],
}

dChangedNormalAreaExceptions = {
iMaya : [], # Colombia
iArabia : [],
iKhmer:	[],
iHolyRome : [],
}

### Broader Area ###

tBroaderArea = (
((0, 0),	(0, 0)),	# Egypt
((0, 0),	(0, 0)),	# China
((0, 0),	(0, 0)),	# Babylonia
((0, 0),	(0, 0)),	# Harappa
((0, 0),	(0, 0)),	# Greece
((0, 0),	(0, 0)),	# India
((0, 0),	(0, 0)),	# Carthage
((0, 0),	(0, 0)),	# Polynesia
((0, 0),	(0, 0)),	# Persia
((0, 0),	(0, 0)),	# Rome
((0, 0),	(0, 0)),	# Tamils
((0, 0),	(0, 0)),	# Ethiopia
((0, 0),	(0, 0)),	# Korea
((0, 0),	(0, 0)),	# Maya
((0, 0),	(0, 0)),	# Byzantium
((0, 0),	(0, 0)),	# Japan
((0, 0),	(0, 0)),	# Vikings
((0, 0), 	(0, 0)),	# Turks
((0, 0),	(0, 0)),	# Arabia
((0, 0),	(0, 0)),	# Tibet
((0, 0),	(0, 0)),	# Indonesia
((0, 0),	(0, 0)),	# Moors
((0, 0),	(0, 0)),	# Spain
((0, 0),	(0, 0)),	# France
((0, 0),	(0, 0)),	# Khmer
((0, 0),	(0, 0)),	# England
((0, 0),	(0, 0)),	# Holy Rome
((0, 0),	(0, 0)),	# Russia
((0, 0),	(0, 0)),	# Mali
((0, 0),	(0, 0)),	# Poland
((0, 0),	(0, 0)),	# Portugal
((0, 0),	(0, 0)),	# Inca
((0, 0),	(0, 0)),	# Italy
((0, 0),	(0, 0)),	# Mongolia
((0, 0),	(0, 0)),	# Aztecs
((0, 0),	(0, 0)),	# Mughals
((0, 0),	(0, 0)),	# Ottomans
((0, 0),	(0, 0)),	# Thailand
((0, 0),	(0, 0)),	# Congo
((0, 0),	(0, 0)),	# Netherlands
((0, 0),	(0, 0)),	# Germany
((0, 0),	(0, 0)),	# America
((0, 0),	(0, 0)),	# Argentina
((0, 0),	(0, 0)),	# Brazil
((0, 0),	(0, 0)),	# Canada
)

dChangedBroaderArea = {
iCarthage :	((0, 0),	(0, 0)), 	# Carthage
iMaya :		((0, 0),	(0, 0)),	# Colombia
iByzantium :	((0, 0),	(0, 0)),
iHolyRome :	((0, 0),	(0, 0)),
iMughals :	((0, 0),	(0, 0)),
}

### Respawn area ###

dRespawnArea = {
iEgypt :	((0, 0), 	(0, 0)),
iChina :	((0, 0),	(0, 0)),
iIndia :	((0, 0),	(0, 0)),
iByzantium :	((0, 0),	(0, 0)),
iMoors :	((0, 0),	(0, 0)),
iInca :		((0, 0),	(0, 0)),
iMughals :	((0, 0),	(0, 0)),
}

dRespawnAreaExceptions = {
iIndia : [],
iMoors : [],
iInca : [],
}

### Rebirth area ###

dRebirthPlot = {
iPersia : (0, 0),	# Esfahan (Iran)
iMaya : (0, 0),		# Bogota (Colombia)
iAztecs : (0, 0),	# Mexico City (Mexico)
}

dRebirthArea = {
iPersia :	((0, 0),	(0, 0)),	# Iran
iMaya :		((0, 0),	(0, 0)),	# Colombia
iAztecs :	((0, 0),	(0, 0)),	# Mexico
}

dRebirthAreaExceptions = {
iPersia : [],
iMaya :	  [], # Colombia
iAztecs : [],
}
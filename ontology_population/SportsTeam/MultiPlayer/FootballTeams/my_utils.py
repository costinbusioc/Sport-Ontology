import pandas as pd

def get_country_code(link):
	tokens = link.split("/")
	if tokens[-1][-1] == 'N' and tokens[-1][-2] == '1':
		code = tokens[-1][:-2]
	else:
		code = tokens[-1][:-1]
	return code

def map_code_to_country(code):
	switcher = {
		'A': 'Austria',
		'AZ': 'Azerbaijan',
		'AND': 'Andorra',
		'ALB': 'Albania',
		'ARM': 'Armenia',
		'WER': 'Belarus',
		'BE': 'Belgium',
		'BOS': 'Bosnia and Herzegovina',
		'BU': 'Bulgaria',
		'KR': 'Croatia',
		'ZYP': 'Cyprus',
		'TS': 'Czech Republic',
		'DK': 'Denmark',
		'GB': 'United Kingdom',
		'FI': 'Finland',
		'FR': 'France',
		'GE': 'Georgia',
		'L': 'Germany',
		'GR': 'Greece',
		'GRS': 'Greece',
		'UNG': 'Hungary',
		'IS': 'Iceland',
		'IT': 'Italy',
		'KAS': 'Kazakhstan',
		'MO': 'Moldova',
		'NL': 'Netherlands',
		'NO': 'Norway',
		'PL': 'Poland',
		'PO': 'Portugal',
		'RO': 'Romania',
		'RU': 'Russia',
		'SC': 'Scotland',
		'SER': 'Serbia',
		'SLO': 'Slovakia',
		'SL': 'Slovenia',
		'ES': 'Spain',
		'SE': 'Sweden',
		'C': 'Switzerland',
		'TR': 'Turkey',
		'UKR': 'Ukraine',
	}
	return switcher[code]

def map_code_to_championship_name(code):
	switcher = {
		'A1': 'BundesligaAustria',
		'A2': 'pass',
		'AZ1': 'PremyerLiqasi',
		'AND1': 'PrimeraDivisió',
		'ALB1': 'KategoriaSuperiore',
		'ARM1': 'Bardsragujnchumb',
		'WER1': 'VysheyshayaLiga',
		'WER2': 'pass',
		'BE1': 'JupilerProLeague',
		'BE2': 'pass',
		'BOS1': 'PremijerLiga',
		'BU1': 'efbetLiga',
		'BU2': 'pass',
		'KR1': '1.HNL',
		'KR2': 'pass',
		'ZYP1': 'FirstDivision',
		'TS1': 'FortunaLigaCzechRepublic',
		'TS2': 'pass',
		'DK1': 'Superligaen',
		'DK2': 'pass',
		'GB1': 'PremierLeague',
		'GB2': 'pass',
		'GB3': 'pass',
		'FI1': 'Veikkausliiga',
		'FI2': 'pass',
		'FR1': 'Ligue1',
		'FR2': 'pass',
		'GE1N': 'CrystalbetErovnuliLiga',
		'L1': 'BundesligaGermany',
		'L2': 'pass',
		'L3': 'pass',
		'GR1': 'SuperLeague1',
		'GRS2': 'pass',
		'UNG1': 'NemzetiBajnokság',
		'IS1': 'PepsiMaxdeild',
		'IT1': 'SerieA',
		'IT2': 'pass',
		'KAS1': 'pass',
		'MO1N': 'DiviziaNationala',
		'NL1': 'Eredivisie',
		'NL2': 'pass',
		'NO1': 'Eliteserien',
		'PL1': 'PKOEkstraklasa',
		'PO1': 'LigaNOS',
		'PO2': 'pass',
		'RO1': 'Liga1',
		'RO2': 'pass',
		'RU1': 'PremierLigaRussia',
		'RU2': 'pass',
		'SC1': 'ScottishPremiership',
		'SER1': 'SuperligaSrbije',
		'SER2': 'pass',
		'SLO1': 'FortunaLigaSlovakia',
		'SL1': 'PrvaLiga',
		'ES1': 'LaLiga',
		'ES2': 'pass',
		'SE1': 'Allsvenskan',
		'SE2': 'pass',
		'C1':'SuperLeague',
		'C2':'pass',
		'TR1': 'SüperLig',
		'TR2': 'pass',
		'UKR1': 'PremierLigaUkraine',
		'UKR2': 'pass'
	}
	return switcher[code]

links = ['https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/A1',
		 'https://www.transfermarkt.com/2-liga/startseite/wettbewerb/A2',
		 'https://www.transfermarkt.com/premyer-liqasi/startseite/wettbewerb/AZ1',
		 'https://www.transfermarkt.com/primera-divisio/startseite/wettbewerb/AND1',
		 'https://www.transfermarkt.com/kategoria-superiore/startseite/wettbewerb/ALB1',
		 'https://www.transfermarkt.com/bardsragujn-chumb/startseite/wettbewerb/ARM1',
		 'https://www.transfermarkt.com/vysheyshaya-liga/startseite/wettbewerb/WER1',
		 'https://www.transfermarkt.com/pershaja-liga/startseite/wettbewerb/WER2',
		 'https://www.transfermarkt.com/jupiler-pro-league/startseite/wettbewerb/BE1',
		 'https://www.transfermarkt.com/proximus-league/startseite/wettbewerb/BE2',
		 'https://www.transfermarkt.com/premijer-liga/startseite/wettbewerb/BOS1',
		 'https://www.transfermarkt.com/efbet-liga/startseite/wettbewerb/BU1',
		 'https://www.transfermarkt.com/vtora-liga/startseite/wettbewerb/BU2',
		 'https://www.transfermarkt.com/1-hnl/startseite/wettbewerb/KR1',
		 'https://www.transfermarkt.com/2-hnl/startseite/wettbewerb/KR2',
		 'https://www.transfermarkt.com/first-division/startseite/wettbewerb/ZYP1',
		 'https://www.transfermarkt.com/fortuna-liga/startseite/wettbewerb/TS1',
		 'https://www.transfermarkt.com/fortuna-narodni-liga/startseite/wettbewerb/TS2',
		 'https://www.transfermarkt.com/superligaen/startseite/wettbewerb/DK1',
		 'https://www.transfermarkt.com/nordicbet-liga/startseite/wettbewerb/DK2',
		 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
		 'https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2',
		 'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3',
		 'https://www.transfermarkt.com/veikkausliiga/startseite/wettbewerb/FI1',
		 'https://www.transfermarkt.com/ykkonen/startseite/wettbewerb/FI2',
		 'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1',
		 'https://www.transfermarkt.com/ligue-2/startseite/wettbewerb/FR2',
		 'https://www.transfermarkt.com/crystalbet-erovnuli-liga/startseite/wettbewerb/GE1N',
		 'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1',
		 'https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2',
		 'https://www.transfermarkt.com/3-liga/startseite/wettbewerb/L3',
		 'https://www.transfermarkt.com/super-league-1/startseite/wettbewerb/GR1',
		 'https://www.transfermarkt.com/super-league-2/startseite/wettbewerb/GRS2',
		 'https://www.transfermarkt.com/nemzeti-bajnoksag/startseite/wettbewerb/UNG1',
		 'https://www.transfermarkt.com/pepsi-max-deild/startseite/wettbewerb/IS1',
		 'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
		 'https://www.transfermarkt.com/serie-b/startseite/wettbewerb/IT2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/KAS1',
		 'https://www.transfermarkt.com/divizia-nationala/startseite/wettbewerb/MO1N',
		 'https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1',
		 'https://www.transfermarkt.com/keuken-kampioen-divisie/startseite/wettbewerb/NL2',
		 'https://www.transfermarkt.com/eliteserien/startseite/wettbewerb/NO1',
		 'https://www.transfermarkt.com/pko-ekstraklasa/startseite/wettbewerb/PL1',
		 'https://www.transfermarkt.com/liga-nos/startseite/wettbewerb/PO1',
		 'https://www.transfermarkt.com/liga-pro/startseite/wettbewerb/PO2',
		 'https://www.transfermarkt.com/liga-1/startseite/wettbewerb/RO1',
		 'https://www.transfermarkt.com/liga-2/startseite/wettbewerb/RO2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1',
		 'https://www.transfermarkt.com/1-division/startseite/wettbewerb/RU2',
		 'https://www.transfermarkt.com/scottish-premiership/startseite/wettbewerb/SC1',
		 'https://www.transfermarkt.com/super-liga-srbije/startseite/wettbewerb/SER1',
		 'https://www.transfermarkt.com/prva-liga-srbije/startseite/wettbewerb/SER2',
		 'https://www.transfermarkt.com/fortuna-liga/startseite/wettbewerb/SLO1',
		 'https://www.transfermarkt.com/prva-liga/startseite/wettbewerb/SL1',
		 'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
		 'https://www.transfermarkt.com/laliga2/startseite/wettbewerb/ES2',
		 'https://www.transfermarkt.com/allsvenskan/startseite/wettbewerb/SE1',
		 'https://www.transfermarkt.com/superettan/startseite/wettbewerb/SE2',
		 'https://www.transfermarkt.com/super-league/startseite/wettbewerb/C1',
		 'https://www.transfermarkt.com/challenge-league/startseite/wettbewerb/C2',
		 'https://www.transfermarkt.com/super-lig/startseite/wettbewerb/TR1',
		 'https://www.transfermarkt.com/1-lig/startseite/wettbewerb/TR2',
		 'https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/UKR1',
		 'https://www.transfermarkt.com/persha-liga/startseite/wettbewerb/UKR2']

def get_links():
	return links

def get_season(season):
	tokens = season.split("/")
	if len(tokens) == 1:
		return "" + str((int(tokens[0]) - 1)) + "/" + tokens[0]

	if int(tokens[0]) <= 20 and int(tokens[0]) >= 0:
		if len(tokens[0]) == 2:
			tokens[0] = "20" + tokens[0]
	else:
		if len(tokens[0]) == 2:
			tokens[0] = "19" + tokens[0]

	if int(tokens[1]) <= 20 and int(tokens[1]) >= 0 and tokens[0][0] != "1":
		if len(tokens[1]) == 2:
			tokens[1] = "20" + tokens[1]
	else:
		if len(tokens[1]) == 2:
			tokens[1] = "19" + tokens[1]

	return tokens[0] + "/" + tokens[1]

def get_list_(input_table, column_name):
	df = pd.read_csv(input_table)
	return df[column_name].tolist()
# import pandas as pd

# input_table = "championship_winners.csv"
# output_table = "championship_winners1.csv"

# df = pd.read_csv(input_table)
# df.drop(df.columns[0], axis = 1, inplace = True)

# for index, row in df.iterrows():
# 	if row[3] == 'Austria' and row[2][:10] == "Bundesliga":
# 		df.at[index, 'Championship'] = "BundesligaAustria" + row[2][10:]
# 	if row[3] == 'Germany' and row[2][:10] == "Bundesliga":
# 		df.at[index, 'Championship'] = "BundesligaGermany" + row[2][10:]
# 	if row[3] == 'Russia' and row[2][:11] == "PremierLiga":
# 		df.at[index, 'Championship'] = "PremierLigaRussia" + row[2][11:]
# 	if row[3] == 'Ukraine' and row[2][:11] == "PremierLiga":
# 		df.at[index, 'Championship'] = "PremierLigaUkraine" + row[2][11:]
# 	if row[3] == 'Slovakia' and row[2][:11] == "FortunaLiga":
# 		df.at[index, 'Championship'] = "FortunaLigaSlovakia" + row[2][11:]
# 	if row[3] == 'Czech Republic' and row[2][:11] == "FortunaLiga":
# 		df.at[index, 'Championship'] = "FortunaLigaCzechRepublic" + row[2][11:]

# with open(output_table, 'w', encoding='utf-8') as f:
# 	df.to_csv(f)

import sys
sys.path.append('../../../helpers')
from helpers import write_csv

tournaments = []
stadiums = []
cities = []
countries = []

tournaments.append('UEFAChampionsLeague_2003/2004')
stadiums.append('Veltins-Arena')
cities.append('Gelsenkirchen')
countries.append('Germany')

tournaments.append('UEFAChampionsLeague_2004/2005')
stadiums.append('Atatürk Olympic Stadium')
cities.append('Istanbul')
countries.append('Turkey')

tournaments.append('UEFAChampionsLeague_2005/2006')
stadiums.append('Stade de France')
cities.append('Paris')
countries.append('France')

tournaments.append('UEFAChampionsLeague_2006/2007')
stadiums.append('Olympiako Stadio Athinon')
cities.append('Athena')
countries.append('Greece')

tournaments.append('UEFAChampionsLeague_2007/2008')
stadiums.append('Luzhniki Stadium')
cities.append('Moscow')
countries.append('Russia')

tournaments.append('UEFAChampionsLeague_2008/2009')
stadiums.append('Olimpico di Roma')
cities.append('Roma')
countries.append('Italy')

tournaments.append('UEFAChampionsLeague_2009/2010')
stadiums.append('Santiago Bernabéu')
cities.append('Madrid')
countries.append('Spain')

tournaments.append('UEFAChampionsLeague_2010/2011')
stadiums.append('Wembley Stadium')
cities.append('Londra')
countries.append('England')

tournaments.append('UEFAChampionsLeague_2011/2012')
stadiums.append('Allianz Arena')
cities.append('Munich')
countries.append('Germany')

tournaments.append('UEFAChampionsLeague_2012/2013')
stadiums.append('Wembley Stadium')
cities.append('Londra')
countries.append('England')

tournaments.append('UEFAChampionsLeague_2013/2014')
stadiums.append('Estádio da Luz')
cities.append('Lisbon')
countries.append('Portugal')

tournaments.append('UEFAChampionsLeague_2014/2015')
stadiums.append('Olympiastadion Berlin')
cities.append('Berlin')
countries.append('Germany')

tournaments.append('UEFAChampionsLeague_2015/2016')
stadiums.append('Giuseppe Meazza')
cities.append('Milano')
countries.append('Italy')

tournaments.append('UEFAChampionsLeague_2016/2017')
stadiums.append('Millennium Stadium')
cities.append('Cardiff')
countries.append('Wales')

tournaments.append('UEFAChampionsLeague_2017/2018')
stadiums.append('NSK Olimpisky')
cities.append('Kiev')
countries.append('Russia')

tournaments.append('UEFAChampionsLeague_2018/2019')
stadiums.append('Wanda Metropolitano')
cities.append('Madrid')
countries.append('Spain')

tournaments.append('UEFA-Cup_2004/2005')
stadiums.append('Estádio José Alvalade')
cities.append('Lisbon')
countries.append('Portugal')

tournaments.append('UEFA-Cup_2005/2006')
stadiums.append('Philips Stadion')
cities.append('Eindhoven')
countries.append('Netherlands')

tournaments.append('UEFA-Cup_2006/2007')
stadiums.append('Hampden Park')
cities.append('Glasgow')
countries.append('Scotland')

tournaments.append('UEFA-Cup_2007/2008')
stadiums.append('Etihad Stadium')
cities.append('Manchester')
countries.append('England')

tournaments.append('UEFA-Cup_2008/2009')
stadiums.append('Ülker Stadyumu FB Şükrü Saraçoğlu Spor Kompleksi')
cities.append('Istanbul')
countries.append('Turkey')

tournaments.append('EuropaLeague_2009/2010')
stadiums.append('Volksparkstadion')
cities.append('Hamburg')
countries.append('Germany')

tournaments.append('EuropaLeague_2010/2011')
stadiums.append('Aviva Stadium')
cities.append('Dublin')
countries.append('Ireland')

tournaments.append('EuropaLeague_2011/2012')
stadiums.append('National Arena')
cities.append('Bucharest')
countries.append('Romania')

tournaments.append('EuropaLeague_2012/2013')
stadiums.append('Johan Cruijff ArenA')
cities.append('Amsterdam')
countries.append('Netherlands')

tournaments.append('EuropaLeague_2013/2014')
stadiums.append('Allianz Stadium')
cities.append('Turin')
countries.append('Italy')

tournaments.append('EuropaLeague_2014/2015')
stadiums.append('PGE Narodowy')
cities.append('Warsaw')
countries.append('Poland')

tournaments.append('EuropaLeague_2015/2016')
stadiums.append('St. Jakob-Park')
cities.append('Basel')
countries.append('Switzerland')

tournaments.append('EuropaLeague_2016/2017')
stadiums.append('Friends Arena')
cities.append('Stockholm')
countries.append('Sweden')

tournaments.append('EuropaLeague_2017/2018')
stadiums.append('Groupama Stadium')
cities.append('Lyon')
countries.append('France')

tournaments.append('EuropaLeague_2018/2019')
stadiums.append('Baku Olympic Stadium')
cities.append('Baku')
countries.append('Azerbaijan')

cols_name = ['Tournament', 'Stadium', 'City', 'Country']
cols = [tournaments, stadiums, cities, countries]
write_csv('finals_stadiums.csv', cols_name, cols)



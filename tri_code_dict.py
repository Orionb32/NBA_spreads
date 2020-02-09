def create_team_conversion():
	team_conversion = dict({
		'Denver Nuggets':'DEN',
		'New York Knicks':'NYK',
		'Houston Rockets':'HOU',
    	'Phoenix Suns':'PHO',
    	'Oklahoma City Thunder':'OKC', 
    	'San Antonio Spurs':'SAS',
    	'Golden State Warriors':'GSW', 
    	'Miami Heat':'MIA',
    	'Los Angeles Lakers':'LAL',
    	'Minnesota Timberwolves':'MIN',
    	'Dallas Mavericks':'DAL',
    	'Memphis Grizzlies':'MEM',
    	'Indiana Pacers':'IND',
    	'Utah Jazz':'UTA',
    	'Sacramento Kings':'SAC',
    	'Orlando Magic':'ORL',
    	'Toronto Raptors':'TOR',
    	'Philadelphia 76ers':'PHI',
    	'Los Angeles Clippers':'LAC',
    	'Chicago Bulls':'CHI',
    	'Washington Wizards':'WAS',
    	'Detroit Pistons':'DET',
    	'Boston Celtics':'BOS',
    	'Portland Trail Blazers':'POR',
    	'Cleveland Cavaliers':'CLE',
    	'Atlanta Hawks':'ATL',
    	'New Orleans Hornets':'NOH',
    	'New Jersey Nets':'NJN',
    	'Charlotte Bobcats':'CHA',
    	'Milwaukee Bucks':'MIL',
    	'Brooklyn Nets':'BRK',
    	'New Orleans Pelicans':'NOP',
    	'Charlotte Hornets':'CHO',
		})
	return team_conversion

def create_tri_code_list():
	tri = ['DEN', 'NOH', 'HOU', 'DAL', 'CHI', 'IND', 'PHO', 'POR', 'GSW',
		'CHA', 'BOS', 'TOR', 'NYK', 'SAS', 'OKC', 'MIN', 'LAC', 'SAC',
		'WAS', 'DET', 'CLE', 'PHI', 'NJN', 'MEM', 'MIL', 'UTA', 'ATL',
		'ORL', 'MIA', 'LAL', 'BRK', 'NOP', 'CHO']
	return tri

def create_teams_list():
	teams = ['Denver Nuggets', 'New York Knicks', 'Houston Rockets',
    	'Phoenix Suns', 'Oklahoma City Thunder', 'San Antonio Spurs',
    	'Golden State Warriors', 'Miami Heat', 'Los Angeles Lakers',
    	'Minnesota Timberwolves', 'Dallas Mavericks', 'Memphis Grizzlies',
    	'Indiana Pacers', 'Utah Jazz', 'Sacramento Kings', 'Orlando Magic',
    	'Toronto Raptors', 'Philadelphia 76ers', 'Los Angeles Clippers',
    	'Chicago Bulls', 'Washington Wizards', 'Detroit Pistons',
    	'Boston Celtics', 'Portland Trail Blazers', 'Cleveland Cavaliers',
    	'Atlanta Hawks', 'New Orleans Hornets', 'New Jersey Nets',
    	'Charlotte Bobcats', 'Milwaukee Bucks', 'Brooklyn Nets',
    	'New Orleans Pelicans', 'Charlotte Hornets']
	return teams


def create_arena_dict():
	arena_dict = dict({'ATL':'State Farm Arena, Atlanta, Georgia',
		'BOS':'TD Garden, Boston, Massachusetts',
		'BRK':'Barclays Center, Brooklyn, New York',
		'CHO':'Spectrum Center, Charlotte, North Carolina',
		'CHI':'United Center, Chicago, Illinois',
		'CLE':'Quicken Loans Arena, Cleveland, Ohio',
		'DAL':'American Airlines Center, Dallas, Texas',
		'DEN':'Pepsi Center, Denver, Colorado',
		'DET':"Little Caesars Arena, Detroit, Michigan",
		'GSW':'Chase Center, San Francisco, California',
		'HOU':'Toyota Center, Houston, Texas',
		'IND':'Bankers Life Fieldhouse, Indianapolis, Indiana',
		'LAC':'STAPLES Center, Los Angeles, California',
		'LAL':'STAPLES Center, Los Angeles, California',
		'MEM':'FedEx Forum, Memphis, Tennessee',
		'MIA':'AmericanAirlines Arena, Miami, Florida',
		'MIL':'Fiserv Forum, Milwaukee, Wisconsin',
		'MIN':'Target Center, Minneapolis, Minnesota',
		'NOP':'Smoothie King Center, New Orleans, Louisiana',
		'NYK':'Madison Square Garden (IV), New York, New York',
		'OKC':'Chesapeake Energy Arena, Oklahoma City, Oklahoma',
		'ORL':'Amway Center, Orlando, Florida',
		'PHI':'Wells Fargo Center, Philadelphia, Pennsylvania',
		'PHO':'Talking Stick Resort Arena, Phoenix, Arizona',
		'POR':'Moda Center, Portland, Oregon',
		'SAC':'Golden 1 Center, Sacramento, California',
		'SAS':'AT&T Center, San Antonio, Texas',
		'TOR':'Scotiabank Arena, Toronto, Canada',
		'UTA':'Vivint Smart Home Arena, Salt Lake City, Utah',
		'WAS':'Capital One Arena, Washington, District of Columbia'})
	return arena_dict







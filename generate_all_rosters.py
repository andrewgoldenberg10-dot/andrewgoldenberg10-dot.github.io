import json
from basketball_reference_web_scraper import client

def build_historical_rosters(start_year, end_year):
    print(f"🏀 Starting historical roster compilation from {start_year} to {end_year}...")
    all_teams_data = []

    # Map raw team tokens to clean, readable display names
    team_name_mapping = {
        'ATLANTA_HAWKS': 'Atlanta Hawks', 'BOSTON_CELTICS': 'Boston Celtics',
        'BROOKLYN_NETS': 'Brooklyn Nets', 'CHARLOTTE_HORNETS': 'Charlotte Hornets',
        'CHICAGO_BULLS': 'Chicago Bulls', 'CLEVELAND_CAVALIERS': 'Cleveland Cavaliers',
        'DALLAS_MAVERICKS': 'Dallas Mavericks', 'DENVER_NUGGETS': 'Denver Nuggets',
        'DETROIT_PISTONS': 'Detroit Pistons', 'GOLDEN_STATE_WARRIORS': 'Golden State Warriors',
        'HOUSTON_ROCKETS': 'Houston Rockets', 'INDIANA_PACERS': 'Indiana Pacers',
        'LOS_ANGELES_CLIPPERS': 'LA Clippers', 'LOS_ANGELES_LAKERS': 'Los Angeles Lakers',
        'MEMPHIS_GRIZZLIES': 'Memphis Grizzlies', 'MIAMI_HEAT': 'Miami Heat',
        'MILWAUKEE_BUCKS': 'Milwaukee Bucks', 'MINNESOTA_TIMBERWOLVES': 'Minnesota Timberwolves',
        'NEW_ORLEANS_PELICANS': 'New Orleans Pelicans', 'NEW_YORK_KNICKS': 'New York Knicks',
        'OKLAHOMA_CITY_THUNDER': 'Oklahoma City Thunder', 'ORLANDO_MAGIC': 'Orlando Magic',
        'PHILADELPHIA_76ERS': 'Philadelphia 76ers', 'PHOENIX_SUNS': 'Phoenix Suns',
        'PORTLAND_TRAIL_BLAZERS': 'Portland Trail Blazers', 'SACRAMENTO_KINGS': 'Sacramento Kings',
        'SAN_ANTONIO_SPURS': 'San Antonio Spurs', 'TORONTO_RAPTORS': 'Toronto Raptors',
        'UTAH_JAZZ': 'Utah Jazz', 'WASHINGTON_WIZARDS': 'Washington Wizards'
    }

    # Loop through each season
    for year in range(start_year, end_year + 1):
        print(f"Fetching season data for year ending in {year}...")
        try:
            # Pull player season totals which contain their team assignments
            player_stats = client.players_season_totals(season_end_year=year)
            
            # Temporary dictionary to group players by their team for this specific year
            season_teams = {}

            for record in player_stats:
                player_name = record['name']
                team_enum = record['team']
                
                if not team_enum:
                    continue
                
                team_key = team_enum.name
                clean_team_name = team_name_mapping.get(team_key, team_key.replace('_', ' ').title())

                if clean_team_name not in season_teams:
                    season_teams[clean_team_name] = set()
                
                # Add player to team roster set (avoids internal duplicates)
                season_teams[clean_team_name].add(player_name)

            # Format the grouped teams into your game's structural JSON layout
            for team_name, roster_set in season_teams.items():
                roster_list = list(roster_set)
                
                # Filter out small mid-season code irregularities or empty squads
                if len(roster_list) >= 8:
                    team_id = f"{team_name.lower().replace(' ', '_')}_{year}"
                    all_teams_data.append({
                        "id": team_id,
                        "year": str(year),
                        "name": team_name,
                        "roster": sorted(roster_list) # Alphabetical sorting for clean presentation
                    })

        except Exception as e:
            print(f"⚠️ Skipped year {year} due to an error: {e}")

    # Write the entire global database array directly to your project file
    output_filename = "./nba_historical_rosters.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_teams_data, f, indent=2, ensure_ascii=False)

    print(f"🎯 Complete! Saved {len(all_teams_data)} total historical team rosters to '{output_filename}'.")

if __name__ == "__main__":
    # Pulling iconic recent decades (e.g., 2010 through 2026 inclusive)
    build_historical_rosters(start_year=1960, end_year=2026)

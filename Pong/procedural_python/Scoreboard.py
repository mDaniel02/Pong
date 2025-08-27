import csv
import os

class Scoreboard:
    def save (player):
        found = False
        filename = "Scoreboard.csv"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, filename)
        if not os.path.exists(filename):
            with open(filename, "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Game", "Wins"])
            with open(filename, "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow([player.Name, player.Game,player.Wins])
        else:
            rows = []
            with open(filename, "r", newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
                    for row in rows:
                        if row["Name"] == player.Name and row["Game"] == player.Game:
                            found = True
                            row["Wins"] = player.Wins
                            break
            if not found:
                rows.append({
                    "Name": player.Name,
                    "Game": player.Game,
                    "Wins": player.Wins,
                })
        
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Name", "Game", "Wins"])
                writer.writeheader()
                writer.writerows(rows)

    def getStats(playerName, Game):
        filename = "Scoreboard.csv"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, filename)
        found = False
        if not os.path.exists(filename):
            with open(filename, "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Game",  "Wins"])
            with open(filename, "a", newline = "") as file:
                writer = csv.writer(file)
                writer.writerow([playerName, Game, 0])
        else:
            rows = []
            stats = []
            with open(filename, "r", newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
                    for row in rows:
                        if row["Name"] == playerName and row["Game"] == Game:
                            found = True
                            stats.append({
                            "Wins": row["Wins"]
                            })
                            # Wins = row["Wins"]
                            # Number_of_games = row["Number of games"]
                            # Record = row["Record"]
                            # return (Wins, Number_of_games, Record)
                            print(stats)
            if not found:
                return ("Player not found in Database!")
    


class Player:
    def __init__(self, Name, Game, Wins ):
        self.Name = Name
        self.Game = Game
        self.Wins = Wins


filepath = 'stats.csv'
class PlayerLists:
    def read_game_results(filepath):
        player1_list = []
        player2_list = []

        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row)  < 5:
                    continue
                try:
                    name1 = row[0].strip('["]')
                    win1 = int(row[1])
                    name2 = row[2].strip('["]')
                    win2 = int(row[3])
                    game = row[4].strip('[["''"]]')

                    player1_list.append(name1)
                    player1_list.append(win1)
                    player1_list.append(game)
                    player2_list.append(name2)
                    player2_list.append(win2)
                    player2_list.append(game)
                except Exception as e:
                    print(f"Error {e}")
                    continue
            return player1_list, player2_list


#player1_list, player2_list = PlayerLists.read_game_results('stats.csv')   

#print(player1_list)
#print(player2_list)

#p1 = Player(player1_list[0],player1_list[2], player1_list[1])
#Scoreboard.save(p1)

#p2 = Player(player2_list[0],player2_list[2], player2_list[1])
#Scoreboard.save(p2)

#p2 = Player(player1_list[2],player1_list[2], player1_list[1])
#Scoreboard.save(p2)


stats = Scoreboard.getStats('Spieler1', 'Pong')
print(stats)
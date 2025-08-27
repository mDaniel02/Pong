import os
import csv
import tkinter as tk
from tkinter import ttk

class GameStatsManager:
    def __init__(self, filename="scoreboard.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(['player', 'game', 'wins']) 

    def update_stats(self, input_data):
        player_name, win_count, game_name = input_data

        updated = False
        records = []

        with open(self.filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Normalize for comparison
                if row['player'].strip().lower() == player_name.strip().lower() and \
                   row['game'].strip().lower() == game_name.strip().lower():
                    new_wins = int(row['wins']) + win_count
                    records.append({
                        'player': player_name.strip(), 
                        'game': game_name.strip(), 
                        'wins': str(new_wins)
                    })
                    updated = True
                else:
                    records.append(row)

        # If no matching record, add new one
        if not updated:
            records.append({
                'player': player_name.strip(), 
                'game': game_name.strip(), 
                'wins': str(win_count)
            })

        # Write all records back
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['player', 'game', 'wins']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"Stats updated for {player_name} in {game_name}")

    def print_all_stats(self):
        print("Player Stats by Game")
        with open(self.filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['player']} - {row['game']} : {row['wins']} wins")
    def get_all_stats(self):
        stats = []
        with open(self.filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stats.append(row)
        return stats


stats = GameStatsManager()

#stats.print_all_stats()


class GameStatGui:
    def __init__(self, root, stat_manager):
        self.root = root
        self.root.title("Game Stats")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.stat_manager = stat_manager

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11))
        style.configure("TCombobox", font=("Segoe UI", 11))
        style.configure("TEntry", font=("Segoe UI", 11))

        # Main container
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.label = ttk.Label(self.frame, text="Game Stats", font=("Segoe UI", 18, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Filters Section
        self.filters_frame = ttk.LabelFrame(self.frame, text="Filters", padding=15)
        self.filters_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20), rowspan=2)

        # Game Filter
        ttk.Label(self.filters_frame, text="Game:").grid(row=0, column=0, sticky="w", pady=5)
        self.dropdown_game_var = tk.StringVar()
        self.dropdown_game = ttk.Combobox(self.filters_frame, textvariable=self.dropdown_game_var, state="readonly")
        self.dropdown_game.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.dropdown_game.bind("<<ComboboxSelected>>", self.on_filter_changed)

        # Player Search
        ttk.Label(self.filters_frame, text="Search Player:").grid(row=2, column=0, sticky="w", pady=5)
        self.search_player_var = tk.StringVar()
        self.search_player_var.trace_add("write", lambda *args: self.load_stats())
        self.entry_player_search = ttk.Entry(self.filters_frame, textvariable=self.search_player_var)
        self.entry_player_search.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # Sort Filter
        ttk.Label(self.filters_frame, text="Sort by:").grid(row=4, column=0, sticky="w", pady=5)
        self.dropdown_sort_var = tk.StringVar()
        self.dropdown_sort = ttk.Combobox(self.filters_frame, textvariable=self.dropdown_sort_var, state="readonly")
        self.dropdown_sort["values"] = ["Default", "Most Wins", "Least Wins"]
        self.dropdown_sort.current(0)
        self.dropdown_sort.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        self.dropdown_sort.bind("<<ComboboxSelected>>", self.on_filter_changed)

        # Refresh Button
        self.refresh_button = ttk.Button(self.filters_frame, text="Refresh Stats", command=self.refresh_filters)
        self.refresh_button.grid(row=6, column=0, pady=(10, 0), sticky="ew")

        # Stats Display Section
        self.stats_frame = ttk.Frame(self.frame)
        self.stats_frame.grid(row=1, column=1, sticky="nsew")

        self.listbox = tk.Listbox(self.stats_frame, font=("Consolas", 11), width=60, height=25)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.stats_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Expand layout configuration
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.refresh_filters()

    def refresh_filters(self):
        """Populate game dropdown and refresh stats"""
        self.populate_game_filter()
        self.load_stats()

    def populate_game_filter(self):
        stats = self.stat_manager.get_all_stats()
        game_names = sorted(set(row["game"] for row in stats))
        game_names.insert(0, "All Games")
        self.dropdown_game["values"] = game_names
        self.dropdown_game.current(0)

    def load_stats(self):
        self.listbox.delete(0, tk.END)
        stats = self.stat_manager.get_all_stats()

        selected_game = self.dropdown_game_var.get()
        search_player = self.search_player_var.get().lower()
        sort_order = self.dropdown_sort_var.get()

        # Apply filters
        filtered_stats = []
        for row in stats:
            if selected_game != "All Games" and row["game"] != selected_game:
                continue
            if search_player and search_player not in row["player"].lower():
                continue
            filtered_stats.append(row)

        # Sort by wins
        if sort_order == "Most Wins":
            filtered_stats.sort(key=lambda x: int(x["wins"]), reverse=True)
        elif sort_order == "Least Wins":
            filtered_stats.sort(key=lambda x: int(x["wins"]))

        for row in filtered_stats:
            display = f"{row['player']:20} | {row['game']:20} | {row['wins']} wins"
            self.listbox.insert(tk.END, display)

    def on_filter_changed(self, event):
        self.load_stats()


if __name__ == "__main__":
    root = tk.Tk()
    maanger = GameStatsManager()
    gui =  GameStatGui(root, maanger)
    root.mainloop()

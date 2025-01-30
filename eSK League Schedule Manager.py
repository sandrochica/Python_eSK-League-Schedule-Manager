import tkinter as tk
from tkinter import scrolledtext

class RoundRobinManager:
    def __init__(self):
        self.teams = []

    def add_team(self, team_name):
        if team_name and team_name not in self.teams:
            self.teams.append(team_name)
            return f'Team "{team_name}" added successfully!'
        return f'Team "{team_name}" already exists or invalid name.'

    def update_team(self, index, new_name):
        if 0 <= index < len(self.teams) and new_name:
            old_name = self.teams[index]
            self.teams[index] = new_name
            return f'Team "{old_name}" updated to "{new_name}".'
        return "Invalid index or name."

    def delete_team(self, index):
        if 0 <= index < len(self.teams):
            removed_team = self.teams.pop(index)
            return f'Team "{removed_team}" deleted successfully!'
        return "Invalid index."

    def generate_schedule(self):
        if len(self.teams) < 3:
            return "Not enough teams to generate a schedule. Minimum 3 teams required."
        if len(self.teams) > 10:
            return "Too many teams. Maximum 10 teams allowed."

        num_teams = len(self.teams)
        if num_teams % 2 != 0:
            self.teams.append("Bye")  # Add a dummy team for odd number of teams

        rounds = []
        teams = self.teams[:]
        num_rounds = len(teams) - 1
        num_matches_per_round = len(teams) // 2

        for round_num in range(num_rounds):
            round_matches = []
            for match_num in range(num_matches_per_round):
                team1 = teams[match_num]
                team2 = teams[-(match_num + 1)]
                if "Bye" not in (team1, team2):
                    round_matches.append(f"{team1} vs {team2}")
            rounds.append(f"Round {round_num + 1}:\n" + "\n".join(round_matches))
            teams.insert(1, teams.pop())  # Rotate teams

        self.teams = [team for team in self.teams if team != "Bye"]  # Remove dummy team if added
        return "\n\n".join(rounds)

# GUI Setup
manager = RoundRobinManager()

root = tk.Tk()
root.title("eSK-League Schedule Manager")
root.geometry("600x600")

# Floating Message UI for Success and Error
def show_floating_message(message, is_error=False):
    message_frame = tk.Frame(root, bg="red" if is_error else "green", bd=2, relief=tk.SOLID)
    message_label = tk.Label(message_frame, text=message, bg="red" if is_error else "green", fg="white", font=("Arial", 12))
    message_label.pack(padx=20, pady=10)
    
    # Place the message in the top-right corner
    message_frame.place(relx=1.0, rely=0.1, anchor="ne")
    
    # Automatically hide the message after 3 seconds
    root.after(3000, message_frame.destroy)

# Error Message Box in the Center
def show_center_error_message(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("400x200")
    
    # Center the window on the screen
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    
    error_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
    # Error Message and OK button
    label = tk.Label(error_window, text=message, font=("Arial", 12), fg="red", wraplength=350, justify="center")
    label.pack(pady=20)

    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)

    error_window.mainloop()

# Functions
def add_team():
    team_name = team_entry.get()
    message = manager.add_team(team_name)
    show_floating_message(message, is_error=False if "added successfully" in message else True)
    update_team_list()
    team_entry.delete(0, tk.END)

def update_team():
    try:
        index = int(update_index_entry.get()) - 1
        new_name = update_name_entry.get()
        message = manager.update_team(index, new_name)
        show_floating_message(message, is_error=False if "updated" in message else True)
        update_team_list()
    except ValueError:
        show_floating_message("Invalid index. Please enter a valid number.", is_error=True)

def delete_team():
    try:
        index = int(delete_index_entry.get()) - 1
        message = manager.delete_team(index)
        show_floating_message(message, is_error=False if "deleted successfully" in message else True)
        update_team_list()
    except ValueError:
        show_floating_message("Invalid index. Please enter a valid number.", is_error=True)

def generate_schedule():
    schedule = manager.generate_schedule()
    if "Not enough teams" in schedule:
        show_center_error_message(schedule)
    elif "Too many teams" in schedule:
        show_center_error_message(schedule)
    else:
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, schedule)
        display_text.tag_add("center", 1.0, "end")

def update_team_list():
    team_list_label.config(text="\n".join(f"{i + 1}. {team}" for i, team in enumerate(manager.teams)))

# Header Section with customized colors for 'S' and 'K'
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

header_text = tk.Label(header_frame, text="e", font=("Arial", 18, "bold"), fg="black")
header_text.pack(side=tk.LEFT)

header_text_s = tk.Label(header_frame, text="S", font=("Arial", 18, "bold"), fg="blue")
header_text_s.pack(side=tk.LEFT)

header_text_k = tk.Label(header_frame, text="K", font=("Arial", 18, "bold"), fg="red")
header_text_k.pack(side=tk.LEFT)

header_text_rest = tk.Label(header_frame, text="-League Schedule Manager", font=("Arial", 18, "bold"), fg="black")
header_text_rest.pack(side=tk.LEFT)

# Add Team Section
add_frame = tk.Frame(root)
add_frame.pack(pady=10)

team_entry = tk.Entry(add_frame, width=30)
team_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(add_frame, text="Add Team", command=add_team)
add_button.pack(side=tk.LEFT, padx=5)

# Update Team Section
update_frame = tk.Frame(root)
update_frame.pack(pady=10)

update_index_entry = tk.Entry(update_frame, width=5)
update_index_entry.pack(side=tk.LEFT, padx=5)
update_index_entry.insert(0, "Index")

update_name_entry = tk.Entry(update_frame, width=20)
update_name_entry.pack(side=tk.LEFT, padx=5)
update_name_entry.insert(0, "New Name")

update_button = tk.Button(update_frame, text="Update Team", command=update_team)
update_button.pack(side=tk.LEFT, padx=5)

# Delete Team Section
delete_frame = tk.Frame(root)
delete_frame.pack(pady=10)

delete_index_entry = tk.Entry(delete_frame, width=5)
delete_index_entry.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(delete_frame, text="Delete Team", command=delete_team)
delete_button.pack(side=tk.LEFT, padx=5)

# Generate Schedule Button
generate_button = tk.Button(root, text="Generate Schedule", command=generate_schedule)
generate_button.pack(pady=10)

# Team List Label
team_list_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT, anchor="w", wraplength=500)
team_list_label.pack(pady=10)

# Scrollable Display Text
scroll_frame = tk.Frame(root)
scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

display_text = scrolledtext.ScrolledText(scroll_frame, font=("Arial", 12), wrap=tk.WORD, yscrollcommand=scrollbar.set, height=15, width=70)
display_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor="center")

scrollbar.config(command=display_text.yview)

display_text.tag_configure("center", justify="center")

root.mainloop()
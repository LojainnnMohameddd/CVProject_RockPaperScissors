import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import Counter
import csv
import threading

# Import your logic module (make sure GameLogic.py is in same folder)
from GameLogic import play_round
from simulate import simulate_n_rounds  # uses the simulate we wrote

# Optional plotting (simulate button will call plot if available)
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False


class RPSGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock - Paper - Scissors — Simulation & GUI")
        self.root.geometry("820x520")
        self.root.minsize(760, 460)

        # --- style (ttk) ---
        self.style = ttk.Style()
        # Use default theme and tweak
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("TFrame", background="#f0f7fb")
        self.style.configure("TLabel", background="#f0f7fb", font=("Helvetica", 11))
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#f0f7fb")
        self.style.configure("Outcome.TLabel", font=("Helvetica", 13, "bold"), background="#f0f7fb")
        self.style.configure("Big.TButton", font=("Helvetica", 12, "bold"), padding=8)
        self.style.configure("Small.TButton", font=("Helvetica", 10), padding=6)

        # main layout frames
        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        # Left: Controls & Scoreboard
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0, 8))

        # Right: Result display & history
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self._build_left()
        self._build_right()

        # game state
        self.scores = Counter({"player": 0, "computer": 0, "draw": 0})
        self.history = []  # list of tuples (player_move, comp_move, result)

        self._update_scoreboard()
        self._update_history_display()

    def _build_left(self):
        # Title
        ttk.Label(self.left_frame, text="Rock · Paper · Scissors", style="Header.TLabel").pack(pady=(2, 12))

        # Buttons for player move
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(pady=(0, 8), fill="x")

        # Buttons with icons-style text
        self.rock_btn = ttk.Button(btn_frame, text="🪨 Rock", style="Big.TButton", command=lambda: self._on_player_move("rock"))
        self.paper_btn = ttk.Button(btn_frame, text="📄 Paper", style="Big.TButton", command=lambda: self._on_player_move("paper"))
        self.scissors_btn = ttk.Button(btn_frame, text="✂️ Scissors", style="Big.TButton", command=lambda: self._on_player_move("scissors"))

        self.rock_btn.grid(row=0, column=0, padx=4, pady=6, sticky="ew")
        self.paper_btn.grid(row=0, column=1, padx=4, pady=6, sticky="ew")
        self.scissors_btn.grid(row=0, column=2, padx=4, pady=6, sticky="ew")

        for i in range(3):
            btn_frame.columnconfigure(i, weight=1)

        # Scoreboard
        score_frame = ttk.LabelFrame(self.left_frame, text="Scoreboard", padding=8)
        score_frame.pack(fill="x", pady=(10, 12))

        self.player_score_lbl = ttk.Label(score_frame, text="Player: 0", style="Outcome.TLabel")
        self.comp_score_lbl = ttk.Label(score_frame, text="Computer: 0", style="Outcome.TLabel")
        self.draw_score_lbl = ttk.Label(score_frame, text="Draws: 0", style="Outcome.TLabel")

        self.player_score_lbl.pack(anchor="w", pady=2)
        self.comp_score_lbl.pack(anchor="w", pady=2)
        self.draw_score_lbl.pack(anchor="w", pady=2)

        # Controls (simulate, reset, export)
        ctrl_frame = ttk.LabelFrame(self.left_frame, text="Actions", padding=8)
        ctrl_frame.pack(fill="x", pady=(0, 12))

        # simulate N rounds entry + button
        sim_row = ttk.Frame(ctrl_frame)
        sim_row.pack(fill="x", pady=(4, 6))
        ttk.Label(sim_row, text="Simulate N rounds:").pack(side="left")
        self.sim_entry = ttk.Entry(sim_row, width=8)
        self.sim_entry.insert(0, "500")
        self.sim_entry.pack(side="left", padx=6)
        self.sim_btn = ttk.Button(sim_row, text="Run", style="Small.TButton", command=self._on_simulate_click)
        self.sim_btn.pack(side="left")

        # Reset & export
        btns_row = ttk.Frame(ctrl_frame)
        btns_row.pack(fill="x", pady=(6, 0))
        self.reset_btn = ttk.Button(btns_row, text="Reset Scores", style="Small.TButton", command=self._reset_scores)
        self.reset_btn.pack(side="left", padx=(0,6))
        self.export_btn = ttk.Button(btns_row, text="Export CSV", style="Small.TButton", command=self._export_csv)
        self.export_btn.pack(side="left")

        # Help / quick tips
        tips = ("Tips:\n- Click a move to play one round.\n"
                "- Use simulate to run many rounds quickly.\n"
                "- Export CSV for submission.")
        ttk.Label(self.left_frame, text=tips, wraplength=220, font=("Helvetica", 9)).pack(pady=(6, 0))

    def _build_right(self):
        # Last result panel
        last_frame = ttk.LabelFrame(self.right_frame, text="Last Result", padding=10)
        last_frame.pack(fill="x", pady=(0, 8))

        self.last_result_lbl = ttk.Label(last_frame, text="No rounds yet.", font=("Helvetica", 12))
        self.last_result_lbl.pack(anchor="w")

        # History box
        history_frame = ttk.LabelFrame(self.right_frame, text="History (latest first)", padding=8)
        history_frame.pack(fill="both", expand=True)

        self.history_txt = tk.Text(history_frame, height=12, wrap="none", state="disabled", background="#ffffff")
        self.history_txt.pack(fill="both", expand=True)

        # Make history scrollable
        scroll_y = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_txt.yview)
        self.history_txt['yscrollcommand'] = scroll_y.set
        scroll_y.pack(side="right", fill="y")

    # --- core actions ---
    def _on_player_move(self, move: str):
        """Called when player presses Rock/Paper/Scissors."""
        try:
            p_move, c_move, result = play_round(move)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # update state
        self.scores[result] += 1
        self.history.insert(0, (p_move, c_move, result))
        self._update_scoreboard()
        self._set_last_result(p_move, c_move, result)
        self._update_history_display()

    def _on_simulate_click(self):
        """Run simulation in background thread to avoid freezing the GUI."""
        val = self.sim_entry.get().strip()
        try:
            n = int(val)
            if n <= 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Invalid number", "Enter a positive integer for rounds.")
            return

        # disable button while running
        self.sim_btn.config(state="disabled")
        self.sim_entry.config(state="disabled")

        # run in thread
        thread = threading.Thread(target=self._run_simulation_thread, args=(n,), daemon=True)
        thread.start()

    def _run_simulation_thread(self, n_rounds):
        """Background worker: runs simulate_n_rounds and updates GUI when done."""
        try:
            stats = simulate_n_rounds(n_rounds, player_strategy="random")
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Simulation error", str(e)))
            self.root.after(0, lambda: self._sim_done())
            return

        # update scoreboard and history with aggregated result
        # We'll just add aggregated counts into current scoreboard to keep it simple
        self.scores["player"] += stats["results"].get("player", 0)
        self.scores["computer"] += stats["results"].get("computer", 0)
        self.scores["draw"] += stats["results"].get("draw", 0)

        # Prepend a single summary line to history
        summary_line = (f"SIM {n_rounds} rounds -> "
                        f"P:{stats['results'].get('player',0)} "
                        f"C:{stats['results'].get('computer',0)} "
                        f"D:{stats['results'].get('draw',0)}")
        self.history.insert(0, ("SIM", "", summary_line))

        # refresh UI on main thread
        self.root.after(0, self._update_scoreboard)
        self.root.after(0, self._update_history_display)

        # if plotting available, show plot (plot_stats imported in simulate.py)
        if HAS_MPL:
            try:
                from simulate import plot_stats
                plot_stats(stats)
            except Exception:
                # ignore plotting errors
                pass

        self.root.after(0, self._sim_done)

    def _sim_done(self):
        self.sim_btn.config(state="normal")
        self.sim_entry.config(state="normal")

    def _reset_scores(self):
        if messagebox.askyesno("Reset", "Reset scores and history?"):
            self.scores = Counter({"player": 0, "computer": 0, "draw": 0})
            self.history = []
            self._update_scoreboard()
            self._update_history_display()
            self._set_last_result("","", "No rounds yet.")

    def _export_csv(self):
        """Export summary CSV with counts — quick file for submission."""
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files","*.csv"),("All files","*.*")],
                                            title="Save simulation summary")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Player", "Computer", "Draw"])
                writer.writerow([self.scores["player"], self.scores["computer"], self.scores["draw"]])
                writer.writerow([])
                writer.writerow(["History (latest first)"])
                writer.writerow(["Player move", "Computer move", "Result"])
                for row in self.history:
                    writer.writerow(row)
            messagebox.showinfo("Saved", f"Saved summary to: {path}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    # --- UI updates ---
    def _update_scoreboard(self):
        self.player_score_lbl.config(text=f"Player: {self.scores['player']}")
        self.comp_score_lbl.config(text=f"Computer: {self.scores['computer']}")
        self.draw_score_lbl.config(text=f"Draws: {self.scores['draw']}")

    def _set_last_result(self, p, c, result):
        if result == "No rounds yet.":
            text = result
        elif result == "SIM":
            text = p  # for aggregated summary we stored text in 'result'
        else:
            text = f"You: {p}   •   Computer: {c}   →   Winner: {result}"
        self.last_result_lbl.config(text=text)

    def _update_history_display(self):
        self.history_txt.config(state="normal")
        self.history_txt.delete("1.0", tk.END)
        for item in self.history[:200]:
            if item[0] == "SIM":
                # aggregated
                line = f"{item[2]}\n"
            else:
                p, c, r = item
                line = f"You: {p:7} | Comp: {c:7} | Winner: {r}\n"
            self.history_txt.insert("end", line)
        self.history_txt.config(state="disabled")


def main():
    root = tk.Tk()
    app = RPSGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()

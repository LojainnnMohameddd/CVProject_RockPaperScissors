from collections import Counter
from GameLogic import play_round
import random
import pprint
import csv
import statistics
import matplotlib.pyplot as plt
plt.style.use("seaborn-v0_8-colorblind")
import seaborn as sns
sns.set_theme(style="whitegrid", palette="pastel")

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False

MOVES = ["rock", "paper", "scissors"]

def simulate_n_rounds(n_rounds: int, player_strategy: str = "random"):
    if n_rounds <= 0:
        raise ValueError("n_rounds must be > 0")

    results = Counter()       
    player_moves = Counter()
    comp_moves = Counter()

    for _ in range(n_rounds):
        if player_strategy == "random":
            p = random.choice(MOVES)
        elif player_strategy.startswith("always_"):
            _, move = player_strategy.split("_", 1)
            p = move
        else:
            p = random.choice(MOVES)

        p_move, c_move, outcome = play_round(p)
        results[outcome] += 1
        player_moves[p_move] += 1
        comp_moves[c_move] += 1

    stats = {
        "rounds": n_rounds,
        "results": dict(results),
        "player_moves": dict(player_moves),
        "comp_moves": dict(comp_moves),
    }

    stats["percentages"] = {
        "player_win_pct": results["player"] / n_rounds * 100,
        "computer_win_pct": results["computer"] / n_rounds * 100,
        "draw_pct": results["draw"] / n_rounds * 100,
    }
    stats["player_move_pct"] = {m: player_moves[m] / n_rounds * 100 for m in MOVES}
    stats["comp_move_pct"] = {m: comp_moves[m] / n_rounds * 100 for m in MOVES}

    return stats

def pretty_print_stats(stats):
    print("\n=== Simulation Summary ===")
    print(f"Rounds: {stats['rounds']}")
    pprint.pprint({
        "results": stats["results"],
        "percentages": stats["percentages"],
        "player_move_pct": stats["player_move_pct"],
        "comp_move_pct": stats["comp_move_pct"]
    })

def plot_stats(stats):
    if not HAS_MPL:
        print("matplotlib not installed — skipping plots.")
        return

    import seaborn as sns
    sns.set_theme(style="whitegrid")

    # ======== GLASS STYLE SETTINGS ========
    plt.rcParams['axes.facecolor'] = (1, 1, 1, 0.4)         # semi-transparent panel
    plt.rcParams['figure.facecolor'] = (1, 1, 1, 0.15)      # glass effect
    plt.rcParams['savefig.facecolor'] = (1, 1, 1, 0)        # transparent for exporting
    glow_color = "#7FDBFF"  # neon blue glow

    # -------------------- GLASS BAR CHART -------------------- #
    labels = ["player", "computer", "draw"]
    vals = [stats["results"].get(l, 0) for l in labels]

    fig, ax = plt.subplots(figsize=(7,5))

    bars = sns.barplot(
        x=labels,
        y=vals,
        palette=["#88cffa", "#87e6c4", "#f7c7b6"],
        ax=ax
    )

    # Glow aura behind bars
    for i, bar in enumerate(ax.patches):
        bar_x = bar.get_x() + bar.get_width() / 2
        bar_y = bar.get_height()
        ax.scatter(
            bar_x, bar_y,
            s=500, color=glow_color, alpha=0.25, zorder=0
        )

    ax.set_title(
        f"Results over {stats['rounds']} rounds",
        fontsize=18, fontweight="bold", color="#00334e"
    )
    ax.set_ylabel("Count", fontsize=13, color="#00334e")
    ax.set_xlabel("Outcome", fontsize=13, color="#00334e")

    # Value labels
    for i, v in enumerate(vals):
        ax.text(i, v + 2, str(v), ha='center',
                fontsize=13, fontweight='bold', color="#00334e")

    # Glass border
    for spine in ax.spines.values():
        spine.set_color("#7FDBFF")
        spine.set_linewidth(1.5)

    plt.tight_layout()
    plt.show()

    # -------------------- GLASS PIE CHART -------------------- #
    labels = list(stats["comp_move_pct"].keys())
    vals = [stats["comp_move_pct"][k] for k in labels]
    colors = sns.color_palette("pastel")[0:3]

    fig, ax = plt.subplots(figsize=(6,6))

    wedges, texts, autotexts = ax.pie(
        vals,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={
            "linewidth": 2,
            "edgecolor": "#7FDBFF"
        },
        textprops={'fontsize': 13, 'color': '#00334e'}
    )

    # Glow effect on the center
    ax.scatter(0, 0, s=2000, color=glow_color, alpha=0.18, zorder=0)

    ax.set_title(
        "Computer Move Distribution",
        fontsize=18, fontweight="bold", color="#00334e"
    )

    plt.tight_layout()
    plt.show()


def save_stats_csv(stats, filename="simulation_results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rounds",
                         stats["rounds"]])
        writer.writerow([])
        writer.writerow(["Results", "Count"])
        for k,v in stats["results"].items():
            writer.writerow([k, v])
        writer.writerow([])
        writer.writerow(["Player move", "Count"])
        for k,v in stats["player_moves"].items():
            writer.writerow([k, v])
        writer.writerow([])
        writer.writerow(["Computer move", "Count"])
        for k,v in stats["comp_moves"].items():
            writer.writerow([k, v])
    print(f"Saved summary to {filename}")

def multi_experiment(trials: int, rounds_per_trial: int, strategy="random"):
    win_pcts = []
    comp_pcts = []
    draw_pcts = []

    for i in range(trials):
        s = simulate_n_rounds(rounds_per_trial, player_strategy=strategy)
        win_pcts.append(s["percentages"]["player_win_pct"])
        comp_pcts.append(s["percentages"]["computer_win_pct"])
        draw_pcts.append(s["percentages"]["draw_pct"])

    summary = {
        "trials": trials,
        "rounds_per_trial": rounds_per_trial,
        "player_win_mean": statistics.mean(win_pcts),
        "player_win_std": statistics.pstdev(win_pcts),
        "computer_win_mean": statistics.mean(comp_pcts),
        "computer_win_std": statistics.pstdev(comp_pcts),
        "draw_mean": statistics.mean(draw_pcts),
        "draw_std": statistics.pstdev(draw_pcts),
    }
    return summary

if __name__ == "__main__":
    n = 500
    stats = simulate_n_rounds(n_rounds=n, player_strategy="random")
    pretty_print_stats(stats)

    save_stats_csv(stats, filename="simulation_summary.csv")

    summary = multi_experiment(trials=30, rounds_per_trial=n, strategy="random")
    print("\n=== Multi-trial summary (30 trials) ===")
    pprint.pprint(summary)

    plot_stats(stats)

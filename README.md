# CVProject_RockPaperScissors
# Rock–Paper–Scissors — Computer Vision Semester Project 🎮🤖

A complete implementation of the classic **Rock–Paper–Scissors** game, built as part of the **Computer Vision course project**.  
The project includes:

- Clean **game logic** (independent from interface)
- **Simulation** and statistical analysis
- Beautiful **visualizations** (Seaborn + Glass-style Matplotlib)
- A full **Tkinter GUI**
- A structured **Jupyter Notebook** with experiments and reflections

---

## 📁 Project Structure

├── GameLogic.py # Core game logic (rules, random moves, winner selection)
├── simulate.py # Simulations, plots, CSV export
├── rps_gui.py # Tkinter interface for interactive gameplay
├── test.py # Quick functional testing of logic
├── project_notebook.ipynb # Full experiments, plots, analysis, reflection questions
├── results_bar.png # Example saved plot (bar chart)
├── comp_pie.png # Example saved plot (pie chart)
├── simulation_summary.csv # Sample output summary
└── README.md


---

## 🚀 Features

### ✔ **1. Independent Game Logic**
- Fully separated from interface  
- Pure Python functions  
- Reusable in any GUI or simulation  

### ✔ **2. Simulation Engine**
- Runs any number of rounds (20, 100, 500, 1000…)  
- Tracks:
  - Player wins  
  - Computer wins  
  - Draws  
  - Move distributions  
- Exports results to **CSV**

### ✔ **3. Visualization**
- Seaborn bar plots  
- Glass-style Matplotlib pie charts  
- Automatic saving to PNG  
- Clean, aesthetic design suitable for reports/notebooks

### ✔ **4. Tkinter GUI**
- Buttons for Rock, Paper, Scissors  
- Live scoreboard  
- Round history  
- Run a simulation from GUI  
- Export summary to CSV  
- Modern, clean UI (ttk theme)

### ✔ **5. Jupyter Notebook**
- Step-by-step experiments  
- Simulation results  
- Graphs  
- Interpretation & analysis  
- Full reflection answers

---

## 🛠 Installation

Install optional plotting libraries:

```bash
pip install matplotlib seaborn

▶️ How to Run

### Run simulation
python simulate.py

### Run GUI
python rps_gui.py

### Run test file
python test.py

📊 Example Outputs
Simulation summary (500 rounds)

Player wins ≈ 33%

Computer wins ≈ 33%

Draws ≈ 33%

As rounds increase, results converge to equal probability
→ Law of Large Numbers

Generated Plots

results_bar.png

comp_pie.png

🤓 Reflection Highlights

Random vs random results are expected to stay balanced

Small simulations show fluctuations, large simulations stabilize

Python uses the Mersenne Twister PRNG

Better strategies can predict opponent moves (frequency, Markov chains…)

Game logic is cleanly separated from the Tkinter interface


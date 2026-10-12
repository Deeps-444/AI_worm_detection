# AI Worm Detection and Containment

This project demonstrates runtime monitoring and containment of simulated AI worm behavior in a multi-agent system. A Streamlit dashboard lets you generate normal agent traffic or start a simulated worm attack, then inspect the network, agent status, monitoring decisions, and event history.

The runtime monitor scores messages using signals such as suspicious message content, unusually high message frequency, propagation between agents, and requests for restricted tools. Depending on the score, it allows, monitors, restricts, or blocks a message. When a message is blocked, its sender is isolated from further communication.

> link to the repo: https://github.com/Deeps-444/AI_worm_detection

## Project files

The source project is provided as `Copy_of_Cybersecurity_CA2.ipynb`. Its `%%writefile` cells create these files in the notebook's current directory:

- `simulation.py` — agent, runtime monitor, and normal traffic and worm attack simulations.
- `app.py` — Streamlit dashboard.

Run the notebook cells that contain `%%writefile simulation.py` and `%%writefile app.py` before starting Streamlit. Those cells need to finish successfully, and the generated files should be in the same directory.

## Requirements

- Python 3.9 or newer
- pip
- A modern web browser

## Run locally on Windows

Open PowerShell in the project folder (`C:\cyber_sec_project`) and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit pandas networkx matplotlib
```

If PowerShell prevents environment activation, you can either allow script activation for the current terminal with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again, or use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit pandas networkx matplotlib
```

Next, open `Copy_of_Cybersecurity_CA2.ipynb` in Jupyter (for example, from VS Code or Jupyter Notebook) and run the cells that write `simulation.py` and `app.py`. Then return to PowerShell and start the app:

```powershell
python -m streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`, and typically opens it in your default browser. If it does not open automatically, copy that URL into a browser. Keep the terminal running while you use the dashboard; press `Ctrl+C` there to stop the server.

## Run on macOS or Linux

From the project directory, create and activate a virtual environment, install dependencies, generate `simulation.py` and `app.py` by running their notebook cells, and launch Streamlit:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install streamlit pandas networkx matplotlib
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`, if a browser does not open automatically. Stop the server with `Ctrl+C` in the terminal.

## Using the dashboard

- **Number of Agents** in the sidebar sets the size of the simulated system (4–10 agents). Reset the simulation after changing this value to apply it to a fresh system.
- **Run Normal Traffic** sends routine messages between agents.
- **Start Worm Attack** marks an agent as compromised and simulates suspicious propagation attempts.
- **Reset Simulation** clears the current system and its results.
- The dashboard shows an overall status, message and agent counts, a network graph, agent status, monitoring logs, and an event feed.

The dashboard state is kept for the current Streamlit session. Each button click reruns the app and updates the displayed simulation state.

## Troubleshooting

- If Streamlit reports that it cannot find `app.py` or `simulation.py`, confirm that you ran both notebook `%%writefile` cells and that the generated files are in the directory where you ran the Streamlit command.
- If a module import fails, activate the virtual environment and install the listed dependencies there.
- If port 8501 is already in use, stop the other Streamlit process or run `python -m streamlit run app.py --server.port 8502`, then open `http://localhost:8502`.

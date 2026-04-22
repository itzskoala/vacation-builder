# VacationBuilder

A multi-agent AI system that turns a few answers about your dream trip into a full, ready-to-read vacation package — transport plan, budget, day-by-day itinerary, lodging options, and a visual gallery — all compiled into a clean HTML/Markdown report.

Built on [CrewAI](https://crewai.com). Seven specialist agents run in sequence, each handing their findings to the next.

## How it works

You answer a handful of questions at the terminal (destination, origin, dates, budget, group, activities you like). The crew then runs:

1. **Input Resolver** — fills in anything you left blank or marked `N/A` via live web search
2. **Travel Researcher** — builds a transport plan matched to your mode (flights, driving route, ferry, etc.)
3. **Financial Advisor** — assembles a per-person and total-group budget
4. **Activities Planner** — curates a day-by-day itinerary
5. **Accommodations Finder** — pulls lodging across budget tiers
6. **Photographer** — gathers a visual preview of the destination
7. **Vacation Compiler** — merges it all into one polished package

Output lands in `output/vacation_package.md` and `output/vacation_package.html`.

## Quick start

Requires **Python 3.10–3.13**. Uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# 1. Clone
git clone <your-repo-url>
cd vacation_builder

# 2. Install uv if you don't have it
pip install uv

# 3. Install dependencies
uv sync

# 4. Add your API keys (see below)
cp .env.example .env   # or create .env manually

# 5. Run the crew
crewai run
```

Answer the prompts in your terminal. When the crew finishes, open `output/vacation_package.html` in your browser.

## Environment variables

Create a `.env` file in the project root with:

```env
MODEL=ollama/llama3.1
API_BASE=http://localhost:XXXXX
SERPER_API_KEY=<your-serper-api-key>

# Optional — enables push notifications when the run finishes
PUSHOVER_USER=<your-pushover-user-key>
PUSHOVER_TOKEN=<your-pushover-app-token>
```

Get a free [Serper](https://serper.dev) key for the Google Flights / Hotels / Events / Images tools.

## Project layout

```
src/vacation_builder/
  crew.py              # Agent + task wiring
  main.py              # CLI entrypoint
  html_export.py       # Markdown → HTML conversion
  config/
    agents.yaml        # Agent roles, goals, backstories
    tasks.yaml         # Task definitions
  tools/               # Custom Serper-based tools
output/                # Generated vacation_package.md / .html
```

## Customizing

Tweak the crew to fit your needs by editing:

- `src/vacation_builder/config/agents.yaml` — change an agent's role, goal, or backstory
- `src/vacation_builder/config/tasks.yaml` — change what each task produces
- `src/vacation_builder/crew.py` — add/remove agents, swap tools, change the process
- `src/vacation_builder/main.py` — change the input prompts

## License

MIT

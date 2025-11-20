# Workout Program Generator

A smart workout program generator that creates personalized training splits based on your goals, available training days, and exercise preferences.

## Live Demo

Try it live here: https://mytrainingpal.onrender.com

## Features

- **Smart Split Selection**: Automatically chooses the best training split based on available days per week
  - 2-3 days: Full Body
  - 4-5 days: Upper/Lower
  - 6 days: Push/Pull/Legs

- **Personalized Volume**: Set different goals for each muscle group
  - Maintenance: 4-6 sets/week
  - Normal Growth: 7-10 sets/week
  - Prioritized Growth: 11-13 sets/week

- **Exercise Selection**: Choose from a comprehensive exercise database with proper movement patterns

- **Intelligent Programming**:
  - Prioritizes compound movements
  - Prevents exercise duplication within sessions
  - Respects movement pattern constraints (e.g., horizontal vs vertical push/pull)
  - Distributes volume evenly across the week

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render
- **Version Control**: Git/GitHub

## Project Structure

```
├── version_site/          # Web application
│   ├── app.py            # Flask application
│   ├── core/             # Core logic
│   │   ├── prog.py       # Program generation algorithm
│   │   └── exercise_database.py
│   ├── templates/        # HTML templates
│   └── static/          # CSS and static assets
├── version_tkinter/      # Desktop version (TKinter)
└── version_kivy/        # Mobile version (Kivy)
```

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/AlexPeirano/gym.tKinter.git
cd gym.tKinter/version_site
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser to `http://localhost:5001`

## How It Works

1. **Choose your training frequency** (2-6 days per week)
2. **Select exercises** for each muscle group from the database
3. **Set your goals** for each muscle group (maintenance, growth, or prioritized growth)
4. **Generate your program** - the algorithm creates an optimal weekly training split

The program uses intelligent algorithms to:
- Calculate exact weekly volume targets based on your goals
- Select and distribute exercises across sessions
- Ensure proper exercise variety and movement patterns
- Adjust sets and reps to hit precise volume targets

## Contributing

Feel free to open issues or submit pull requests.

## License

This project is open source and available under the MIT License.

---

Made by Alex Peirano

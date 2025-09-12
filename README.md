# GenAI Projects

This repository contains various Python projects and scripts focusing on web applications, automation, and interactive tools.

## Project Structure

### Flask Demo
- **Calculator API** (`flaskdemo.py`): RESTful API for basic arithmetic operations
- **Mini Social Network** (`streamlit_demo.py`): Interactive social media demo with Streamlit featuring:
  - User posts with timestamps
  - Like functionality
  - Real-time feed updates

### Playwright Automation
- **Facebook Metadata Scraper** (`storemetadata.py`): Extracts and saves metadata from Facebook
- **Sports News Fetcher** (`playwrightkeyfunctions.py`): Automated news aggregation
- **Match News API** (`flaskdemo.py`): Flask API endpoint for latest match news

### PyAutoGUI RPA
- **Mouse Control Demo** (`finding_the_mouse_pointer.py`): Mouse pointer tracking
- **RPA Scripts** (`rpa_demo.py`): Desktop automation examples including:
  - Mouse movement and clicks
  - Keyboard input simulation
  - Image recognition capabilities

### Python Daily Challenge
A 15-day coding challenge with interactive Streamlit applications:
1. **Day 1** - Greeting Form: Interactive user greeting with age-based responses
2. **Day 2** - Expense Splitter: Group expense calculator with settlement suggestions
3. **Day 3** - Simple Calculator: Basic arithmetic operations with UI
4. **Day 4** - BMI Calculator: Stylish BMI calculator with visual feedback
5. **Day 5** - Unit Converter: Multi-unit converter featuring:
   - Currency conversion with live rates
   - Temperature conversion across units
   - Length and weight conversions
   - Animated UI with Lottie animations

## Prerequisites
- Python 3.13 or higher
- Virtual environment setup (paarivenv)

## Key Dependencies
- Web Development: `flask`, `streamlit`
- Automation: `playwright`, `pyautogui`
- UI Enhancement: `streamlit-lottie`
- Data Processing: `numpy`, `pandas`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/paari24/genAI.git
   cd genAI
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv paarivenv
   source paarivenv/bin/activate  # On Windows: paarivenv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install flask streamlit playwright pyautogui streamlit-lottie numpy pandas
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Usage

Each project can be run independently:

- Flask Applications:
  ```bash
  python flaskDemo/flaskdemo.py
  streamlit run flaskDemo/streamlit_demo.py
  ```

- Automation Scripts:
  ```bash
  python playwright/storemetadata.py
  python pyautogui/rpa_demo.py
  ```

- Daily Challenges:
  ```bash
  streamlit run pythonDailyChallenge/day{1-5}.py
  ```

## Author

paari24

## License

This project is available under the MIT License. See the LICENSE file for more details.

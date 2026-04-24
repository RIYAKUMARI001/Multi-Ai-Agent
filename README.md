# Multi-Agent Travel Assistant 

This is a smart travel planning system built with **LangChain** and **LangGraph**. It uses a team of specialized AI agents to help you plan the perfect 3-day trip without you having to do all the research yourself.

<img width="1442" height="641" alt="image" src="https://github.com/user-attachments/assets/29fb6f2d-ad72-4d7a-a9a2-d12b01a6fbb4" />
<img width="1475" height="446" alt="image" src="https://github.com/user-attachments/assets/de397ddf-cc7d-4a4f-83b8-8bb125863128" />
<img width="1315" height="365" alt="image" src="https://github.com/user-attachments/assets/822c876c-02e7-4ab6-9946-aaf3e420d367" />
<img width="1457" height="596" alt="image" src="https://github.com/user-attachments/assets/4beda06d-86c8-4c99-b0c0-f5037a8dac65" />

### How it works
Instead of one big boring prompt, this system splits the work between 4 different "experts":
*   **Travel Planner**: Focuses on making a solid day-by-day itinerary.
*   **Budget Analyst**: Handles all the math and estimates how much you'll spend.
*   **Local Expert**: Adds those cool "hidden gems" and culture tips that only locals know.
*   **Finalizer**: Takes everything and cleans it up into a readable report.

They all talk to each other and share the same "State," so the final result feels like it was written by a real travel agency.

### Getting Started
1. **Clone the project** to your local machine.
2. **Install the dependencies**:
   ```bash
   pip install langchain langgraph langchain-google-genai python-dotenv
   ```
3. **Set up your API Key**: 
   - Create a `.env` file in the main folder.
   - Add your key: `GOOGLE_API_KEY=your_actual_key_here`

### Usage
To start planning, just run:
```bash
python multi_agent_system.py
```
It’ll ask you where you want to go and what you’re into (like food, history, etc.), and then it'll generate the full plan for you. 

Happy travels! 


# ✈️ Multi-Agent AI Travel Planner

An AI-powered travel planner built with CrewAI that uses multiple 
specialized agents to research and generate personalized itineraries.

## Features
- 🤖 4 specialized AI agents (Planner, Researcher, Writer, Critic)
- 🌤️ Live weather forecasts using Open-Meteo API
- 🗺️ Interactive map with recommended places
- 📄 PDF export of your itinerary
- ✈️ Inputs: departure city, destination, budget, travel style, interests


## Tech Stack
- **CrewAI** — multi-agent orchestration
- **Groq API** — LLM inference (Llama 3.3 70B)
- **Tavily API** — real-time web search
- **Open-Meteo API** — live weather data
- **Streamlit** — web interface
- **Folium** — interactive maps
- **fpdf2** — PDF generation


## Architecture
User Input → Planner Agent → Researcher Agent → Writer Agent → Critic Agent → Output
↓
Tavily Search + Weather Tool


## Screenshots

![Screenshot 1](https://raw.githubusercontent.com/BHARATHKUMARVNAIK/Multi-agent-travel-planner/main/images/Screenshot%202026-05-15%20at%206.05.33%E2%80%AFPM.png)
![Screenshot 2](https://raw.githubusercontent.com/BHARATHKUMARVNAIK/Multi-agent-travel-planner/main/images/Screenshot%202026-05-15%20at%206.05.59%E2%80%AFPM.png)
![Screenshot 3](https://raw.githubusercontent.com/BHARATHKUMARVNAIK/Multi-agent-travel-planner/main/images/Screenshot%202026-05-15%20at%206.06.13%E2%80%AFPM.png)
![Screenshot 4](https://raw.githubusercontent.com/BHARATHKUMARVNAIK/Multi-agent-travel-planner/main/images/Screenshot%202026-05-15%20at%206.06.30%E2%80%AFPM.png)
![Screenshot 5](https://raw.githubusercontent.com/BHARATHKUMARVNAIK/Multi-agent-travel-planner/main/images/Screenshot%202026-05-15%20at%206.06.41%E2%80%AFPM.png)

## Setup

1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-travel-planner
cd multi-agent-travel-planner
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key


4. Run the app
```bash
streamlit run app.py
```

## Free APIs Used
| API        | Purpose       | Cost |
|-----       |---------      |------|
| Groq       | LLM inference | Free tier |
| Tavily     | Web search    | Free tier |
| Open-Meteo | Weather       | Completely free |

## Author
Built by Bharath kumar V Naik — bharathkumar.v179@gmail.com

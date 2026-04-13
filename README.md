# FLL Lesson Builder Agent

An AI-powered application designed to help FIRST LEGO League (FLL) coaches create educational materials (PowerPoint presentations and Word documents) for students aged 9-14.

## Features
- AI Agent built with LangGraph for lesson planning.
- PowerPoint generation for visual teaching.
- Word document generation for detailed handouts.
- Web search capabilities for up-to-date FLL information.

## Project Structure
- `agent/`: Core agent logic (state, nodes, graph, and prompts).
- `tools/`: PowerPoint and Word document generation tools.
- `config/`: Configuration management using Pydantic.
- `output/`: Directory for generated documents.
- `tests/`: Project test suite.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file based on `.env.example` and add your API keys.
3. Run the application: `python app.py`
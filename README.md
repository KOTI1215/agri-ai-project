# Agri-AI Smart Farming System

An AI-powered web application built with Flask for smart agriculture, featuring crop yield forecasting and leaf disease detection.

## Features
- **Crop Leaf Disease Detection:** Upload leaf images to instantly analyze and detect potential agricultural diseases.
- **Crop Yield Forecasting:** Input environmental factors (rainfall and temperature) to predict expected crop yields using a trained machine learning model.

## Tech Stack
- **Backend:** Python, Flask
- **Machine Learning / Data:** Scikit-Learn, Pickle
- **Frontend:** HTML5, CSS3, Bootstrap (or custom styling)

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/KOTI1215/agri-ai-project.git](https://github.com/KOTI1215/agri-ai-project.git)
   cd agri-ai-project
   # Agri-AI Smart Farming System 🌾🤖

An intelligent web-based smart farming assistant built with **Flask**, **SQLite**, and **Bootstrap**, featuring live weather integration, crop yield forecasting, fertilizer recommendations, and multilingual support (English and Bahasa Melayu).

## 🚀 Features
1. **Crop Yield Forecasting & Weather Integration:** Fetches live meteorological data via the OpenWeatherMap API and estimates crop yields.
2. **Fertilizer Recommendations:** Provides customized nutrient advice (Nitrogen, Phosphorus, Potassium) based on crop requirements.
3. **Activity History Logging:** Automatically logs all user queries, predictions, and recommendations to a persistent SQLite database (`farming_history.db`).
4. **Multilingual Support:** Dynamic language switching between English and Bahasa Melayu.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Requests
* **Database:** SQLite
* **Frontend:** HTML5, Bootstrap 5, Jinja2 Templates
* **External API:** OpenWeatherMap API

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/KOTI1215/agri-ai-project.git](https://github.com/KOTI1215/agri-ai-project.git)
   cd agri-ai-project
   # Agri-AI Smart Farming System

A full-stack web application built with **Flask**, **SQLite**, and **Tailwind CSS** that provides real-time global weather lookups, intelligent agricultural advisories, and an automated activity history log.

## Features
* **Global City Weather Lookup:** Integrates with the OpenWeatherMap API to fetch live temperature, humidity, and atmospheric conditions for any city worldwide.
* **Smart Irrigation Advisory:** Automatically evaluates weather metrics (such as rain conditions, extreme heat, and humidity) to recommend optimal irrigation strategies.
* **Fertilizer & Pest Advisory:** Form inputs to manage crop nutrient levels (NPK) and diagnose pest or disease symptoms.
* **Activity History Log:** Uses Flask-SQLAlchemy to securely record and display all user queries, timestamps, and advisories in an embedded dashboard table.

## Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Requests
* **Frontend:** HTML5, Tailwind CSS (CDN), Jinja2 Templating
* **Database:** SQLite (`farming_v2.db`)

## Getting Started
1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows PowerShell
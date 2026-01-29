# Gemini Chart Box

A web application that generates and analyzes charts using Google's Gemini AI API.

## Features

- 📊 **Dynamic Chart Generation**: Create bar, line, pie, and doughnut charts with AI
- 🤖 **AI-Powered Analysis**: Get intelligent insights about your data using Gemini
- 🎨 **Beautiful UI**: Modern, responsive interface with gradient design
- ⚡ **Real-time Processing**: Instant chart generation and analysis

## Project Structure

```
gemini chart box/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
└── frontend/
    ├── index.html          # Main HTML page
    └── script.js           # Frontend logic
```

## Prerequisites

- Python 3.8+
- Google Gemini API Key
- Modern web browser

## Setup Instructions

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API key"
3. Copy your API key

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file (copy from `.env.example`):
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` and paste your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   FLASK_ENV=development
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

   The server will start at `http://localhost:5000`

### 3. Frontend Setup

1. Open `frontend/index.html` in your web browser
   - Or use Live Server extension in VS Code
   - Or start a simple HTTP server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - Then visit `http://localhost:8000`

## Usage

1. Enter a query describing the data you want to visualize:
   - Example: "Monthly sales for Q1 2025"
   - Example: "Website traffic by source"

2. Select a chart type:
   - Bar Chart
   - Line Chart
   - Pie Chart
   - Doughnut Chart

3. Click "Generate Chart"

4. The AI will:
   - Generate appropriate data based on your query
   - Display an interactive chart
   - Provide AI-powered insights about the data

## API Endpoints

### POST `/api/analyze`
Generates chart data using Gemini AI

**Request:**
```json
{
  "query": "Monthly sales data",
  "chartType": "bar"
}
```

**Response:**
```json
{
  "success": true,
  "chartData": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [{
      "label": "Sales",
      "data": [100, 150, 200],
      "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56"]
    }],
    "insights": "Sales showed a steady increase..."
  },
  "chartType": "bar"
}
```

### POST `/api/insights`
Gets AI insights about the chart data

**Request:**
```json
{
  "description": "Monthly sales chart"
}
```

**Response:**
```json
{
  "success": true,
  "insights": "The data shows..."
}
```

### GET `/api/health`
Health check endpoint

## Troubleshooting

**CORS Error**: Make sure Flask is running with CORS enabled (already configured in app.py)

**API Key Error**: Verify your API key is correctly set in `.env`

**Chart not displaying**: Check browser console for errors and ensure both frontend and backend are running

**Connection refused**: Make sure Flask server is running on port 5000

## Technologies Used

- **Backend**: Flask, Python, Google Generative AI
- **Frontend**: HTML5, JavaScript, Chart.js
- **Styling**: CSS3 with Gradients and Animations

## License

MIT

## Contributing

Feel free to modify and extend this project!

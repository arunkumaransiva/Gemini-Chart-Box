from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please create a .env file with your API key.")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Sample datasets for demo
SAMPLE_DATASETS = {
    'sales': {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'datasets': [{
            'label': 'Monthly Sales (2025)',
            'data': [12000, 19000, 15000, 25000, 22000, 30000],
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
            'borderColor': '#333',
            'borderWidth': 1
        }],
        'insights': 'Sales show an upward trend with a peak in June. Q1 averaged $15,333 while Q2 averaged $25,667.'
    },
    'traffic': {
        'labels': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'datasets': [{
            'label': 'Website Traffic',
            'data': [2500, 3200, 2800, 4100, 5200, 3800, 2100],
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': '#36A2EB',
            'borderWidth': 2
        }],
        'insights': 'Website traffic peaks on Friday with 5,200 visitors. Weekdays average 3,570 visitors compared to 2,950 on weekends.'
    },
    'products': {
        'labels': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'datasets': [{
            'label': 'Units Sold (Q1 2025)',
            'data': [450, 320, 280, 180, 240],
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        }],
        'insights': 'Product A leads with 450 units sold. Top 3 products account for 68% of total sales.'
    },
    'revenue': {
        'labels': ['Product A', 'Product B', 'Product C', 'Product D'],
        'datasets': [{
            'label': 'Revenue Distribution',
            'data': [35, 25, 20, 20],
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
        }],
        'insights': 'Product A generates 35% of total revenue. The top 2 products account for 60% of all revenue.'
    },
    'growth': {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [{
            'label': 'Revenue (in thousands)',
            'data': [65, 78, 90, 120],
            'backgroundColor': 'rgba(75, 192, 75, 0.5)',
            'borderColor': '#4BC0C0',
            'borderWidth': 2,
            'fill': True
        }],
        'insights': 'Quarter-over-quarter growth shows strong acceleration, with Q4 revenue 85% higher than Q1. Annualized revenue projected at $353K.'
    }
}

def format_chart_data(chart_type, chart_data):
    """Format chart data according to chart type requirements"""
    if chart_type in ['pie', 'doughnut']:
        # Pie and doughnut charts need single dataset with all data
        if 'datasets' in chart_data and len(chart_data['datasets']) > 0:
            dataset = chart_data['datasets'][0]
            return {
                'labels': chart_data.get('labels', []),
                'datasets': [{
                    'label': dataset.get('label', 'Data'),
                    'data': dataset.get('data', []),
                    'backgroundColor': dataset.get('backgroundColor', [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                    ]),
                    'borderColor': '#fff',
                    'borderWidth': 2
                }],
                'insights': chart_data.get('insights', '')
            }
    elif chart_type == 'line':
        # Line charts need proper styling
        if 'datasets' in chart_data and len(chart_data['datasets']) > 0:
            dataset = chart_data['datasets'][0]
            return {
                'labels': chart_data.get('labels', []),
                'datasets': [{
                    'label': dataset.get('label', 'Data'),
                    'data': dataset.get('data', []),
                    'borderColor': '#36A2EB',
                    'backgroundColor': 'rgba(54, 162, 235, 0.1)',
                    'borderWidth': 2,
                    'fill': True,
                    'tension': 0.4,
                    'pointBackgroundColor': '#36A2EB',
                    'pointBorderColor': '#fff',
                    'pointBorderWidth': 2,
                    'pointRadius': 5
                }],
                'insights': chart_data.get('insights', '')
            }
    
    # Default bar chart or other types
    return chart_data

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample datasets"""
    return jsonify({
        'success': True,
        'datasets': list(SAMPLE_DATASETS.keys()),
        'data': SAMPLE_DATASETS
    })

@app.route('/api/sample-data/<dataset_name>', methods=['GET'])
def get_sample_dataset(dataset_name):
    """Get specific sample dataset"""
    if dataset_name in SAMPLE_DATASETS:
        chart_type = request.args.get('chartType', 'bar')
        chart_data = SAMPLE_DATASETS[dataset_name]
        formatted_data = format_chart_data(chart_type, chart_data)
        return jsonify({
            'success': True,
            'chartData': formatted_data,
            'chartType': chart_type
        })
    return jsonify({'error': 'Dataset not found'}), 404

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Analyze data using Gemini AI and prepare chart data"""
    try:
        data = request.json
        user_query = data.get('query', '')
        chart_type = data.get('chartType', 'bar')
        
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Create a prompt for Gemini to generate chart data
        prompt = f"""
        Based on this request: "{user_query}"
        
        Generate JSON data for a {chart_type} chart with the following structure:
        {{
            "labels": ["label1", "label2", "label3", "label4", "label5"],
            "datasets": [{{
                "label": "Data Series 1",
                "data": [value1, value2, value3, value4, value5],
                "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
            }}],
            "insights": "Brief insight about the data"
        }}
        
        Important:
        - Use realistic numbers appropriate to the context
        - Provide 5 data points minimum
        - Use diverse colors for visualization
        - Keep insights under 100 words
        - Respond with ONLY valid JSON, no additional text or markdown
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to parse JSON from response
        try:
            # Clean up response if needed
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            chart_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback with better default data
            chart_data = {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                "datasets": [{
                    "label": "Sample Data",
                    "data": [25, 40, 35, 50, 45],
                    "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
                }],
                "insights": response_text if response_text else "Data visualization showing trends over time."
            }
        
        return jsonify({
            'success': True,
            'chartData': format_chart_data(chart_type, chart_data),
            'chartType': chart_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['POST'])
def get_insights():
    """Get AI insights about chart data"""
    try:
        data = request.json
        chart_description = data.get('description', '')
        
        if not chart_description:
            return jsonify({'error': 'Description is required'}), 400
        
        prompt = f"""
        Provide 2-3 key insights about this chart/data: {chart_description}
        Keep insights concise and actionable.
        """
        
        response = model.generate_content(prompt)
        
        return jsonify({
            'success': True,
            'insights': response.text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Gemini Chart Box API is running'})

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='127.0.0.1')

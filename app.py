import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math
import os

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Required for Render deployment

# Color palette - strictly enforced
COLORS = {
    'charcoal': '#0F1113',
    'dark_grey': '#1B1D1F',
    'gold_primary': '#D4AF37',
    'highlight_gold': '#FFCF66',
    'neutral_text': '#B8B9BB',
    'success_green': '#3DBC6B',
    'danger_red': '#E4574C',
    'warning_orange': '#F4A261'
}

# Generate sample data using pure Python (no pandas/numpy)
def generate_sample_data():
    try:
        # Set random seed for consistent data
        random.seed(42)
        
        # 1. Financial Impact data
        financial_data = {
            'categories': ['Revenue', 'Operating Costs', 'Net Profit', 'Investments', 'Returns'],
            'current': [2850000, -1320000, 1530000, -480000, 720000],
            'previous': [2600000, -1450000, 1150000, -520000, 580000]
        }
        
        # 2. Deadline Tracker data
        deadline_data = {
            'tasks': ['Q4 Financial Report', 'System Infrastructure Upgrade', 'Compliance Audit Review', 'Annual Budget Planning', 'Security Assessment'],
            'days_left': [3, 15, 1, 12, 8],
            'progress': [85, 45, 95, 60, 70]
        }
        # Add urgency status based on days left
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        # 3. Alert Severity data
        alert_data = {
            'severity': ['Critical', 'Warning', 'Info'],
            'count': [8, 24, 42]
        }
        
        # 4. Historical Trends data (last 365 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Generate dates
        historical_dates = []
        current_date = start_date
        while current_date <= end_date:
            historical_dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Generate realistic trending data
        base_value = 1000
        historical_performance = []
        for i, date in enumerate(historical_dates):
            # Add trend, seasonality, and noise
            trend = (i / len(historical_dates)) * 200
            seasonal = 100 * math.sin(2 * math.pi * i / 365)
            noise = random.uniform(-50, 50)
            value = base_value + trend + seasonal + noise
            historical_performance.append(value)
        
        historical_data = {
            'dates': historical_dates,
            'performance': historical_performance,
            'target': 1200
        }
        
        # 5. Growth vs Decline data
        growth_data = {
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            'growth_rate': [12, 18, 15, 22, 28, 25, 30, 35],
            'decline_rate': [5, 8, 4, 6, 9, 7, 8, 6]
        }
        
        # 6. Performance KPIs data
        performance_data = {
            'kpis': ['Operational Efficiency', 'Quality Score', 'Response Time', 'Cost Optimization', 'Customer Satisfaction'],
            'current_score': [85, 92, 78, 88, 91],
            'target_score': [90, 95, 85, 90, 95],
            'industry_avg': [75, 85, 80, 82, 87]
        }
        
        # 7. Risk score (single value for gauge)
        risk_score = 68  # Out of 100 (lower is better)
        
        # 8. Projection & Forecast data (next 12 months)
        future_dates = []
        current_month = datetime.now().replace(day=1)
        for i in range(12):
            future_dates.append(current_month + timedelta(days=32*i))
        
        base_forecast = 1500
        growth_rate = 0.05
        forecast_values = []
        lower_confidence = []
        upper_confidence = []
        
        for i in range(12):
            forecast = base_forecast * (1 + growth_rate) ** i
            forecast_values.append(forecast)
            lower_confidence.append(forecast * 0.85)
            upper_confidence.append(forecast * 1.15)
        
        projection_data = {
            'dates': future_dates,
            'forecast': forecast_values,
            'lower_confidence': lower_confidence,
            'upper_confidence': upper_confidence
        }
        
        return {
            'financial': financial_data,
            'deadlines': deadline_data,
            'alerts': alert_data,
            'historical': historical_data,
            'growth': growth_data,
            'performance': performance_data,
            'risk_score': risk_score,
            'projections': projection_data
        }
        
    except Exception as e:
        print(f"Error generating sample data: {str(e)}")
        # Return minimal fallback data
        return {
            'financial': {'categories': ['Revenue'], 'current': [1000000], 'previous': [900000]},
            'deadlines': {'tasks': ['Sample Task'], 'days_left': [5], 'progress': [50], 'urgency': ['Normal']},
            'alerts': {'severity': ['Info'], 'count': [10]},
            'historical': {'dates': [datetime.now()], 'performance': [1000], 'target': 1200},
            'growth': {'months': ['Jan'], 'growth_rate': [15], 'decline_rate': [5]},
            'performance': {'kpis': ['Performance'], 'current_score': [80], 'target_score': [90], 'industry_avg': [75]},
            'risk_score': 70,
            'projections': {'dates': [datetime.now()], 'forecast': [1500], 'lower_confidence': [1400], 'upper_confidence': [1600]}
        }

# Initialize data
data = generate_sample_data()

# Common chart layout template
def get_base_layout(title):
    return {
        'title': {
            'text': title,
            'font': {'color': COLORS['neutral_text'], 'size': 18, 'family': 'Inter'},
            'x': 0.5,
            'xanchor': 'center'
        },
        'paper_bgcolor': COLORS['charcoal'],
        'plot_bgcolor': COLORS['dark_grey'],
        'font': {'color': COLORS['neutral_text'], 'family': 'Inter'},
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
        'showlegend': True,
        'legend': {
            'font': {'color': COLORS['neutral_text']},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': COLORS['neutral_text'],
            'borderwidth': 1
        },
        'xaxis': {'color': COLORS['neutral_text'], 'gridcolor': '#2A2D30'},
        'yaxis': {'color': COLORS['neutral_text'], 'gridcolor': '#2A2D30'}
    }

# Chart 1: Financial Impact Bar Chart
def create_financial_chart():
    try:
        fig = go.Figure()
        
        # Current period bars
        colors_current = [COLORS['success_green'] if x > 0 else COLORS['danger_red'] for x in data['financial']['current']]
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<br><extra></extra>',
            text=[f"${x:,.0f}" for x in data['financial']['current']],
            textposition='outside'
        ))
        
        # Previous period bars
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=COLORS['gold_primary'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<br><extra></extra>'
        ))
        
        layout = get_base_layout('Financial Impact Analysis')
        layout['yaxis']['tickformat'] = '$,.0f'
        layout['barmode'] = 'group'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating financial chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 2: Deadline Tracker Horizontal Timeline
def create_deadline_chart():
    try:
        urgency_colors = {
            'Critical': COLORS['danger_red'],
            'Warning': COLORS['warning_orange'], 
            'Normal': COLORS['success_green']
        }
        
        fig = go.Figure()
        
        colors = [urgency_colors[urgency] for urgency in data['deadlines']['urgency']]
        
        fig.add_trace(go.Bar(
            x=data['deadlines']['days_left'],
            y=data['deadlines']['tasks'],
            orientation='h',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>Days Remaining: %{x}<br>Progress: %{customdata}%<br><extra></extra>',
            customdata=data['deadlines']['progress'],
            text=[f"{days}d" for days in data['deadlines']['days_left']],
            textposition='middle right'
        ))
        
        layout = get_base_layout('Project Deadline Tracker')
        layout['xaxis']['title'] = 'Days Remaining'
        layout['height'] = 400
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating deadline chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 3: Alert Severity Donut Chart
def create_alert_chart():
    try:
        severity_colors = [COLORS['danger_red'], COLORS['warning_orange'], COLORS['success_green']]
        
        fig = go.Figure(go.Pie(
            labels=data['alerts']['severity'],
            values=data['alerts']['count'],
            hole=0.6,
            marker_colors=severity_colors,
            hovertemplate='<b>%{label} Alerts</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            textinfo='label+percent',
            textfont={'color': 'white', 'size': 12}
        ))
        
        # Add center annotation
        total_alerts = sum(data['alerts']['count'])
        fig.add_annotation(
            text=f"Total<br><b>{total_alerts}</b><br>Alerts",
            x=0.5, y=0.5,
            font={'size': 16, 'color': COLORS['neutral_text']},
            showarrow=False
        )
        
        layout = get_base_layout('Alert Severity Distribution')
        layout['showlegend'] = False
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating alert chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 4: Historical Trends Area Chart
def create_historical_chart():
    try:
        fig = go.Figure()
        
        # Performance area chart
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['performance'],
            mode='lines',
            line={'color': COLORS['gold_primary'], 'width': 3},
            fill='tonexty',
            fillcolor=f"rgba(212, 175, 55, 0.3)",
            name='Performance Metric',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Performance: %{y:,.1f}<extra></extra>'
        ))
        
        # Target line
        fig.add_hline(
            y=data['historical']['target'],
            line_dash="dash",
            line_color=COLORS['success_green'],
            line_width=2,
            annotation_text="Performance Target",
            annotation_position="top right"
        )
        
        layout = get_base_layout('Historical Performance Trends')
        layout['xaxis']['title'] = 'Date'
        layout['yaxis']['title'] = 'Performance Score'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating historical chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 5: Growth vs Decline Stacked Analysis
def create_growth_chart():
    try:
        fig = go.Figure()
        
        # Growth bars
        fig.add_trace(go.Bar(
            x=data['growth']['months'],
            y=data['growth']['growth_rate'],
            name='Growth Rate',
            marker_color=COLORS['success_green'],
            hovertemplate='<b>%{x}</b><br>Growth: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['growth_rate']],
            textposition='outside'
        ))
        
        # Decline bars (negative values)
        decline_negative = [-rate for rate in data['growth']['decline_rate']]
        fig.add_trace(go.Bar(
            x=data['growth']['months'],
            y=decline_negative,
            name='Decline Rate',
            marker_color=COLORS['danger_red'],
            hovertemplate='<b>%{x}</b><br>Decline: %{y}%<extra></extra>',
            text=[f"-{rate}%" for rate in data['growth']['decline_rate']],
            textposition='outside'
        ))
        
        layout = get_base_layout('Growth vs Decline Analysis')
        layout['yaxis']['title'] = 'Rate (%)'
        layout['yaxis']['ticksuffix'] = '%'
        layout['xaxis']['title'] = 'Month'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating growth chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 6: Performance Comparison Radar Chart
def create_performance_chart():
    try:
        fig = go.Figure()
        
        # Current performance
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['current_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Current Performance',
            line_color=COLORS['gold_primary'],
            fillcolor=f"rgba(212, 175, 55, 0.4)",
            hovertemplate='<b>%{theta}</b><br>Current: %{r}%<extra></extra>'
        ))
        
        # Target performance
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Target',
            line_color=COLORS['success_green'],
            fillcolor=f"rgba(61, 188, 107, 0.2)",
            hovertemplate='<b>%{theta}</b><br>Target: %{r}%<extra></extra>'
        ))
        
        # Industry average
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['industry_avg'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Industry Average',
            line_color=COLORS['neutral_text'],
            line_dash='dot',
            hovertemplate='<b>%{theta}</b><br>Industry Avg: %{r}%<extra></extra>'
        ))
        
        layout = get_base_layout('Performance vs Target KPIs')
        layout['polar'] = {
            'radialaxis': {
                'visible': True,
                'range': [0, 100],
                'color': COLORS['neutral_text'],
                'ticksuffix': '%'
            },
            'angularaxis': {'color': COLORS['neutral_text']}
        }
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating performance chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 7: Risk & Compliance Gauge
def create_risk_gauge():
    try:
        # Determine gauge color based on risk score
        if data['risk_score'] <= 30:
            gauge_color = COLORS['success_green']
        elif data['risk_score'] <= 70:
            gauge_color = COLORS['warning_orange']
        else:
            gauge_color = COLORS['danger_red']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=data['risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk & Compliance Score", 'font': {'color': COLORS['neutral_text'], 'size': 16}},
            delta={
                'reference': 50,
                'increasing': {'color': COLORS['danger_red']},
                'decreasing': {'color': COLORS['success_green']}
            },
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': COLORS['neutral_text'],
                    'tickfont': {'color': COLORS['neutral_text']}
                },
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(61, 188, 107, 0.3)'},
                    {'range': [30, 70], 'color': 'rgba(244, 162, 97, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(228, 87, 76, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': COLORS['neutral_text'], 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            },
            number={'font': {'color': COLORS['neutral_text'], 'size': 24}}
        ))
        
        fig.update_layout(
            paper_bgcolor=COLORS['charcoal'],
            plot_bgcolor=COLORS['charcoal'],
            font={'color': COLORS['neutral_text'], 'family': 'Inter'},
            margin={'l': 40, 'r': 40, 't': 60, 'b': 40},
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error creating risk gauge: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Chart 8: Projection & Forecast with Confidence Bands
def create_projection_chart():
    try:
        fig = go.Figure()
        
        # Upper confidence bound (invisible, for fill)
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['upper_confidence'],
            mode='lines',
            line={'width': 0},
            showlegend=False,
            hoverinfo='skip',
            name='Upper Bound'
        ))
        
        # Lower confidence bound with fill
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['lower_confidence'],
            mode='lines',
            line={'width': 0},
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.2)',
            name='Confidence Interval',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Range: $%{y:,.0f} - $%{customdata:,.0f}<extra></extra>',
            customdata=data['projections']['upper_confidence']
        ))
        
        # Main forecast line
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['forecast'],
            mode='lines+markers',
            line={'color': COLORS['gold_primary'], 'width': 4},
            marker={'size': 8, 'color': COLORS['highlight_gold']},
            name='Revenue Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
        ))
        
        layout = get_base_layout('12-Month Revenue Projection')
        layout['xaxis']['title'] = 'Month'
        layout['yaxis']['title'] = 'Revenue ($)'
        layout['yaxis']['tickformat'] = '$,.0f'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error creating projection chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# Enhanced CSS with better responsive design
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>LexCura Executive Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: #0F1113;
                color: #B8B9BB;
                overflow-x: hidden;
            }
            
            .sidebar {
                background: linear-gradient(180deg, #1B1D1F 0%, #0F1113 100%);
                border-right: 2px solid #D4AF37;
                height: 100vh;
                position: fixed;
                width: 280px;
                padding: 30px 20px;
                z-index: 1000;
                box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
            }
            
            .logo {
                font-size: 26px;
                font-weight: 700;
                color: #D4AF37;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 1px solid #2A2D30;
                text-align: center;
            }
            
            .nav-item {
                color: #B8B9BB;
                padding: 15px 20px;
                margin: 8px 0;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                border-left: 3px solid transparent;
            }
            
            .nav-item:hover {
                background-color: rgba(212, 175, 55, 0.1);
                color: #FFCF66;
                border-left-color: #D4AF37;
                transform: translateX(5px);
            }
            
            .main-content {
                margin-left: 280px;
                padding: 20px;
                min-height: 100vh;
            }
            
            .header {
                background: linear-gradient(135deg, #1B1D1F 0%, #2A2D30 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                border-left: 5px solid #D4AF37;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            }
            
            .header h1 {
                color: #D4AF37;
                margin: 0;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            
            .header p {
                color: #B8B9BB;
                margin: 15px 0 0 0;
                font-size: 14px;
                opacity: 0.8;
            }
            
            .card {
                background: linear-gradient(145deg, #1B1D1F 0%, #252830 100%);
                border-radius: 15px;
                padding: 25px;
                margin: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
                border: 1px solid #2A2D30;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #FFCF66);
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            /* Mobile responsive */
            @media (max-width: 1200px) {
                .chart-grid {
                    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
                }
            }
            
            @media (max-width: 900px) {
                .sidebar {
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                }
                
                .main-content {
                    margin-left: 0;
                    padding: 15px;
                }
                
                .chart-grid {
                    grid-template-columns: 1fr;
                    gap: 15px;
                }
                
                .card {
                    margin: 8px;
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 24px;
                }
            }
            
            @media (max-width: 600px) {
                .header {
                    padding: 20px;
                }
                
                .card {
                    padding: 15px;
                }
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0F1113;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #D4AF37;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #FFCF66;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Main app layout
app.layout = html.Div([
    # Sidebar Navigation
    html.Div([
        html.Div("LexCura Dashboard", className="logo"),
        html.Div([
            html.Div("Overview", className="nav-item"),
            html.Div("Analytics", className="nav-item"),
            html.Div("Reports", className="nav-item"),
            html.Div("Settings", className="nav-item"),
            html.Div("Security", className="nav-item"),
        ])
    ], className="sidebar"),
    
    # Main Content Area
    html.Div([
        # Header Section
        html.Div([
            html.H1("Executive Business Intelligence Dashboard"),
            html.P(f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
        ], className="header"),
        
        # Charts Grid Container
        html.Div([
            # Financial Impact Chart
            html.Div([
                dcc.Graph(
                    id='financial-impact-chart',
                    figure=create_financial_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Deadline Tracker Chart
            html.Div([
                dcc.Graph(
                    id='deadline-tracker-chart',
                    figure=create_deadline_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Alert Severity Chart
            html.Div([
                dcc.Graph(
                    id='alert-severity-chart',
                    figure=create_alert_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Historical Trends Chart
            html.Div([
                dcc.Graph(
                    id='historical-trends-chart',
                    figure=create_historical_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Growth vs Decline Chart
            html.Div([
                dcc.Graph(
                    id='growth-decline-chart',
                    figure=create_growth_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Performance Comparison Chart
            html.Div([
                dcc.Graph(
                    id='performance-comparison-chart',
                    figure=create_performance_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Risk & Compliance Gauge
            html.Div([
                dcc.Graph(
                    id='risk-compliance-gauge',
                    figure=create_risk_gauge(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
            # Projection & Forecast Chart
            html.Div([
                dcc.Graph(
                    id='projection-forecast-chart',
                    figure=create_projection_chart(),
                    config={'displayModeBar': False, 'responsive': True},
                    style={'height': '420px'}
                )
            ], className="card"),
            
        ], className="chart-grid"),
        
        # Auto-refresh interval component
        dcc.Interval(
            id='auto-refresh-interval',
            interval=300000,  # 5 minutes in milliseconds
            n_intervals=0
        ),
        
        # Status indicator
        html.Div([
            html.Div(id='status-indicator', children=[
                html.Span("🟢 ", style={'color': COLORS['success_green']}),
                html.Span("System Online", style={'color': COLORS['neutral_text']})
            ], style={'text-align': 'center', 'padding': '20px', 'font-size': '14px'})
        ])
        
    ], className="main-content")
])

# Callback for auto-refresh functionality
@app.callback(
    [Output('financial-impact-chart', 'figure'),
     Output('deadline-tracker-chart', 'figure'),
     Output('alert-severity-chart', 'figure'),
     Output('historical-trends-chart', 'figure'),
     Output('growth-decline-chart', 'figure'),
     Output('performance-comparison-chart', 'figure'),
     Output('risk-compliance-gauge', 'figure'),
     Output('projection-forecast-chart', 'figure'),
     Output('status-indicator', 'children')],
    [Input('auto-refresh-interval', 'n_intervals')]
)
def update_dashboard_charts(n_intervals):
    """
    Auto-refresh all charts every 5 minutes
    """
    try:
        # Regenerate data with slight variations for realistic updates
        global data
        
        # Add small random variations to existing data
        if n_intervals > 0:
            # Vary financial data slightly
            for i in range(len(data['financial']['current'])):
                variation = random.uniform(-0.05, 0.05)  # ±5% variation
                data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
            
            # Vary risk score slightly
            data['risk_score'] = max(0, min(100, data['risk_score'] + random.uniform(-3, 3)))
        
        # Create status indicator
        current_time = datetime.now().strftime('%I:%M %p')
        status_indicator = [
            html.Span("🟢 ", style={'color': COLORS['success_green']}),
            html.Span(f"Live Data - Updated at {current_time}", 
                     style={'color': COLORS['neutral_text']})
        ]
        
        return (
            create_financial_chart(),
            create_deadline_chart(),
            create_alert_chart(),
            create_historical_chart(),
            create_growth_chart(),
            create_performance_chart(),
            create_risk_gauge(),
            create_projection_chart(),
            status_indicator
        )
        
    except Exception as e:
        print(f"Error in dashboard update callback: {str(e)}")
        # Return current figures if update fails
        error_status = [
            html.Span("🔴 ", style={'color': COLORS['danger_red']}),
            html.Span("Update Error - Using Cached Data", 
                     style={'color': COLORS['neutral_text']})
        ]
        
        return (
            create_financial_chart(),
            create_deadline_chart(),
            create_alert_chart(),
            create_historical_chart(),
            create_growth_chart(),
            create_performance_chart(),
            create_risk_gauge(),
            create_projection_chart(),
            error_status
        )

# Health check endpoint for Render
@app.server.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

# Main application entry point
if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 8050))
    
    # Run the app
    app.run_server(
        debug=False,  # Never use debug=True in production
        host='0.0.0.0',  # Required for Render
        port=port
    )

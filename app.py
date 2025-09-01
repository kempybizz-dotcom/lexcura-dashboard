import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math
import os
import hashlib

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server

# Authentication configuration
USERS = {
    "admin": "dashboard2024",
    "client": "lexcura2024"
}

# Color palette
COLORS = {
    'charcoal': '#0F1113',
    'dark_grey': '#1B1D1F',
    'gold_primary': '#D4AF37',
    'highlight_gold': '#FFCF66',
    'neutral_text': '#B8B9BB',
    'success_green': '#3DBC6B',
    'danger_red': '#E4574C',
    'warning_orange': '#F4A261',
    'deep_blue': '#2E3A59'
}

# Session store for authentication
session_store = {}

def generate_session_id():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def verify_credentials(username, password):
    return USERS.get(username) == password

def is_authenticated(session_id):
    return session_id in session_store

def generate_sample_data():
    try:
        random.seed(42)
        
        # Financial data
        financial_data = {
            'categories': ['Q4 Revenue', 'Operating Costs', 'Net Profit', 'R&D Investment', 'Marketing ROI', 'Legal Services'],
            'current': [4250000, -1850000, 2400000, -680000, 920000, -340000],
            'previous': [3800000, -1920000, 1880000, -720000, 780000, -290000],
            'targets': [4500000, -1750000, 2750000, -650000, 1100000, -320000]
        }
        
        # Deadline data
        deadline_data = {
            'tasks': ['Q4 Financial Audit', 'Cloud Migration', 'Compliance Review', 'Budget 2025', 'Security Upgrade', 'Client Onboarding'],
            'days_left': [2, 18, 1, 15, 25, 8],
            'progress': [92, 35, 98, 55, 20, 75],
            'priority': ['Critical', 'High', 'Critical', 'Medium', 'Low', 'High']
        }
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        # Alert data
        alert_data = {
            'severity': ['Critical', 'High', 'Medium', 'Low', 'Info'],
            'count': [5, 12, 18, 25, 40]
        }
        
        # Historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        historical_dates = []
        current_date = start_date
        while current_date <= end_date:
            historical_dates.append(current_date)
            current_date += timedelta(days=1)
        
        historical_performance = []
        for i, date in enumerate(historical_dates):
            trend = (i / len(historical_dates)) * 300
            seasonal = 150 * math.sin(2 * math.pi * i / 365)
            noise = random.uniform(-75, 75)
            value = 1000 + trend + seasonal + noise
            historical_performance.append(max(0, value))
        
        historical_data = {
            'dates': historical_dates,
            'performance': historical_performance,
            'target': 1200
        }
        
        # Growth data
        growth_data = {
            'quarters': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
            'revenue_growth': [15, 22, 18, 28],
            'market_expansion': [8, 12, 15, 20]
        }
        
        # Performance KPIs
        performance_data = {
            'kpis': ['Legal Efficiency', 'Client Satisfaction', 'Response Time', 'Cost Optimization', 'Revenue Growth', 'Market Position'],
            'current_score': [88, 94, 82, 91, 85, 78],
            'target_score': [92, 96, 88, 95, 90, 85],
            'industry_avg': [75, 87, 78, 83, 80, 72]
        }
        
        risk_score = random.randint(45, 75)
        
        # Projection data
        future_dates = []
        current_month = datetime.now().replace(day=1)
        for i in range(12):
            future_dates.append(current_month + timedelta(days=32*i))
        
        forecast_values = []
        lower_confidence = []
        upper_confidence = []
        
        base_forecast = 2000
        growth_rate = 0.06
        
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
        print(f"Error generating data: {str(e)}")
        return {
            'financial': {'categories': ['Revenue'], 'current': [1000000], 'previous': [900000], 'targets': [1100000]},
            'deadlines': {'tasks': ['Sample Task'], 'days_left': [5], 'progress': [50], 'urgency': ['Normal'], 'priority': ['Medium']},
            'alerts': {'severity': ['Info'], 'count': [10]},
            'historical': {'dates': [datetime.now()], 'performance': [1000], 'target': 1200},
            'growth': {'quarters': ['Q1'], 'revenue_growth': [15], 'market_expansion': [8]},
            'performance': {'kpis': ['Performance'], 'current_score': [80], 'target_score': [90], 'industry_avg': [75]},
            'risk_score': 70,
            'projections': {'dates': [datetime.now()], 'forecast': [1500], 'lower_confidence': [1400], 'upper_confidence': [1600]}
        }

# Initialize data
data = generate_sample_data()

def get_base_layout(title):
    return {
        'title': {
            'text': title,
            'font': {'color': COLORS['neutral_text'], 'size': 20, 'family': 'Inter'},
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
            'bgcolor': 'rgba(0,0,0,0.3)',
            'bordercolor': COLORS['gold_primary'],
            'borderwidth': 1
        },
        'xaxis': {'color': COLORS['neutral_text'], 'gridcolor': '#2A2D30'},
        'yaxis': {'color': COLORS['neutral_text'], 'gridcolor': '#2A2D30'},
        'transition': {'duration': 800, 'easing': 'cubic-in-out'},
        'hovermode': 'x unified'
    }

# Chart creation functions
def create_financial_chart():
    try:
        fig = go.Figure()
        
        colors_current = []
        for x in data['financial']['current']:
            if x > 0:
                colors_current.append(COLORS['success_green'])
            else:
                colors_current.append(COLORS['danger_red'])
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=COLORS['gold_primary'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<extra></extra>'
        ))
        
        layout = get_base_layout('Financial Performance Analysis')
        layout['yaxis']['tickformat'] = '$,.0f'
        layout['barmode'] = 'group'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in financial chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Financial Performance Analysis'))
        return fig

def create_deadline_chart():
    try:
        fig = go.Figure()
        
        priority_colors = {
            'Critical': COLORS['danger_red'],
            'High': COLORS['warning_orange'],
            'Medium': COLORS['deep_blue'],
            'Low': COLORS['success_green']
        }
        
        colors = [priority_colors.get(priority, COLORS['neutral_text']) for priority in data['deadlines']['priority']]
        
        fig.add_trace(go.Bar(
            y=data['deadlines']['tasks'],
            x=data['deadlines']['days_left'],
            orientation='h',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>Days Left: %{x}<br>Priority: %{text}<extra></extra>',
            text=data['deadlines']['priority']
        ))
        
        layout = get_base_layout('Project Timeline Tracker')
        layout['xaxis']['title'] = 'Days Remaining'
        layout['height'] = 450
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in deadline chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Project Timeline Tracker'))
        return fig

def create_alert_chart():
    try:
        severity_colors = [COLORS['danger_red'], COLORS['warning_orange'], COLORS['deep_blue'], COLORS['success_green'], '#4A90E2']
        
        fig = go.Figure(go.Pie(
            labels=data['alerts']['severity'],
            values=data['alerts']['count'],
            hole=0.6,
            marker_colors=severity_colors,
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            textinfo='label+percent',
            textfont={'color': 'white', 'size': 12}
        ))
        
        total_alerts = sum(data['alerts']['count'])
        fig.add_annotation(
            text=f"Total<br><b>{total_alerts}</b><br>Alerts",
            x=0.5, y=0.5,
            font={'size': 16, 'color': COLORS['neutral_text']},
            showarrow=False
        )
        
        layout = get_base_layout('Alert Distribution')
        layout['showlegend'] = False
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in alert chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Alert Distribution'))
        return fig

def create_historical_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['performance'],
            mode='lines',
            line={'color': COLORS['gold_primary'], 'width': 3},
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.3)',
            name='Performance',
            hovertemplate='<b>%{x}</b><br>Value: %{y:,.1f}<extra></extra>'
        ))
        
        fig.add_hline(
            y=data['historical']['target'],
            line_dash="dash",
            line_color=COLORS['success_green'],
            line_width=2,
            annotation_text="Target"
        )
        
        layout = get_base_layout('Historical Performance Trends')
        layout['xaxis']['title'] = 'Date'
        layout['yaxis']['title'] = 'Performance Score'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in historical chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Historical Performance Trends'))
        return fig

def create_growth_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['revenue_growth'],
            name='Revenue Growth',
            marker_color=COLORS['success_green'],
            hovertemplate='<b>%{x}</b><br>Growth: %{y}%<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['market_expansion'],
            name='Market Expansion',
            marker_color=COLORS['gold_primary'],
            hovertemplate='<b>%{x}</b><br>Expansion: %{y}%<extra></extra>'
        ))
        
        layout = get_base_layout('Growth Analysis')
        layout['yaxis']['title'] = 'Growth Rate (%)'
        layout['yaxis']['ticksuffix'] = '%'
        layout['barmode'] = 'group'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in growth chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Growth Analysis'))
        return fig

def create_performance_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['current_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Current',
            line={'color': COLORS['gold_primary'], 'width': 3},
            fillcolor='rgba(212, 175, 55, 0.4)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Target',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'}
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['industry_avg'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Industry Avg',
            line={'color': COLORS['neutral_text'], 'width': 1, 'dash': 'dash'}
        ))
        
        layout = get_base_layout('Performance KPIs')
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
        print(f"Error in performance chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Performance KPIs'))
        return fig

def create_risk_gauge():
    try:
        if data['risk_score'] <= 30:
            gauge_color = COLORS['success_green']
            risk_level = "Low"
        elif data['risk_score'] <= 70:
            gauge_color = COLORS['warning_orange']
            risk_level = "Medium"
        else:
            gauge_color = COLORS['danger_red']
            risk_level = "High"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Score ({risk_level})", 'font': {'color': COLORS['neutral_text']}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': COLORS['neutral_text']},
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(61, 188, 107, 0.3)'},
                    {'range': [30, 70], 'color': 'rgba(244, 162, 97, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(228, 87, 76, 0.3)'}
                ],
                'bordercolor': COLORS['gold_primary'],
                'borderwidth': 2
            },
            number={'font': {'color': COLORS['neutral_text'], 'size': 24}}
        ))
        
        fig.update_layout(
            paper_bgcolor=COLORS['charcoal'],
            plot_bgcolor=COLORS['charcoal'],
            font={'color': COLORS['neutral_text']},
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error in risk gauge: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(paper_bgcolor=COLORS['charcoal'], height=400)
        return fig

def create_projection_chart():
    try:
        fig = go.Figure()
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['upper_confidence'],
            mode='lines',
            line={'width': 0},
            showlegend=False,
            name='Upper'
        ))
        
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['lower_confidence'],
            mode='lines',
            line={'width': 0},
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.2)',
            name='Confidence Range'
        ))
        
        # Main forecast line
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['forecast'],
            mode='lines+markers',
            line={'color': COLORS['gold_primary'], 'width': 4},
            marker={'size': 8, 'color': COLORS['highlight_gold']},
            name='Forecast',
            hovertemplate='<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
        ))
        
        layout = get_base_layout('Revenue Projection')
        layout['xaxis']['title'] = 'Month'
        layout['yaxis']['title'] = 'Revenue ($)'
        layout['yaxis']['tickformat'] = '$,.0f'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in projection chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Revenue Projection'))
        return fig

# Logo intro screen
def get_logo_intro():
    return html.Div([
        html.Div([
            html.Img(
                src="/assets/lexcura_logo.png", 
                id="intro-logo",
                style={
                    'width': '200px',
                    'height': 'auto',
                    'opacity': '0',
                    'transform': 'scale(0.8)',
                    'transition': 'all 1.5s ease'
                }
            ),
            html.H1(
                "LexCura Executive Dashboard",
                id="intro-title",
                style={
                    'color': COLORS['gold_primary'],
                    'font-family': 'Inter',
                    'font-weight': '700',
                    'font-size': '32px',
                    'margin-top': '30px',
                    'opacity': '0',
                    'transition': 'all 1s ease 0.5s'
                }
            ),
            html.P(
                "Initializing Business Intelligence Platform...",
                id="intro-subtitle",
                style={
                    'color': COLORS['neutral_text'],
                    'font-family': 'Inter',
                    'font-size': '16px',
                    'margin-top': '15px',
                    'opacity': '0',
                    'transition': 'all 1s ease 1s'
                }
            )
        ], style={
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            'justify-content': 'center',
            'height': '100vh',
            'text-align': 'center'
        }),
        dcc.Interval(id='intro-timer', interval=3500, n_intervals=0, max_intervals=1)
    ], id='intro-screen', style={
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'width': '100%',
        'height': '100%',
        'background': f'linear-gradient(135deg, {COLORS["dark_grey"]}, {COLORS["charcoal"]})',
        'z-index': '9999'
    })

def get_login_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="/assets/lexcura_logo.png", 
                                   style={'width': '120px', 'height': 'auto', 'margin-bottom': '30px'}),
                            html.H2("LexCura Dashboard", 
                                   style={'color': COLORS['gold_primary'], 'font-weight': 'bold'}),
                            html.P("Executive Business Intelligence Platform", 
                                  style={'color': COLORS['neutral_text'], 'margin-bottom': '30px'}),
                            dbc.Form([
                                dbc.Row([
                                    dbc.Label("Username"),
                                    dbc.Input(id="username-input", type="text", placeholder="Enter username"),
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Label("Password"),
                                    dbc.Input(id="password-input", type="password", placeholder="Enter password"),
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Button("Access Dashboard", id="login-button", color="warning", 
                                             className="w-100", 
                                             style={'background-color': COLORS['gold_primary']})
                                ])
                            ]),
                            html.Div(id="login-alert", className="mt-3"),
                            html.Div([
                                html.Small("Demo: admin/dashboard2024 or client/lexcura2024", 
                                         style={'color': COLORS['neutral_text']})
                            ], className="text-center mt-3")
                        ], style={'text-align': 'center'})
                    ])
                ], style={'background-color': COLORS['dark_grey'], 'border': f'2px solid {COLORS["gold_primary"]}'}),
            ], width=6, lg=4)
        ], justify="center", className="min-vh-100 align-items-center"),
        dcc.Store(id='session-store'),
        dcc.Store(id='show-intro', data={'show': False})
    ], fluid=True, style={'background-color': COLORS['charcoal']})

def get_sidebar():
    return html.Div([
        html.Div([
            html.Img(src="/assets/lexcura_logo.png", style={'width': '40px', 'height': 'auto', 'margin-right': '15px'}),
            html.Span("LexCura Dashboard", style={'font-size': '20px', 'font-weight': '700'})
        ], className="logo"),
        
        html.Div([
            html.Div("Overview", id="nav-overview", className="nav-item"),
            html.Div("Analytics", id="nav-analytics", className="nav-item"),
            html.Div("Reports", id="nav-reports", className="nav-item"),
            html.Div("Google Slides", id="nav-slides", className="nav-item"),
            html.Div("Archive", id="nav-archive", className="nav-item"),
            html.Div("Settings", id="nav-settings", className="nav-item"),
            html.Hr(style={'border-color': COLORS['gold_primary'], 'margin': '20px 0'}),
            html.Div("Logout", id="logout-btn", className="nav-item", 
                    style={'color': COLORS['danger_red']})
        ])
    ], className="sidebar")

def get_header(title):
    return html.Div([
        html.H1(title),
        html.P(f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    ], className="header")

def get_dashboard_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Executive Business Intelligence Dashboard"),
            
            # Control panel
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.ButtonGroup([
                                dbc.Button("Export PDF", id="export-pdf-btn", color="warning"),
                                dbc.Button("Refresh Data", id="refresh-data-btn", color="secondary"),
                                dbc.Button("Full Screen", id="fullscreen-btn", color="info")
                            ])
                        ], width=8),
                        dbc.Col([
                            html.Div(id='status-indicator', children=[
                                html.Span("● ", style={'color': COLORS['success_green'], 'font-size': '16px'}),
                                html.Span("System Online", style={'color': COLORS['neutral_text']})
                            ], style={'text-align': 'right', 'padding': '8px 0'})
                        ], width=4)
                    ])
                ])
            ], className="mb-4"),
            
            # Charts Grid
            html.Div([
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='performance-comparison-chart',
                            figure=create_performance_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='risk-compliance-gauge',
                            figure=create_risk_gauge(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='projection-forecast-chart',
                            figure=create_projection_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
            ], className="chart-grid"),
            
            dcc.Interval(
                id='auto-refresh-interval',
                interval=300000,
                n_intervals=0
            ),
            
            dcc.Download(id="download-pdf")
            
        ], className="main-content")
    ])

def get_archive_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Document Archive"),
            html.H3("Historical Reports", style={'color': COLORS['gold_primary']}),
            html.P("Archive system ready for integration", style={'color': COLORS['neutral_text']})
        ], className="main-content")
    ])

def get_google_slides_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Google Slides Integration"),
            html.H3("Live Presentation", style={'color': COLORS['gold_primary']}),
            html.Iframe(
                src="https://docs.google.com/presentation/d/e/YOUR_PRESENTATION_ID/embed",
                style={
                    'width': '100%',
                    'height': '600px',
                    'border': f'2px solid {COLORS["gold_primary"]}',
                    'border-radius': '10px'
                }
            )
        ], className="main-content")
    ])

def get_settings_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Dashboard Settings"),
            html.H3("Configuration Panel", style={'color': COLORS['gold_primary']}),
            html.P("Settings interface ready", style={'color': COLORS['neutral_text']})
        ], className="main-content")
    ])

# Enhanced CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>LexCura Executive Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background-color: #0F1113;
                color: #B8B9BB;
                overflow-x: hidden;
            }
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes slideInRight {
                from { opacity: 0; transform: translateX(50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            @keyframes fadeInScale {
                from { opacity: 0; transform: scale(0.8); }
                to { opacity: 1; transform: scale(1); }
            }
            
            .intro-logo-animate {
                opacity: 1 !important;
                transform: scale(1) !important;
            }
            
            .intro-title-animate {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
            
            .intro-subtitle-animate {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
            
            .sidebar {
                background: linear-gradient(180deg, #1B1D1F 0%, #0F1113 100%);
                border-right: 3px solid #D4AF37;
                height: 100vh;
                position: fixed;
                width: 280px;
                padding: 30px 20px;
                z-index: 1000;
                box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4);
                animation: slideInRight 0.8s ease-out;
            }
            
            .logo {
                font-size: 18px;
                font-weight: 700;
                color: #D4AF37;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #2A2D30;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeInScale 0.6s ease-out 0.2s both;
            }
            
            .nav-item {
                color: #B8B9BB;
                padding: 16px 20px;
                margin: 6px 0;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                border-left: 4px solid transparent;
                animation: fadeInUp 0.5s ease-out both;
            }
            
            .nav-item:hover {
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(255, 207, 102, 0.1));
                color: #FFCF66;
                border-left-color: #D4AF37;
                transform: translateX(6px);
                box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
            }
            
            .nav-item.active {
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(255, 207, 102, 0.15));
                color: #FFCF66;
                border-left-color: #D4AF37;
                transform: translateX(6px);
            }
            
            .main-content {
                margin-left: 280px;
                padding: 20px;
                min-height: 100vh;
                animation: fadeInUp 0.8s ease-out 0.3s both;
            }
            
            .header {
                background: linear-gradient(135deg, #1B1D1F 0%, #2A2D30 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                border-left: 5px solid #D4AF37;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
                animation: fadeInScale 0.8s ease-out 0.4s both;
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
            
            .chart-card {
                background: linear-gradient(145deg, #1B1D1F 0%, #252830 100%);
                border-radius: 15px;
                padding: 25px;
                margin: 15px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
                border: 1px solid #2A2D30;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .chart-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #FFCF66);
            }
            
            .chart-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
                border-color: #D4AF37;
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            ._dash-loading {
                color: #D4AF37 !important;
            }
            
            .btn {
                transition: all 0.3s ease;
                font-weight: 600;
                border-radius: 8px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            }
            
            @media (max-width: 1200px) {
                .chart-grid {
                    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
                }
            }
            
            @media (max-width: 900px) {
                .sidebar {
                    transform: translateX(-100%);
                }
                
                .main-content {
                    margin-left: 0;
                    padding: 15px;
                }
                
                .chart-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 24px;
                }
            }
            
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0F1113;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #D4AF37, #FFCF66);
                border-radius: 4px;
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
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() {
                    const logo = document.getElementById('intro-logo');
                    const title = document.getElementById('intro-title');
                    const subtitle = document.getElementById('intro-subtitle');
                    
                    if (logo) logo.classList.add('intro-logo-animate');
                    setTimeout(function() {
                        if (title) title.classList.add('intro-title-animate');
                    }, 500);
                    setTimeout(function() {
                        if (subtitle) subtitle.classList.add('intro-subtitle-animate');
                    }, 1000);
                }, 200);
            });
        </script>
    </body>
</html>
'''

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Store(id='show-intro', storage_type='session', data={'show': False}),
    html.Div(id='page-content')
])

# Page routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('intro-timer', 'n_intervals')],
    [State('session-store', 'data'), State('show-intro', 'data')]
)
def display_page(pathname, intro_intervals, session_data, intro_data):
    session_id = session_data.get('session_id') if session_data else None
    
    if not session_id or not is_authenticated(session_id):
        return get_login_layout()
    
    if intro_data and not intro_data.get('intro_shown', False):
        if intro_intervals == 0:
            return get_logo_intro()
    
    if pathname == '/archive':
        return get_archive_layout()
    elif pathname == '/slides':
        return get_google_slides_layout()
    elif pathname == '/settings':
        return get_settings_layout()
    else:
        return get_dashboard_layout()

# Login callback
@app.callback(
    [Output('session-store', 'data'),
     Output('login-alert', 'children'),
     Output('url', 'pathname'),
     Output('show-intro', 'data')],
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'), State('password-input', 'value')]
)
def handle_login(n_clicks, username, password):
    if n_clicks and username and password:
        if verify_credentials(username, password):
            session_id = generate_session_id()
            session_store[session_id] = {'username': username, 'login_time': datetime.now()}
            return (
                {'session_id': session_id, 'username': username},
                dbc.Alert("Login successful!", color="success"),
                "/",
                {'show': True, 'intro_shown': False}
            )
        else:
            return (
                {},
                dbc.Alert("Invalid credentials", color="danger"),
                "/login",
                {'show': False, 'intro_shown': True}
            )
    return {}, "", "/login", {'show': False, 'intro_shown': True}

# Intro completion callback
@app.callback(
    [Output('show-intro', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    Input('intro-timer', 'n_intervals'),
    State('show-intro', 'data'),
    prevent_initial_call=True
)
def complete_intro(n_intervals, intro_data):
    if n_intervals > 0 and intro_data and not intro_data.get('intro_shown', False):
        return {'show': True, 'intro_shown': True}, "/"
    return dash.no_update, dash.no_update

# Logout callback
@app.callback(
    [Output('session-store', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True),
     Output('show-intro', 'data', allow_duplicate=True)],
    Input('logout-btn', 'n_clicks'),
    State('session-store', 'data'),
    prevent_initial_call=True
)
def handle_logout(n_clicks, session_data):
    if n_clicks and session_data:
        session_id = session_data.get('session_id')
        if session_id in session_store:
            del session_store[session_id]
    return {}, "/login", {'show': False, 'intro_shown': True}

# Navigation callbacks
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('nav-overview', 'n_clicks'),
     Input('nav-analytics', 'n_clicks'),
     Input('nav-reports', 'n_clicks'),
     Input('nav-slides', 'n_clicks'),
     Input('nav-archive', 'n_clicks'),
     Input('nav-settings', 'n_clicks')],
    prevent_initial_call=True
)
def handle_navigation(overview, analytics, reports, slides, archive, settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "/"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    routes = {
        'nav-overview': "/",
        'nav-analytics': "/analytics", 
        'nav-reports': "/reports",
        'nav-slides': "/slides",
        'nav-archive': "/archive",
        'nav-settings': "/settings"
    }
    return routes.get(button_id, "/")

# Dashboard refresh callback
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
    [Input('auto-refresh-interval', 'n_intervals'),
     Input('refresh-data-btn', 'n_clicks')]
)
def update_dashboard_charts(n_intervals, refresh_clicks):
    try:
        global data
        
        if n_intervals > 0 or refresh_clicks:
            # Add small variations for realistic updates
            for i in range(len(data['financial']['current'])):
                variation = random.uniform(-0.02, 0.03)
                data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
            
            risk_change = random.uniform(-1, 1)
            data['risk_score'] = max(0, min(100, data['risk_score'] + risk_change))
        
        current_time = datetime.now().strftime('%I:%M %p')
        status_indicator = [
            html.Span("● ", style={'color': COLORS['success_green'], 'font-size': '16px'}),
            html.Span(f"Updated at {current_time}", style={'color': COLORS['neutral_text']})
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
        print(f"Error updating dashboard: {str(e)}")
        error_status = [
            html.Span("● ", style={'color': COLORS['danger_red'], 'font-size': '16px'}),
            html.Span("Update Error", style={'color': COLORS['neutral_text']})
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

# Export callback
@app.callback(
    Output("download-pdf", "data"),
    Input("export-pdf-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_report(n_clicks):
    if n_clicks:
        try:
            report_text = f"""LexCura Executive Dashboard Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Financial Summary:
- Revenue: ${data['financial']['current'][0]:,.0f}
- Risk Score: {data['risk_score']}/100
- Total Alerts: {sum(data['alerts']['count'])}

Full dashboard analytics available online.
"""
            return dict(content=report_text, filename=f"LexCura_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        except Exception as e:
            print(f"Export error: {str(e)}")
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=port
    )
                            id='financial-impact-chart',
                            figure=create_financial_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='deadline-tracker-chart',
                            figure=create_deadline_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='alert-severity-chart',
                            figure=create_alert_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='historical-trends-chart',
                            figure=create_historical_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(
                            id='growth-decline-chart',
                            figure=create_growth_chart(),
                            config={'displayModeBar': False, 'responsive': True},
                            style={'height': '420px'}
                        )
                    ], color=COLORS['gold_primary'])
                ], className="chart-card"),
                
                html.Div([
                    dcc.Loading([
                        dcc.Graph(

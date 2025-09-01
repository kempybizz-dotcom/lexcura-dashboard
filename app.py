import dash
from dash import dcc, html, Input, Output, callback, State, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math
import os
import json
import hashlib
import base64
from urllib.parse import parse_qs
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
import plotly.io as pio

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server

# Authentication configuration
USERS = {
    "admin": "dashboard2024",  # Simple test credentials
    "client": "lexcura2024"    # Client credentials
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
    'warning_orange': '#F4A261'
}

# Session store for authentication
session_store = {}

def generate_session_id():
    """Generate a secure session ID"""
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def verify_credentials(username, password):
    """Verify user credentials"""
    return USERS.get(username) == password

def is_authenticated(session_data, user_data=None):
    """Enhanced authentication check with multiple fallbacks"""
    if not session_data and not user_data:
        return False
    
    # Check session store data
    if session_data:
        if session_data.get('authenticated') == True:
            return True
        session_id = session_data.get('session_id')
        if session_id and session_id in session_store:
            return True
    
    # Check user data
    if user_data:
        session_id = user_data.get('session_id')
        if session_id and session_id in session_store:
            return True
    
    return False

# Enhanced data generation with better error handling
def generate_sample_data():
    try:
        random.seed(42)
        
        # Financial data
        financial_data = {
            'categories': ['Revenue', 'Operating Costs', 'Net Profit', 'Investments', 'Returns'],
            'current': [2850000, -1320000, 1530000, -480000, 720000],
            'previous': [2600000, -1450000, 1150000, -520000, 580000]
        }
        
        # Deadline data
        deadline_data = {
            'tasks': ['Q4 Financial Report', 'Infrastructure Upgrade', 'Compliance Audit', 'Budget Planning', 'Security Assessment'],
            'days_left': [3, 15, 1, 12, 8],
            'progress': [85, 45, 95, 60, 70]
        }
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        # Alert data
        alert_data = {
            'severity': ['Critical', 'Warning', 'Info'],
            'count': [8, 24, 42]
        }
        
        # Historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        historical_dates = []
        current_date = start_date
        while current_date <= end_date:
            historical_dates.append(current_date)
            current_date += timedelta(days=1)
        
        base_value = 1000
        historical_performance = []
        for i, date in enumerate(historical_dates):
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
        
        # Growth data
        growth_data = {
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            'growth_rate': [12, 18, 15, 22, 28, 25, 30, 35],
            'decline_rate': [5, 8, 4, 6, 9, 7, 8, 6]
        }
        
        # Performance data
        performance_data = {
            'kpis': ['Operational Efficiency', 'Quality Score', 'Response Time', 'Cost Optimization', 'Customer Satisfaction'],
            'current_score': [85, 92, 78, 88, 91],
            'target_score': [90, 95, 85, 90, 95],
            'industry_avg': [75, 85, 80, 82, 87]
        }
        
        risk_score = 68
        
        # Projection data
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
        
        # Google Slides archive data (mock)
        archive_data = [
            {
                'date': '2024-12-01',
                'title': 'Q4 Executive Summary',
                'url': 'https://docs.google.com/presentation/d/1example1/edit',
                'thumbnail': '/assets/slide_thumb_1.png'
            },
            {
                'date': '2024-11-15',
                'title': 'November Performance Review',
                'url': 'https://docs.google.com/presentation/d/1example2/edit',
                'thumbnail': '/assets/slide_thumb_2.png'
            },
            {
                'date': '2024-11-01',
                'title': 'Monthly Financial Report',
                'url': 'https://docs.google.com/presentation/d/1example3/edit',
                'thumbnail': '/assets/slide_thumb_3.png'
            }
        ]
        
        return {
            'financial': financial_data,
            'deadlines': deadline_data,
            'alerts': alert_data,
            'historical': historical_data,
            'growth': growth_data,
            'performance': performance_data,
            'risk_score': risk_score,
            'projections': projection_data,
            'archive': archive_data
        }
        
    except Exception as e:
        print(f"Critical error in data generation: {str(e)}")
        # Minimal fallback data
        return {
            'financial': {'categories': ['Revenue'], 'current': [1000000], 'previous': [900000]},
            'deadlines': {'tasks': ['Sample Task'], 'days_left': [5], 'progress': [50], 'urgency': ['Normal']},
            'alerts': {'severity': ['Info'], 'count': [10]},
            'historical': {'dates': [datetime.now()], 'performance': [1000], 'target': 1200},
            'growth': {'months': ['Jan'], 'growth_rate': [15], 'decline_rate': [5]},
            'performance': {'kpis': ['Performance'], 'current_score': [80], 'target_score': [90], 'industry_avg': [75]},
            'risk_score': 70,
            'projections': {'dates': [datetime.now()], 'forecast': [1500], 'lower_confidence': [1400], 'upper_confidence': [1600]},
            'archive': []
        }

# Initialize data
data = generate_sample_data()

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

# Enhanced chart creation with animations
def create_financial_chart():
    try:
        fig = go.Figure()
        
        colors_current = [COLORS['success_green'] if x > 0 else COLORS['danger_red'] for x in data['financial']['current']]
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<br><extra></extra>',
            text=[f"${x:,.0f}" for x in data['financial']['current']],
            textposition='outside',
            marker_line=dict(color='rgba(255,255,255,0.3)', width=1)
        ))
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=COLORS['gold_primary'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<br><extra></extra>',
            marker_line=dict(color='rgba(255,255,255,0.2)', width=1)
        ))
        
        layout = get_base_layout('Financial Impact Analysis')
        layout['yaxis']['tickformat'] = '$,.0f'
        layout['barmode'] = 'group'
        layout['transition'] = {'duration': 800, 'easing': 'cubic-in-out'}
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in financial chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Financial Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Financial Impact Analysis'))
        return fig

def create_deadline_chart():
    try:
        urgency_colors = {
            'Critical': COLORS['danger_red'],
            'Warning': COLORS['warning_orange'], 
            'Normal': COLORS['success_green']
        }
        
        fig = go.Figure()
        
        colors = [urgency_colors.get(urgency, COLORS['neutral_text']) for urgency in data['deadlines']['urgency']]
        
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
        print(f"Error in deadline chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Deadline Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Project Deadline Tracker'))
        return fig

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
        print(f"Error in alert chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Alert Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Alert Severity Distribution'))
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
            fillcolor=f"rgba(212, 175, 55, 0.3)",
            name='Performance Metric',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Performance: %{y:,.1f}<extra></extra>'
        ))
        
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
        print(f"Error in historical chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Historical Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Historical Performance Trends'))
        return fig

def create_growth_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data['growth']['months'],
            y=data['growth']['growth_rate'],
            name='Growth Rate',
            marker_color=COLORS['success_green'],
            hovertemplate='<b>%{x}</b><br>Growth: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['growth_rate']],
            textposition='outside'
        ))
        
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
        print(f"Error in growth chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Growth Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Growth vs Decline Analysis'))
        return fig

def create_performance_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['current_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Current Performance',
            line_color=COLORS['gold_primary'],
            fillcolor=f"rgba(212, 175, 55, 0.4)",
            hovertemplate='<b>%{theta}</b><br>Current: %{r}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Target',
            line_color=COLORS['success_green'],
            fillcolor=f"rgba(61, 188, 107, 0.2)",
            hovertemplate='<b>%{theta}</b><br>Target: %{r}%<extra></extra>'
        ))
        
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
        print(f"Error in performance chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Performance Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('Performance vs Target KPIs'))
        return fig

def create_risk_gauge():
    try:
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
        print(f"Error in risk gauge: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Risk Gauge Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(
            paper_bgcolor=COLORS['charcoal'],
            plot_bgcolor=COLORS['charcoal'],
            font={'color': COLORS['neutral_text'], 'family': 'Inter'},
            height=400
        )
        return fig

def create_projection_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['upper_confidence'],
            mode='lines',
            line={'width': 0},
            showlegend=False,
            hoverinfo='skip',
            name='Upper Bound'
        ))
        
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
        print(f"Error in projection chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Projection Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(get_base_layout('12-Month Revenue Projection'))
        return fig

# PDF Report Generation
def generate_pdf_report():
    """Generate a PDF report of dashboard data"""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#D4AF37')
        )
        story.append(Paragraph("LexCura Executive Dashboard Report", title_style))
        story.append(Spacer(1, 20))
        
        # Date
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Financial Summary
        story.append(Paragraph("Financial Summary", styles['Heading2']))
        financial_data_table = [
            ['Category', 'Current Period', 'Previous Period', 'Change'],
            ['Revenue', f"${data['financial']['current'][0]:,.0f}", f"${data['financial']['previous'][0]:,.0f}", 
             f"{((data['financial']['current'][0] - data['financial']['previous'][0]) / data['financial']['previous'][0] * 100):.1f}%"]
        ]
        
        table = Table(financial_data_table)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D4AF37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#0F1113')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F5F5F5')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC'))
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Risk Score
        story.append(Paragraph("Risk Assessment", styles['Heading2']))
        story.append(Paragraph(f"Current Risk Score: {data['risk_score']}/100", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

# Login page layout with animations
def get_login_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H2("LexCura Dashboard", className="text-center mb-4", 
                                   style={'color': COLORS['gold_primary'], 'font-weight': 'bold'}),
                            html.Hr(),
                            dbc.Form([
                                dbc.Row([
                                    dbc.Label("Username", html_for="username-input"),
                                    dbc.Input(id="username-input", type="text", placeholder="Enter username",
                                             className="mb-2"),
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Label("Password", html_for="password-input"),
                                    dbc.Input(id="password-input", type="password", placeholder="Enter password",
                                             className="mb-2"),
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("Login", id="login-button", color="warning", 
                                                 className="w-100", 
                                                 style={'background-color': COLORS['gold_primary'],
                                                       'border-color': COLORS['gold_primary'],
                                                       'font-weight': '600',
                                                       'padding': '12px'})
                                    ])
                                ])
                            ]),
                            html.Div(id="login-alert", className="mt-3")
                        ])
                    ])
                ], className="login-card", style={'background-color': COLORS['dark_grey'], 
                                                  'border': f'2px solid {COLORS["gold_primary"]}',
                                                  'border-radius': '15px',
                                                  'box-shadow': '0 10px 30px rgba(0, 0, 0, 0.5)'}),
            ], width=6, lg=4)
        ], justify="center", className="min-vh-100 align-items-center"),
        dcc.Store(id='session-store'),
        dcc.Store(id='current-user')
    ], fluid=True, style={'background-color': COLORS['charcoal']})

# Analytics page layout - Different view of the same data
def get_analytics_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Advanced Analytics"),
            dbc.Container([
                # Key Metrics Cards
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("$2.85M", className="text-warning"),
                                html.P("Total Revenue", className="card-text")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("68", className="text-danger"),
                                html.P("Risk Score", className="card-text")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("74", className="text-info"),
                                html.P("Total Alerts", className="card-text")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("85%", className="text-success"),
                                html.P("Avg Performance", className="card-text")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=3)
                ], className="mb-4"),
                
                # Analytics Charts
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='analytics-financial-chart',
                                figure=create_financial_chart(),
                                config={'displayModeBar': True, 'responsive': True},
                                style={'height': '400px'}
                            )
                        ], className="card")
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='analytics-performance-chart',
                                figure=create_performance_chart(),
                                config={'displayModeBar': True, 'responsive': True},
                                style={'height': '400px'}
                            )
                        ], className="card")
                    ], width=6)
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Reports page layout
def get_reports_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Reports & Exports"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H3("Generate Reports", style={'color': COLORS['gold_primary']}),
                        html.P("Create and download professional reports", style={'color': COLORS['neutral_text']}),
                        html.Hr(style={'border-color': COLORS['gold_primary']}),
                        
                        # Report Options
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("Available Reports"),
                                dbc.ButtonGroup([
                                    dbc.Button("Executive Summary PDF", id="exec-summary-btn", color="warning",
                                              style={'background-color': COLORS['gold_primary'], 'border-color': COLORS['gold_primary']}),
                                    dbc.Button("Financial Report PDF", id="financial-report-btn", color="secondary"),
                                    dbc.Button("Performance Analytics", id="performance-report-btn", color="info")
                                ], className="mb-3"),
                                html.Hr(),
                                html.H6("Report History"),
                                html.Ul([
                                    html.Li(f"Executive Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
                                    html.Li(f"Financial Report - {(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}"),
                                    html.Li(f"Performance Report - {(datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M')}")
                                ], style={'color': COLORS['neutral_text']})
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=8),
                    dbc.Col([
                        # Quick Stats
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("Quick Statistics"),
                                html.P(f"Reports Generated This Month: 12", style={'color': COLORS['neutral_text']}),
                                html.P(f"Last Export: {datetime.now().strftime('%Y-%m-%d')}", style={'color': COLORS['neutral_text']}),
                                html.P(f"Total Data Points: 1,247", style={'color': COLORS['neutral_text']}),
                                html.Hr(),
                                html.Div([
                                    dcc.Graph(
                                        figure=create_risk_gauge(),
                                        config={'displayModeBar': False},
                                        style={'height': '300px'}
                                    )
                                ])
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=4)
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Settings page layout
def get_settings_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Dashboard Settings"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        # Display Settings
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("Display Settings"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Refresh Interval"),
                                        dcc.Dropdown(
                                            id="refresh-interval-dropdown",
                                            options=[
                                                {"label": "1 minute", "value": 60000},
                                                {"label": "5 minutes", "value": 300000},
                                                {"label": "10 minutes", "value": 600000},
                                                {"label": "30 minutes", "value": 1800000}
                                            ],
                                            value=300000,
                                            style={'color': '#000'}
                                        )
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Label("Theme"),
                                        dcc.Dropdown(
                                            id="theme-dropdown",
                                            options=[
                                                {"label": "Dark Gold (Current)", "value": "dark_gold"},
                                                {"label": "Light Mode", "value": "light"},
                                                {"label": "Blue Theme", "value": "blue"}
                                            ],
                                            value="dark_gold",
                                            style={'color': '#000'}
                                        )
                                    ], width=6)
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Checklist(
                                            options=[
                                                {"label": "Show animations", "value": "animations"},
                                                {"label": "Auto-refresh", "value": "auto_refresh"},
                                                {"label": "Sound notifications", "value": "sound"}
                                            ],
                                            value=["animations", "auto_refresh"],
                                            id="settings-checklist"
                                        )
                                    ])
                                ])
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=8),
                    dbc.Col([
                        # System Info
                        dbc.Card([
                            dbc.CardBody([
                                html.H5("System Information"),
                                html.P(f"Dashboard Version: 2.1.0", style={'color': COLORS['neutral_text']}),
                                html.P(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", style={'color': COLORS['neutral_text']}),
                                html.P(f"Data Sources: 8 Active", style={'color': COLORS['neutral_text']}),
                                html.P(f"Uptime: 99.9%", style={'color': COLORS['success_green']}),
                                html.Hr(),
                                dbc.Button("Clear Cache", color="danger", size="sm", className="me-2"),
                                dbc.Button("Reset Settings", color="warning", size="sm")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}'})
                    ], width=4)
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Archive page layout
def get_archive_layout():
    archive_cards = []
    for item in data['archive']:
        card = dbc.Card([
            dbc.CardImg(src="/assets/lexcura_logo.png", top=True, style={'height': '200px', 'object-fit': 'cover'}),
            dbc.CardBody([
                html.H5(item['title'], className="card-title"),
                html.P(f"Created: {item['date']}", className="card-text text-muted"),
                dbc.Button("Open Presentation", href=item['url'], target="_blank", 
                          color="warning", style={'background-color': COLORS['gold_primary'],
                                                'border-color': COLORS['gold_primary']})
            ])
        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}',
                 'margin-bottom': '20px'})
        archive_cards.append(dbc.Col(card, width=12, md=6, lg=4))
    
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Archive - Historical Reports"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H3("Google Slides Archive", style={'color': COLORS['gold_primary']}),
                        html.P("Access all historical presentation reports", style={'color': COLORS['neutral_text']}),
                        html.Hr(style={'border-color': COLORS['gold_primary']}),
                        dbc.Row(archive_cards)
                    ])
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Google Slides integration layout
def get_google_slides_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Live Google Slides"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H3("Current Presentation", style={'color': COLORS['gold_primary']}),
                        html.P("View and interact with the latest presentation", style={'color': COLORS['neutral_text']}),
                        html.Hr(style={'border-color': COLORS['gold_primary']}),
                        html.Div([
                            html.Iframe(
                                src="https://docs.google.com/presentation/d/e/YOUR_PRESENTATION_ID/embed?start=false&loop=false&delayms=3000",
                                style={
                                    'width': '100%',
                                    'height': '600px',
                                    'border': f'2px solid {COLORS["gold_primary"]}',
                                    'border-radius': '10px'
                                }
                            )
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Open in New Tab", id="open-slides-btn", color="warning",
                                          style={'background-color': COLORS['gold_primary'],
                                                'border-color': COLORS['gold_primary']})
                            ], width=6),
                            dbc.Col([
                                dbc.Button("Download PDF", id="download-slides-btn", color="secondary")
                            ], width=6)
                        ])
                    ])
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

def get_sidebar():
    """Enhanced sidebar with Google Slides integration"""
    return html.Div([
        html.Div([
            html.Div("LexCura", style={'font-size': '28px', 'font-weight': '700', 'color': COLORS['gold_primary']}),
            html.Div("Executive Dashboard", style={'font-size': '14px', 'color': COLORS['neutral_text'], 'opacity': '0.8'})
        ], className="logo-enhanced"),
        
        # System Status Card
        dbc.Card([
            dbc.CardBody([
                html.H6("System Status", style={'color': COLORS['gold_primary'], 'margin-bottom': '10px'}),
                html.Div([
                    html.Span("● ", className="status-dot", style={'color': COLORS['success_green']}),
                    html.Small("Online", style={'color': COLORS['success_green']})
                ], className="mb-1"),
                html.Div([
                    html.Small(f"Uptime: 99.9%", style={'color': COLORS['neutral_text']})
                ]),
                html.Div([
                    html.Small(f"Last Update: {datetime.now().strftime('%H:%M')}", 
                              style={'color': COLORS['neutral_text']})
                ])
            ])
        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}',
                  'margin': '20px 10px', 'border-radius': '10px'}),
        
        # Reports Section
        dbc.Card([
            dbc.CardBody([
                html.H6("Weekly Reports", style={'color': COLORS['gold_primary'], 'margin-bottom': '15px'}),
                html.Div([
                    html.Div([
                        dbc.Button([
                            html.I(className="fas fa-file-pdf", style={'margin-right': '8px'}),
                            "View Current Report"
                        ], id="view-pdf-btn", color="warning", size="sm", className="sidebar-btn mb-2",
                           style={'width': '100%', 'background-color': COLORS['gold_primary'],
                                  'border-color': COLORS['gold_primary']}),
                        html.Span("1", className="notification-badge")
                    ], className="button-with-badge", style={'width': '100%', 'margin-bottom': '8px'}),
                    
                    dbc.Button([
                        html.I(className="fas fa-presentation", style={'margin-right': '8px'}),
                        "Google Slides"
                    ], id="view-slides-btn", color="info", size="sm", className="sidebar-btn",
                       style={'width': '100%'})
                ])
            ])
        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}',
                  'margin': '20px 10px', 'border-radius': '10px'}),
        
        # Action Buttons
        html.Div([
            dbc.Button([
                html.I(className="fas fa-download", style={'margin-right': '8px'}),
                "Export Data"
            ], id="pdf-reports-btn", color="warning", size="sm", className="sidebar-btn",
               style={'width': '90%', 'margin': '10px 5%', 'background-color': COLORS['gold_primary'],
                      'border-color': COLORS['gold_primary']}),
            
            dbc.Button([
                html.I(className="fas fa-sync-alt", style={'margin-right': '8px'}),
                "Refresh Data"
            ], id="refresh-manual-btn", color="info", size="sm", className="sidebar-btn",
               style={'width': '90%', 'margin': '10px 5%'}),
            
            html.Hr(style={'border-color': COLORS['gold_primary'], 'margin': '20px 10px'}),
            
            dbc.Button([
                html.I(className="fas fa-sign-out-alt", style={'margin-right': '8px'}),
                "Logout"
            ], id="logout-btn", color="danger", size="sm", className="sidebar-btn",
               style={'width': '90%', 'margin': '10px 5%'})
        ])
    ], className="sidebar")

def get_header(title="Executive Business Intelligence Dashboard"):
    """Elite header with advanced metrics and real-time indicators"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.I(className="fas fa-chart-line", style={'margin-right': '15px', 'color': COLORS['gold_primary']}),
                        title
                    ], className="glow-text elite-title"),
                    html.Div([
                        html.Span([
                            html.I(className="fas fa-clock", style={'margin-right': '8px'}),
                            f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}"
                        ], style={'margin-right': '25px', 'color': COLORS['neutral_text']}),
                        html.Span([
                            html.Span("●", className="status-dot heartbeat", 
                                     style={'color': COLORS['success_green'], 'margin-right': '8px'}),
                            "Real-Time Data Stream"
                        ], style={'color': COLORS['success_green']})
                    ], className="header-subtext")
                ])
            ], width=7),
            dbc.Col([
                # Elite KPI Cards
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-dollar-sign", 
                                               style={'color': COLORS['gold_primary'], 'font-size': '18px'}),
                                        html.H4("$2.85M", 
                                               style={'color': COLORS['gold_primary'], 'margin': '5px 0 0 0', 'font-weight': '700'})
                                    ], className="kpi-icon-value"),
                                    html.Small("Total Revenue", 
                                              style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                    html.Div([
                                        html.I(className="fas fa-arrow-up", 
                                               style={'color': COLORS['success_green'], 'font-size': '12px'}),
                                        html.Span(" +12.5%", style={'color': COLORS['success_green'], 'font-size': '12px'})
                                    ])
                                ], className="text-center elite-kpi-card")
                            ], className="elite-mini-card floating")
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-exclamation-triangle", 
                                               style={'color': COLORS['warning_orange'], 'font-size': '18px'}),
                                        html.H4("74", 
                                               style={'color': COLORS['warning_orange'], 'margin': '5px 0 0 0', 'font-weight': '700'})
                                    ], className="kpi-icon-value"),
                                    html.Small("Active Alerts", 
                                              style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                    html.Div([
                                        html.I(className="fas fa-arrow-down", 
                                               style={'color': COLORS['success_green'], 'font-size': '12px'}),
                                        html.Span(" -8", style={'color': COLORS['success_green'], 'font-size': '12px'})
                                    ])
                                ], className="text-center elite-kpi-card")
                            ], className="elite-mini-card floating")
                        ], width=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-shield-alt", 
                                               style={'color': COLORS['success_green'], 'font-size': '18px'}),
                                        html.H4("99.9%", 
                                               style={'color': COLORS['success_green'], 'margin': '5px 0 0 0', 'font-weight': '700'})
                                    ], className="kpi-icon-value"),
                                    html.Small("System Uptime", 
                                              style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                    html.Div([
                                        html.I(className="fas fa-check", 
                                               style={'color': COLORS['success_green'], 'font-size': '12px'}),
                                        html.Span(" Stable", style={'color': COLORS['success_green'], 'font-size': '12px'})
                                    ])
                                ], className="text-center elite-kpi-card")
                            ], className="elite-mini-card floating")
                        ], width=4)
                    ], className="g-2")
                ], className="elite-kpi-container")
            ], width=5)
        ], align="center")
    ], className="header elite-header")

# Main dashboard layout
def get_dashboard_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Executive Business Intelligence Dashboard"),
            html.Div([
                # Charts Grid Container
                html.Div([
                    # Financial Impact Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='financial-impact-chart',
                                figure=create_financial_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Deadline Tracker Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='deadline-tracker-chart',
                                figure=create_deadline_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Alert Severity Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='alert-severity-chart',
                                figure=create_alert_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Historical Trends Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='historical-trends-chart',
                                figure=create_historical_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Growth vs Decline Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='growth-decline-chart',
                                figure=create_growth_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Performance Comparison Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='performance-comparison-chart',
                                figure=create_performance_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Risk & Compliance Gauge
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='risk-compliance-gauge',
                                figure=create_risk_gauge(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                    # Projection & Forecast Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='projection-forecast-chart',
                                figure=create_projection_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '420px'}
                            )
                        ], color=COLORS['gold_primary'])
                    ], className="card"),
                    
                ], className="chart-grid"),
                
                # Status indicator - NO EMOJIS
                html.Div([
                    html.Div(id='status-indicator', children=[
                        html.Span("● ", style={'color': COLORS['success_green'], 'font-size': '20px'}),
                        html.Span("System Online", style={'color': COLORS['neutral_text']})
                    ], style={'text-align': 'center', 'padding': '20px', 'font-size': '14px'})
                ])
                
            ], id="dashboard-content"),
            
            # Auto-refresh interval component
            dcc.Interval(
                id='auto-refresh-interval',
                interval=300000,  # 5 minutes
                n_intervals=0
            ),
            
            # Download component for PDF
            dcc.Download(id="download-pdf")
            
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Enhanced CSS with Font Awesome icons
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>LexCura Executive Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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
            
            /* Elite Premium Dashboard Styling */
            .elite-header {
                background: linear-gradient(135deg, #1B1D1F 0%, #2A2D30 50%, #1B1D1F 100%);
                border: 2px solid #D4AF37;
                border-radius: 20px;
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: 
                    0 0 50px rgba(212, 175, 55, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
            }
            
            .elite-header::before {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, #D4AF37, #FFCF66, #D4AF37, #FFCF66);
                z-index: -1;
                border-radius: 20px;
                background-size: 400% 400%;
                animation: gradientBorder 4s ease infinite;
            }
            
            @keyframes gradientBorder {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            
            .elite-title {
                font-size: 36px !important;
                font-weight: 800 !important;
                margin-bottom: 15px !important;
                background: linear-gradient(135deg, #D4AF37, #FFCF66, #D4AF37);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: none !important;
            }
            
            .elite-mini-card {
                background: linear-gradient(145deg, 
                    rgba(27, 29, 31, 0.9) 0%, 
                    rgba(42, 45, 48, 0.9) 100%) !important;
                border: 1px solid rgba(212, 175, 55, 0.3) !important;
                border-radius: 15px !important;
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 8px 25px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            }
            
            .elite-mini-card:hover {
                transform: translateY(-10px) scale(1.05) !important;
                border-color: rgba(212, 175, 55, 0.6) !important;
                box-shadow: 
                    0 20px 50px rgba(0, 0, 0, 0.6),
                    0 0 30px rgba(212, 175, 55, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
            
            .kpi-icon-value {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                margin-bottom: 8px;
            }
            
            .elite-kpi-card {
                padding: 20px 15px !important;
            }
            
            .heartbeat {
                animation: heartbeat 2s infinite;
            }
            
            @keyframes heartbeat {
                0%, 100% { 
                    transform: scale(1); 
                    opacity: 1; 
                }
                25% { 
                    transform: scale(1.2); 
                    opacity: 0.8; 
                }
                50% { 
                    transform: scale(1); 
                    opacity: 1; 
                }
            }
            
            /* CRITICAL LAYOUT FIXES */
            .sidebar {
                background: linear-gradient(180deg, 
                    rgba(27, 29, 31, 0.95) 0%, 
                    rgba(15, 17, 19, 0.98) 100%);
                backdrop-filter: blur(20px);
                border-right: 3px solid #D4AF37;
                box-shadow: 
                    4px 0 30px rgba(0, 0, 0, 0.5),
                    inset -1px 0 0 rgba(212, 175, 55, 0.2);
                height: 100vh;
                position: fixed;
                width: 280px;
                padding: 20px 15px;
                z-index: 1000;
                overflow-y: auto;
            }
            
            .main-content {
                margin-left: 280px !important;
                padding: 20px !important;
                min-height: 100vh;
                width: calc(100vw - 280px) !important;
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
                margin-top: 20px;
                width: 100%;
            }
            
            /* Fix header layout */
            .elite-header {
                background: linear-gradient(135deg, #1B1D1F 0%, #2A2D30 50%, #1B1D1F 100%);
                border: 2px solid #D4AF37;
                border-radius: 20px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 
                    0 0 50px rgba(212, 175, 55, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
                width: 100%;
            }
            
            /* Fix KPI cards layout */
            .elite-kpi-container {
                width: 100%;
            }
            
            .elite-mini-card {
                background: linear-gradient(145deg, 
                    rgba(27, 29, 31, 0.9) 0%, 
                    rgba(42, 45, 48, 0.9) 100%) !important;
                border: 1px solid rgba(212, 175, 55, 0.3) !important;
                border-radius: 12px !important;
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 6px 20px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease !important;
                height: 100%;
            }
            
            .elite-mini-card:hover {
                transform: translateY(-5px) !important;
                border-color: rgba(212, 175, 55, 0.6) !important;
                box-shadow: 
                    0 12px 35px rgba(0, 0, 0, 0.6),
                    0 0 20px rgba(212, 175, 55, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }
            
            .elite-kpi-card {
                padding: 15px 12px !important;
                text-align: center;
            }
            
            /* Button fixes */
            .sidebar-btn {
                transition: all 0.3s ease !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
                border: none !important;
                width: 100% !important;
                margin-bottom: 8px !important;
            }
            
            .sidebar-btn:hover {
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
            }
            
            /* Card fixes */
            .chart-grid .card {
                background: linear-gradient(145deg, 
                    rgba(27, 29, 31, 0.95) 0%, 
                    rgba(37, 40, 48, 0.95) 100%);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(212, 175, 55, 0.2);
                border-radius: 15px;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
                margin: 0;
                padding: 20px;
                height: auto;
                min-height: 450px;
            }
            
            .logo-enhanced {
                background: linear-gradient(135deg, 
                    rgba(212, 175, 55, 0.15) 0%, 
                    rgba(255, 207, 102, 0.1) 50%,
                    rgba(212, 175, 55, 0.05) 100%);
                border: 1px solid rgba(212, 175, 55, 0.3);
                border-radius: 15px;
                margin: 20px 10px 25px 10px;
                padding: 25px 20px;
                position: relative;
                overflow: hidden;
            }
            
            .logo-enhanced::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(212, 175, 55, 0.3), 
                    transparent);
                animation: logoShimmer 3s infinite;
            }
            
            @keyframes logoShimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            /* Elite chart containers */
            .chart-grid .card {
                background: linear-gradient(145deg, 
                    rgba(27, 29, 31, 0.95) 0%, 
                    rgba(37, 40, 48, 0.95) 100%);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(212, 175, 55, 0.2);
                border-radius: 20px;
                box-shadow: 
                    0 15px 40px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
            }
            
            .chart-grid .card::before {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                height: 6px;
                background: linear-gradient(90deg, 
                    #D4AF37 0%, 
                    #FFCF66 25%, 
                    #D4AF37 50%, 
                    #FFCF66 75%, 
                    #D4AF37 100%);
                background-size: 200% 100%;
                animation: borderFlow 4s linear infinite;
                border-radius: 20px 20px 0 0;
                z-index: 1;
            }
            
            @keyframes borderFlow {
                0% { background-position: 0% 0%; }
                100% { background-position: 200% 0%; }
            }
            
            /* Elite status indicator */
            #status-indicator {
                background: linear-gradient(135deg, 
                    rgba(212, 175, 55, 0.15) 0%, 
                    rgba(0, 0, 0, 0.4) 100%);
                border: 2px solid rgba(212, 175, 55, 0.4);
                border-radius: 30px;
                padding: 20px 30px;
                backdrop-filter: blur(20px);
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
            }
            
            #status-indicator::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(212, 175, 55, 0.2), 
                    transparent);
                animation: statusShine 5s infinite;
            }
            
            /* Notification badge styling */
            .notification-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                background: linear-gradient(45deg, #E4574C, #F4A261);
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                font-size: 12px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid #0F1113;
                animation: badgePulse 2s infinite;
            }
            
            @keyframes badgePulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            /* Enhanced button positioning for badges */
            .button-with-badge {
                position: relative;
                display: inline-block;
            }
            
            /* Subtle data flow animation */
            .data-flow {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, 
                    transparent 0%, 
                    #D4AF37 50%, 
                    transparent 100%);
                animation: dataStream 3s linear infinite;
            }
            
            @keyframes dataStream {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            .logo-enhanced {
                text-align: center;
                padding: 20px;
                border-bottom: 2px solid #D4AF37;
                margin-bottom: 20px;
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(0,0,0,0) 100%);
            }
            
            /* Sidebar button enhancements */
            .sidebar-btn {
                transition: all 0.3s ease;
                border-radius: 8px !important;
                font-weight: 500;
                margin: 8px 5% !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }
            
            .sidebar-btn:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 6px 20px rgba(0,0,0,0.4);
            }
            
            /* Chart loading animation */
            .chart-loading {
                position: relative;
                overflow: hidden;
            }
            
            .chart-loading::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
                animation: shimmer 2s infinite;
                z-index: 1;
            }
            
            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            /* Enhanced card animations */
            .card {
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
            }
            
            .card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #FFCF66, #D4AF37);
                background-size: 200% 100%;
                animation: gradientShift 3s ease-in-out infinite;
            }
            
            @keyframes gradientShift {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
            
            .card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
                border-color: rgba(212, 175, 55, 0.6);
            }
            
            /* Floating elements */
            .floating {
                animation: float 6s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            /* Glowing text effect */
            .glow-text {
                text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
                animation: textGlow 2s ease-in-out infinite alternate;
            }
            
            @keyframes textGlow {
                from { text-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }
                to { text-shadow: 0 0 20px rgba(212, 175, 55, 0.8); }
            }
            
            /* Enhanced status indicator */
            #status-indicator {
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(0,0,0,0.3));
                border-radius: 25px;
                padding: 15px 25px;
                border: 1px solid rgba(212, 175, 55, 0.3);
                backdrop-filter: blur(10px);
            }
            
            /* Scrollbar enhancements */
            ::-webkit-scrollbar {
                width: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: linear-gradient(180deg, #0F1113, #1B1D1F);
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #D4AF37, #FFCF66);
                border-radius: 6px;
                border: 2px solid #0F1113;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(180deg, #FFCF66, #D4AF37);
            }
            
            .nav-item.active {
                background-color: rgba(212, 175, 55, 0.2);
                color: #FFCF66 !important;
                border-left-color: #D4AF37;
                text-decoration: none !important;
            }
            
            .main-content {
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
            
            /* Loading spinner customization */
            ._dash-loading {
                color: #D4AF37 !important;
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
                    margin-left: 0 !important;
                    padding: 15px !important;
                }
                
                .chart-grid {
                    grid-template-columns: 1fr;
                    gap: 15px;
                }
            }
            
            /* Login button animation */
            #login-button {
                transition: all 0.3s ease;
                transform: scale(1);
                box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            }
            
            #login-button:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 25px rgba(212, 175, 55, 0.5);
                background-color: #FFCF66 !important;
            }
            
            #login-button:active {
                transform: scale(0.98);
                transition: all 0.1s ease;
            }
            
            /* Input field styling */
            .form-control:focus {
                border-color: #D4AF37 !important;
                box-shadow: 0 0 0 0.2rem rgba(212, 175, 55, 0.25) !important;
            }
            
            /* Card animation */
            .login-card {
                animation: slideInUp 0.6s ease-out;
                transform: translateY(0);
            }
            
            @keyframes slideInUp {
                from {
                    transform: translateY(30px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            /* Success alert animation */
            .alert {
                animation: fadeInDown 0.5s ease-out;
            }
            
            @keyframes fadeInDown {
                from {
                    transform: translateY(-20px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
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

# Main app layout with URL routing and session preservation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Store(id='current-user', storage_type='session'),  # Additional session store
    html.Div(id='page-content')
])

# Simplified page routing - only dashboard/login
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('session-store', 'data'),
     State('current-user', 'data')],
    prevent_initial_call=False
)
def display_page(pathname, session_data, user_data):
    """Display dashboard or login based on authentication"""
    
    # Check authentication using enhanced method
    authenticated = is_authenticated(session_data, user_data)
    
    if not authenticated:
        return get_login_layout()
    
    # For now, always show dashboard regardless of path
    return get_dashboard_layout()

# Login callback with improved session handling
@app.callback(
    [Output('session-store', 'data'),
     Output('current-user', 'data'),
     Output('login-alert', 'children'),
     Output('url', 'pathname')],
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'),
     State('password-input', 'value')]
)
def handle_login(n_clicks, username, password):
    if n_clicks and username and password:
        if verify_credentials(username, password):
            session_id = generate_session_id()
            session_data = {
                'username': username,
                'login_time': datetime.now().isoformat(),
                'authenticated': True
            }
            session_store[session_id] = session_data
            
            return (
                {'session_id': session_id, 'authenticated': True},
                {'username': username, 'session_id': session_id},
                dbc.Alert("Login successful! Redirecting...", color="success"),
                "/"
            )
        else:
            return (
                {'authenticated': False},
                {},
                dbc.Alert("Invalid credentials. Please try again.", color="danger"),
                "/login"
            )
    return {'authenticated': False}, {}, "", "/login"

# Fixed logout callback with forced redirect
@app.callback(
    [Output('session-store', 'data', allow_duplicate=True),
     Output('current-user', 'data', allow_duplicate=True)],
    Input('logout-btn', 'n_clicks'),
    [State('session-store', 'data'),
     State('current-user', 'data')],
    prevent_initial_call=True
)
def handle_logout(n_clicks, session_data, user_data):
    if n_clicks and n_clicks > 0:
        # Clean up session store
        if session_data and session_data.get('session_id'):
            session_id = session_data.get('session_id')
            if session_id in session_store:
                del session_store[session_id]
        
        # Clear all session data - this will trigger login page display
        return {'authenticated': False}, {}
    
    # Return unchanged if no click
    return session_data or {'authenticated': False}, user_data or {}

# Manual refresh callback
@app.callback(
    [Output('financial-impact-chart', 'figure', allow_duplicate=True),
     Output('deadline-tracker-chart', 'figure', allow_duplicate=True),
     Output('alert-severity-chart', 'figure', allow_duplicate=True),
     Output('historical-trends-chart', 'figure', allow_duplicate=True),
     Output('growth-decline-chart', 'figure', allow_duplicate=True),
     Output('performance-comparison-chart', 'figure', allow_duplicate=True),
     Output('risk-compliance-gauge', 'figure', allow_duplicate=True),
     Output('projection-forecast-chart', 'figure', allow_duplicate=True)],
    Input("refresh-manual-btn", "n_clicks"),
    prevent_initial_call=True
)
def manual_refresh_charts(n_clicks):
    if n_clicks and n_clicks > 0:
        # Add small data variations for realistic updates
        global data
        for i in range(len(data['financial']['current'])):
            variation = random.uniform(-0.02, 0.02)
            data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
        
        return (
            create_financial_chart(),
            create_deadline_chart(),
            create_alert_chart(),
            create_historical_chart(),
            create_growth_chart(),
            create_performance_chart(),
            create_risk_gauge(),
            create_projection_chart()
        )
    
    return [dash.no_update] * 8
@app.callback(
    Output("download-pdf", "data", allow_duplicate=True),
    Input("pdf-reports-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_pdf_reports(n_clicks):
    if n_clicks and n_clicks > 0:
        try:
            pdf_buffer = generate_pdf_report()
            if pdf_buffer:
                return dcc.send_bytes(pdf_buffer.getvalue(), 
                                    filename=f"LexCura_Dashboard_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
    return None
@app.callback(
    Output("download-pdf", "data", allow_duplicate=True),
    [Input("exec-summary-btn", "n_clicks"),
     Input("financial-report-btn", "n_clicks"), 
     Input("performance-report-btn", "n_clicks")],
    prevent_initial_call=True
)
def handle_report_downloads(exec_clicks, financial_clicks, performance_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        pdf_buffer = generate_pdf_report()
        if pdf_buffer:
            if button_id == "exec-summary-btn":
                filename = f"LexCura_Executive_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            elif button_id == "financial-report-btn":
                filename = f"LexCura_Financial_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            else:
                filename = f"LexCura_Performance_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            
            return dcc.send_bytes(pdf_buffer.getvalue(), filename=filename)
    except Exception as e:
        print(f"Error in report download: {str(e)}")
    
    return None

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
        
        # Add small variations for realistic updates
        if n_intervals > 0 or refresh_clicks:
            for i in range(len(data['financial']['current'])):
                variation = random.uniform(-0.02, 0.02)
                data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
            
            data['risk_score'] = max(0, min(100, data['risk_score'] + random.uniform(-2, 2)))
        
        current_time = datetime.now().strftime('%I:%M %p')
        status_indicator = [
            html.Span("● ", className="status-dot", 
                     style={'color': COLORS['success_green'], 'font-size': '20px'}),
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
        print(f"Error in dashboard update: {str(e)}")
        error_status = [
            html.Span("● ", style={'color': COLORS['danger_red'], 'font-size': '20px'}),
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

# PDF Export callback
@app.callback(
    Output("download-pdf", "data"),
    Input("export-pdf-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_pdf_report(n_clicks):
    if n_clicks:
        try:
            pdf_buffer = generate_pdf_report()
            if pdf_buffer:
                return dcc.send_bytes(pdf_buffer.getvalue(), 
                                    filename=f"LexCura_Dashboard_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        except Exception as e:
            print(f"Error exporting PDF: {str(e)}")
    return None

# Google Slides callback
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('open-slides-btn', 'n_clicks'),
    prevent_initial_call=True
)
def open_google_slides(n_clicks):
    if n_clicks:
        # In a real implementation, you would open the Google Slides URL
        # For now, we'll just stay on the same page
        return "/slides"
    return "/slides"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=port
    )

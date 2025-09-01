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
    'deep_blue': '#2E3A59',
    'accent_purple': '#6A4C93'
}

# Session store for authentication
session_store = {}

def generate_session_id():
    """Generate a secure session ID"""
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def verify_credentials(username, password):
    """Verify user credentials"""
    return USERS.get(username) == password

def is_authenticated(session_id):
    """Check if session is authenticated"""
    return session_id in session_store

# Enhanced data generation with more realistic business data
def generate_sample_data():
    try:
        random.seed(42)
        
        # Financial data with more categories
        financial_data = {
            'categories': ['Q4 Revenue', 'Operating Costs', 'Net Profit', 'R&D Investment', 'Marketing ROI', 'Legal Services'],
            'current': [4250000, -1850000, 2400000, -680000, 920000, -340000],
            'previous': [3800000, -1920000, 1880000, -720000, 780000, -290000],
            'targets': [4500000, -1750000, 2750000, -650000, 1100000, -320000]
        }
        
        # Advanced deadline data with more projects
        deadline_data = {
            'tasks': ['Q4 Financial Audit', 'Cloud Migration', 'Compliance Review', 'Budget 2025', 'Security Upgrade', 'Client Onboarding', 'Legal Documentation'],
            'days_left': [2, 18, 1, 15, 25, 8, 12],
            'progress': [92, 35, 98, 55, 20, 75, 60],
            'priority': ['Critical', 'High', 'Critical', 'Medium', 'Low', 'High', 'Medium']
        }
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        # Enhanced alert data
        alert_data = {
            'severity': ['Critical', 'High', 'Medium', 'Low', 'Info'],
            'count': [5, 12, 18, 25, 40],
            'categories': ['Security', 'Performance', 'Compliance', 'System', 'User']
        }
        
        # Extended historical data with multiple metrics
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        historical_dates = []
        current_date = start_date
        while current_date <= end_date:
            historical_dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Multiple performance metrics
        base_values = {'revenue': 1000, 'efficiency': 75, 'satisfaction': 80}
        historical_data = {
            'dates': historical_dates,
            'revenue_performance': [],
            'operational_efficiency': [],
            'client_satisfaction': [],
            'targets': {'revenue': 1200, 'efficiency': 85, 'satisfaction': 90}
        }
        
        for i, date in enumerate(historical_dates):
            # Revenue trend
            trend = (i / len(historical_dates)) * 300
            seasonal = 150 * math.sin(2 * math.pi * i / 365)
            noise = random.uniform(-75, 75)
            revenue_value = base_values['revenue'] + trend + seasonal + noise
            historical_data['revenue_performance'].append(max(0, revenue_value))
            
            # Efficiency trend
            eff_trend = (i / len(historical_dates)) * 15
            eff_seasonal = 5 * math.cos(2 * math.pi * i / 365)
            eff_noise = random.uniform(-3, 3)
            eff_value = base_values['efficiency'] + eff_trend + eff_seasonal + eff_noise
            historical_data['operational_efficiency'].append(max(0, min(100, eff_value)))
            
            # Satisfaction trend
            sat_trend = (i / len(historical_dates)) * 12
            sat_seasonal = 8 * math.sin(2 * math.pi * i / 180)
            sat_noise = random.uniform(-4, 4)
            sat_value = base_values['satisfaction'] + sat_trend + sat_seasonal + sat_noise
            historical_data['client_satisfaction'].append(max(0, min(100, sat_value)))
        
        # Enhanced growth data with quarterly breakdown
        growth_data = {
            'quarters': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024 (Proj)'],
            'revenue_growth': [15, 22, 18, 28],
            'market_expansion': [8, 12, 15, 20],
            'client_acquisition': [25, 18, 30, 35],
            'operational_decline': [5, 3, 2, 1]
        }
        
        # Comprehensive performance KPIs
        performance_data = {
            'kpis': ['Legal Efficiency', 'Client Satisfaction', 'Response Time', 'Cost Optimization', 'Revenue Growth', 'Market Position'],
            'current_score': [88, 94, 82, 91, 85, 78],
            'target_score': [92, 96, 88, 95, 90, 85],
            'industry_avg': [75, 87, 78, 83, 80, 72],
            'last_quarter': [85, 91, 79, 88, 82, 75]
        }
        
        # Dynamic risk assessment
        risk_score = random.randint(45, 75)
        
        # Advanced projection data with confidence intervals
        future_dates = []
        current_month = datetime.now().replace(day=1)
        for i in range(18):  # Extended to 18 months
            future_dates.append(current_month + timedelta(days=32*i))
        
        base_forecast = 2000
        growth_rate = 0.06
        projection_data = {
            'dates': future_dates,
            'revenue_forecast': [],
            'conservative_forecast': [],
            'optimistic_forecast': [],
            'lower_confidence': [],
            'upper_confidence': []
        }
        
        for i in range(18):
            # Main forecast
            forecast = base_forecast * (1 + growth_rate) ** i
            projection_data['revenue_forecast'].append(forecast)
            
            # Conservative scenario (slower growth)
            conservative = base_forecast * (1 + growth_rate * 0.7) ** i
            projection_data['conservative_forecast'].append(conservative)
            
            # Optimistic scenario (faster growth)
            optimistic = base_forecast * (1 + growth_rate * 1.3) ** i
            projection_data['optimistic_forecast'].append(optimistic)
            
            # Confidence intervals
            projection_data['lower_confidence'].append(forecast * 0.85)
            projection_data['upper_confidence'].append(forecast * 1.15)
        
        # Google Slides archive with more entries
        archive_data = [
            {
                'date': '2024-12-15',
                'title': 'Q4 Executive Summary 2024',
                'url': 'https://docs.google.com/presentation/d/1example1/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Executive Report'
            },
            {
                'date': '2024-11-28',
                'title': 'November Financial Performance',
                'url': 'https://docs.google.com/presentation/d/1example2/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Financial Report'
            },
            {
                'date': '2024-11-01',
                'title': 'Legal Services Analytics',
                'url': 'https://docs.google.com/presentation/d/1example3/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Analytics Report'
            },
            {
                'date': '2024-10-15',
                'title': 'Client Satisfaction Survey Results',
                'url': 'https://docs.google.com/presentation/d/1example4/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Research Report'
            },
            {
                'date': '2024-10-01',
                'title': 'Q3 Compliance Review',
                'url': 'https://docs.google.com/presentation/d/1example5/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Compliance Report'
            },
            {
                'date': '2024-09-15',
                'title': 'Technology Roadmap 2025',
                'url': 'https://docs.google.com/presentation/d/1example6/edit',
                'thumbnail': '/assets/lexcura_logo.png',
                'type': 'Strategic Report'
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
        return {
            'financial': {'categories': ['Revenue'], 'current': [1000000], 'previous': [900000], 'targets': [1100000]},
            'deadlines': {'tasks': ['Sample Task'], 'days_left': [5], 'progress': [50], 'urgency': ['Normal'], 'priority': ['Medium']},
            'alerts': {'severity': ['Info'], 'count': [10], 'categories': ['System']},
            'historical': {'dates': [datetime.now()], 'revenue_performance': [1000], 'operational_efficiency': [75], 'client_satisfaction': [80], 'targets': {'revenue': 1200, 'efficiency': 85, 'satisfaction': 90}},
            'growth': {'quarters': ['Q1'], 'revenue_growth': [15], 'market_expansion': [8], 'client_acquisition': [25], 'operational_decline': [5]},
            'performance': {'kpis': ['Performance'], 'current_score': [80], 'target_score': [90], 'industry_avg': [75], 'last_quarter': [78]},
            'risk_score': 70,
            'projections': {'dates': [datetime.now()], 'revenue_forecast': [1500], 'conservative_forecast': [1400], 'optimistic_forecast': [1600], 'lower_confidence': [1300], 'upper_confidence': [1700]},
            'archive': []
        }

# Initialize data
data = generate_sample_data()

def get_animated_layout(title):
    """Base layout with animation settings"""
    return {
        'title': {
            'text': title,
            'font': {'color': COLORS['neutral_text'], 'size': 20, 'family': 'Inter', 'weight': 600},
            'x': 0.5,
            'xanchor': 'center'
        },
        'paper_bgcolor': COLORS['charcoal'],
        'plot_bgcolor': COLORS['dark_grey'],
        'font': {'color': COLORS['neutral_text'], 'family': 'Inter'},
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
        'showlegend': True,
        'legend': {
            'font': {'color': COLORS['neutral_text'], 'size': 12},
            'bgcolor': 'rgba(0,0,0,0.3)',
            'bordercolor': COLORS['gold_primary'],
            'borderwidth': 1,
            'x': 0.02,
            'y': 0.98
        },
        'xaxis': {
            'color': COLORS['neutral_text'], 
            'gridcolor': '#2A2D30',
            'gridwidth': 0.5,
            'zeroline': False
        },
        'yaxis': {
            'color': COLORS['neutral_text'], 
            'gridcolor': '#2A2D30',
            'gridwidth': 0.5,
            'zeroline': False
        },
        # Animation settings
        'transition': {'duration': 800, 'easing': 'cubic-in-out'},
        'hovermode': 'x unified'
    }

# Enhanced animated chart functions
def create_financial_chart():
    try:
        fig = go.Figure()
        
        # Current period bars with gradient colors
        colors_current = []
        for i, x in enumerate(data['financial']['current']):
            if x > 0:
                colors_current.append(f'rgba(61, 188, 107, {0.8 + i*0.05})')  # Green gradient
            else:
                colors_current.append(f'rgba(228, 87, 76, {0.8 + i*0.05})')   # Red gradient
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            marker_line=dict(width=2, color=COLORS['gold_primary']),
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<br>vs Target: %{customdata:,.0f}<extra></extra>',
            customdata=data['financial']['targets'],
            text=[f"${x:,.0f}" for x in data['financial']['current']],
            textposition='outside',
            textfont={'size': 12, 'color': COLORS['neutral_text']}
        ))
        
        # Previous period bars
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=COLORS['gold_primary'],
            marker_line=dict(width=1, color=COLORS['highlight_gold']),
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<br><extra></extra>'
        ))
        
        # Target line
        fig.add_trace(go.Scatter(
            x=data['financial']['categories'],
            y=data['financial']['targets'],
            mode='markers',
            marker=dict(size=12, color=COLORS['highlight_gold'], symbol='diamond'),
            name='Targets',
            hovertemplate='<b>%{x}</b><br>Target: $%{y:,.0f}<br><extra></extra>'
        ))
        
        layout = get_animated_layout('Financial Performance Analysis')
        layout['yaxis']['tickformat'] = '$,.0f'
        layout['barmode'] = 'group'
        layout['bargap'] = 0.3
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in financial chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Financial Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_deadline_chart():
    try:
        fig = go.Figure()
        
        priority_colors = {
            'Critical': COLORS['danger_red'],
            'High': COLORS['warning_orange'],
            'Medium': '#4A90E2',
            'Low': COLORS['success_green']
        }
        
        colors = [priority_colors.get(priority, COLORS['neutral_text']) for priority in data['deadlines']['priority']]
        
        # Main bars
        fig.add_trace(go.Bar(
            y=data['deadlines']['tasks'],
            x=data['deadlines']['days_left'],
            orientation='h',
            marker_color=colors,
            marker_line=dict(width=1, color='white'),
            hovertemplate='<b>%{y}</b><br>Days Left: %{x}<br>Progress: %{customdata}%<br>Priority: %{text}<br><extra></extra>',
            customdata=data['deadlines']['progress'],
            text=data['deadlines']['priority'],
            name='Days Remaining'
        ))
        
        # Progress indicators as secondary bars
        fig.add_trace(go.Bar(
            y=data['deadlines']['tasks'],
            x=[d * (p/100) for d, p in zip(data['deadlines']['days_left'], data['deadlines']['progress'])],
            orientation='h',
            marker_color='rgba(255, 207, 102, 0.6)',
            marker_line=dict(width=0),
            name='Progress',
            hovertemplate='Progress: %{customdata}%<extra></extra>',
            customdata=data['deadlines']['progress']
        ))
        
        layout = get_animated_layout('Project Timeline & Progress Tracker')
        layout['xaxis']['title'] = 'Days Remaining'
        layout['height'] = 500
        layout['barmode'] = 'overlay'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in deadline chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Deadline Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_alert_chart():
    try:
        severity_colors = [COLORS['danger_red'], '#FF6B35', COLORS['warning_orange'], '#4A90E2', COLORS['success_green']]
        
        fig = go.Figure()
        
        # Main donut
        fig.add_trace(go.Pie(
            labels=data['alerts']['severity'],
            values=data['alerts']['count'],
            hole=0.65,
            marker_colors=severity_colors,
            marker_line=dict(color='white', width=3),
            hovertemplate='<b>%{label} Priority</b><br>Count: %{value}<br>Percentage: %{percent}<br>Category: %{customdata}<extra></extra>',
            customdata=data['alerts']['categories'],
            textinfo='label+percent',
            textfont={'color': 'white', 'size': 11, 'family': 'Inter'},
            textposition='inside',
            pull=[0.05 if sev == 'Critical' else 0 for sev in data['alerts']['severity']]  # Pull out critical
        ))
        
        # Center annotation with animation
        total_alerts = sum(data['alerts']['count'])
        critical_alerts = data['alerts']['count'][0] if len(data['alerts']['count']) > 0 else 0
        
        fig.add_annotation(
            text=f"Total Alerts<br><b style='font-size: 24px; color: {COLORS['gold_primary']}'>{total_alerts}</b><br><span style='color: {COLORS['danger_red']}; font-size: 14px'>{critical_alerts} Critical</span>",
            x=0.5, y=0.5,
            font={'size': 16, 'color': COLORS['neutral_text'], 'family': 'Inter'},
            showarrow=False,
            align='center'
        )
        
        layout = get_animated_layout('Security & System Alerts Distribution')
        layout['showlegend'] = True
        layout['legend']['orientation'] = 'v'
        layout['legend']['x'] = 1.05
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in alert chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Alert Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_historical_chart():
    try:
        fig = go.Figure()
        
        # Revenue performance with area fill
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['revenue_performance'],
            mode='lines',
            line={'color': COLORS['gold_primary'], 'width': 3, 'shape': 'spline'},
            fill='tonexty',
            fillcolor=f"rgba(212, 175, 55, 0.2)",
            name='Revenue Performance',
            hovertemplate='<b>Revenue Performance</b><br>Date: %{x}<br>Value: %{y:,.1f}<br><extra></extra>'
        ))
        
        # Operational efficiency
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['operational_efficiency'],
            mode='lines',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'},
            name='Operational Efficiency (%)',
            yaxis='y2',
            hovertemplate='<b>Efficiency</b><br>Date: %{x}<br>Value: %{y:.1f}%<br><extra></extra>'
        ))
        
        # Client satisfaction
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['client_satisfaction'],
            mode='lines',
            line={'color': COLORS['deep_blue'], 'width': 2, 'dash': 'dash'},
            name='Client Satisfaction (%)',
            yaxis='y2',
            hovertemplate='<b>Client Satisfaction</b><br>Date: %{x}<br>Value: %{y:.1f}%<br><extra></extra>'
        ))
        
        # Target lines
        fig.add_hline(
            y=data['historical']['targets']['revenue'],
            line_dash="solid",
            line_color=COLORS['highlight_gold'],
            line_width=2,
            opacity=0.7,
            annotation_text="Revenue Target",
            annotation_position="top right"
        )
        
        layout = get_animated_layout('Historical Performance Trends (12 Months)')
        layout['xaxis']['title'] = 'Date'
        layout['yaxis']['title'] = 'Revenue Performance'
        layout['yaxis2'] = dict(
            title='Efficiency & Satisfaction (%)',
            overlaying='y',
            side='right',
            range=[0, 100],
            color=COLORS['neutral_text']
        )
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in historical chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Historical Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_growth_chart():
    try:
        fig = go.Figure()
        
        # Revenue growth bars
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['revenue_growth'],
            name='Revenue Growth',
            marker_color=COLORS['success_green'],
            marker_line=dict(width=2, color='white'),
            hovertemplate='<b>%{x}</b><br>Revenue Growth: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['revenue_growth']],
            textposition='outside',
            textfont={'size': 12, 'color': COLORS['success_green']}
        ))
        
        # Market expansion
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['market_expansion'],
            name='Market Expansion',
            marker_color=COLORS['gold_primary'],
            marker_line=dict(width=2, color='white'),
            hovertemplate='<b>%{x}</b><br>Market Expansion: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['market_expansion']],
            textposition='outside',
            textfont={'size': 12, 'color': COLORS['gold_primary']}
        ))
        
        # Client acquisition line
        fig.add_trace(go.Scatter(
            x=data['growth']['quarters'],
            y=data['growth']['client_acquisition'],
            mode='lines+markers',
            line={'color': COLORS['deep_blue'], 'width': 4},
            marker={'size': 10, 'color': COLORS['deep_blue'], 'line': dict(width=2, color='white')},
            name='Client Acquisition',
            hovertemplate='<b>%{x}</b><br>New Clients: +%{y}%<extra></extra>'
        ))
        
        layout = get_animated_layout('Quarterly Growth Analysis & Market Expansion')
        layout['yaxis']['title'] = 'Growth Rate (%)'
        layout['yaxis']['ticksuffix'] = '%'
        layout['xaxis']['title'] = 'Quarter'
        layout['barmode'] = 'group'
        layout['bargap'] = 0.3
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in growth chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Growth Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_performance_chart():
    try:
        fig = go.Figure()
        
        # Current performance radar
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['current_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Current Performance',
            line={'color': COLORS['gold_primary'], 'width': 3},
            fillcolor=f"rgba(212, 175, 55, 0.3)",
            hovertemplate='<b>%{theta}</b><br>Current: %{r}%<br><extra></extra>',
            marker={'size': 8}
        ))
        
        # Target performance
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            mode='lines+markers',
            name='Target Goals',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'},
            marker={'size': 6, 'symbol': 'diamond'},
            hovertemplate='<b>%{theta}</b><br>Target: %{r}%<br><extra></extra>'
        ))
        
        # Industry average
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['industry_avg'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Industry Benchmark',
            line={'color': COLORS['neutral_text'], 'width': 2, 'dash': 'dash'},
            hovertemplate='<b>%{theta}</b><br>Industry Avg: %{r}%<br><extra></extra>'
        ))
        
        # Last quarter comparison
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['last_quarter'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Last Quarter',
            line={'color': COLORS['warning_orange'], 'width': 1},
            opacity=0.7,
            hovertemplate='<b>%{theta}</b><br>Last Quarter: %{r}%<br><extra></extra>'
        ))
        
        layout = get_animated_layout('Performance KPIs vs Industry Benchmarks')
        layout['polar'] = {
            'bgcolor': COLORS['dark_grey'],
            'radialaxis': {
                'visible': True,
                'range': [0, 100],
                'color': COLORS['neutral_text'],
                'ticksuffix': '%',
                'gridcolor': '#2A2D30',
                'linecolor': COLORS['gold_primary']
            },
            'angularaxis': {
                'color': COLORS['neutral_text'],
                'gridcolor': '#2A2D30',
                'linecolor': COLORS['gold_primary']
            }
        }
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in performance chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Performance Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_risk_gauge():
    try:
        # Enhanced risk assessment colors
        if data['risk_score'] <= 25:
            gauge_color = COLORS['success_green']
            risk_level = "Minimal"
        elif data['risk_score'] <= 50:
            gauge_color = '#4A90E2'
            risk_level = "Low"
        elif data['risk_score'] <= 75:
            gauge_color = COLORS['warning_orange']
            risk_level = "Moderate"
        else:
            gauge_color = COLORS['danger_red']
            risk_level = "High"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=data['risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': f"<b>Risk Assessment Score</b><br><span style='font-size:16px;color:{gauge_color}'>{risk_level} Risk</span>",
                'font': {'color': COLORS['neutral_text'], 'size': 18, 'family': 'Inter'}
            },
            delta={
                'reference': 50,
                'increasing': {'color': COLORS['danger_red']},
                'decreasing': {'color': COLORS['success_green']},
                'suffix': ' pts'
            },
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': COLORS['neutral_text'],
                    'tickfont': {'color': COLORS['neutral_text'], 'size': 12}
                },
                'bar': {'color': gauge_color, 'thickness': 0.4},
                'steps': [
                    {'range': [0, 25], 'color': 'rgba(61, 188, 107, 0.2)'},
                    {'range': [25, 50], 'color': 'rgba(74, 144, 226, 0.2)'},
                    {'range': [50, 75], 'color': 'rgba(244, 162, 97, 0.2)'},
                    {'range': [75, 100], 'color': 'rgba(228, 87, 76, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': COLORS['highlight_gold'], 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                },
                'bordercolor': COLORS['gold_primary'],
                'borderwidth': 2
            },
            number={'font': {'color': COLORS['neutral_text'], 'size': 28, 'family': 'Inter'}}
        ))
        
        fig.update_layout(
            paper_bgcolor=COLORS['charcoal'],
            plot_bgcolor=COLORS['charcoal'],
            font={'color': COLORS['neutral_text'], 'family': 'Inter'},
            margin={'l': 40, 'r': 40, 't': 80, 'b': 40},
            height=400
        )
        
        return fig
    except Exception as e:
        print(f"Error in risk gauge: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Risk Gauge Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
        return fig

def create_projection_chart():
    try:
        fig = go.Figure()
        
        # Upper confidence bound (invisible for fill)
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['upper_confidence'],
            mode='lines',
            line={'width': 0},
            showlegend=False,
            hoverinfo='skip',
            name='Upper Confidence'
        ))
        
        # Lower confidence bound with fill
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['lower_confidence'],
            mode='lines',
            line={'width': 0},
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.15)',
            name='Confidence Range (85%-115%)',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Range: $%{y:,.0f} - $%{customdata:,.0f}<extra></extra>',
            customdata=data['projections']['upper_confidence']
        ))
        
        # Conservative forecast
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['conservative_forecast'],
            mode='lines',
            line={'color': COLORS['warning_orange'], 'width': 2, 'dash': 'dash'},
            name='Conservative Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Conservative: $%{y:,.0f}<extra></extra>'
        ))
        
        # Optimistic forecast
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['optimistic_forecast'],
            mode='lines',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'},
            name='Optimistic Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Optimistic: $%{y:,.0f}<extra></extra>'
        ))
        
        # Main forecast line with markers
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['revenue_forecast'],
            mode='lines+markers',
            line={'color': COLORS['gold_primary'], 'width': 4},
            marker={'size': 8, 'color': COLORS['highlight_gold'], 'line': dict(width=2, color=COLORS['gold_primary'])},
            name='Base Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
        ))
        
        layout = get_animated_layout('18-Month Revenue Projection with Scenarios')
        layout['xaxis']['title'] = 'Month'
        layout['yaxis']['title'] = 'Revenue ($)'
        layout['yaxis']['tickformat'] = '$,.0f'
        
        fig.update_layout(layout)
        return fig
    except Exception as e:
        print(f"Error in projection chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(text="Projection Chart Error - Please Refresh", x=0.5, y=0.5, showarrow=False)
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
                    'transition': 'all 1.5s cubic-bezier(0.4, 0, 0.2, 1)',
                    'filter': 'drop-shadow(0 0 20px rgba(212, 175, 55, 0.5))'
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
                    'transform': 'translateY(20px)',
                    'transition': 'all 1.2s cubic-bezier(0.4, 0, 0.2, 1) 0.5s'
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
                    'transform': 'translateY(20px)',
                    'transition': 'all 1s cubic-bezier(0.4, 0, 0.2, 1) 1s'
                }
            ),
            html.Div([
                html.Div(style={
                    'width': '60px',
                    'height': '4px',
                    'background': f'linear-gradient(90deg, {COLORS["gold_primary"]}, {COLORS["highlight_gold"]})',
                    'border-radius': '2px',
                    'transform': 'scaleX(0)',
                    'animation': 'loadingBar 2s ease-in-out 1.5s forwards'
                })
            ], style={'margin-top': '30px', 'display': 'flex', 'justify-content': 'center'})
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
        'background': f'radial-gradient(circle at center, {COLORS["dark_grey"]} 0%, {COLORS["charcoal"]} 100%)',
        'z-index': '9999',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    })

# Login page layout
def get_login_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="/assets/lexcura_logo.png", 
                                   style={'width': '120px', 'height': 'auto', 'margin-bottom': '30px'}),
                            html.H2("LexCura Dashboard", className="text-center mb-4", 
                                   style={'color': COLORS['gold_primary'], 'font-weight': 'bold', 'font-family': 'Inter'}),
                            html.P("Executive Business Intelligence Platform", 
                                  className="text-center mb-4",
                                  style={'color': COLORS['neutral_text'], 'font-size': '14px'}),
                            html.Hr(style={'border-color': COLORS['gold_primary']}),
                            dbc.Form([
                                dbc.Row([
                                    dbc.Label("Username", html_for="username-input", 
                                            style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                    dbc.Input(id="username-input", type="text", placeholder="Enter username",
                                            style={'background-color': COLORS['dark_grey'], 'border-color': COLORS['gold_primary'], 'color': COLORS['neutral_text']}),
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Label("Password", html_for="password-input",
                                            style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                    dbc.Input(id="password-input", type="password", placeholder="Enter password",
                                            style={'background-color': COLORS['dark_grey'], 'border-color': COLORS['gold_primary'], 'color': COLORS['neutral_text']}),
                                ], className="mb-4"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("Access Dashboard", id="login-button", color="warning", 
                                                 className="w-100", 
                                                 style={'background-color': COLORS['gold_primary'],
                                                       'border-color': COLORS['gold_primary'],
                                                       'font-weight': '600',
                                                       'padding': '12px',
                                                       'font-family': 'Inter'})
                                    ])
                                ])
                            ]),
                            html.Div(id="login-alert", className="mt-3"),
                            html.Div([
                                html.Small("Demo Credentials:", style={'color': COLORS['neutral_text'], 'display': 'block', 'margin-top': '20px'}),
                                html.Small("admin / dashboard2024", style={'color': COLORS['gold_primary'], 'display': 'block'}),
                                html.Small("client / lexcura2024", style={'color': COLORS['gold_primary'], 'display': 'block'})
                            ], className="text-center")
                        ], style={'text-align': 'center'})
                    ])
                ], style={'background-color': COLORS['dark_grey'], 
                         'border': f'2px solid {COLORS["gold_primary"]}',
                         'border-radius': '15px',
                         'box-shadow': '0 10px 30px rgba(0, 0, 0, 0.5)'}),
            ], width=6, lg=4)
        ], justify="center", className="min-vh-100 align-items-center"),
        dcc.Store(id='session-store'),
        dcc.Store(id='show-intro', data={'show': False})
    ], fluid=True, style={'background-color': COLORS['charcoal']})

# Enhanced Archive page with filtering and search
def get_archive_layout():
    archive_cards = []
    report_types = list(set([item['type'] for item in data['archive']]))
    
    for item in data['archive']:
        card = dbc.Card([
            dbc.CardImg(src=item['thumbnail'], top=True, 
                       style={'height': '120px', 'object-fit': 'contain', 'padding': '20px', 'background-color': COLORS['charcoal']}),
            dbc.CardBody([
                html.H5(item['title'], className="card-title", style={'color': COLORS['gold_primary'], 'font-weight': '600'}),
                html.P(f"Created: {item['date']}", className="card-text", style={'color': COLORS['neutral_text'], 'font-size': '14px'}),
                dbc.Badge(item['type'], color="info", className="mb-2", 
                         style={'background-color': COLORS['deep_blue']}),
                html.Br(),
                dbc.Button("Open Presentation", href=item['url'], target="_blank", 
                          color="warning", className="mt-2",
                          style={'background-color': COLORS['gold_primary'],
                                'border-color': COLORS['gold_primary'],
                                'font-weight': '500'})
            ])
        ], style={'background-color': COLORS['dark_grey'], 
                 'border': f'1px solid {COLORS["gold_primary"]}',
                 'margin-bottom': '20px',
                 'border-radius': '10px',
                 'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
                 'box-shadow': '0 4px 15px rgba(0, 0, 0, 0.3)'})
        archive_cards.append(dbc.Col(card, width=12, md=6, lg=4))
    
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Document Archive - Historical Reports"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3("📊 Google Slides Archive", style={'color': COLORS['gold_primary'], 'margin-bottom': '20px'}),
                                html.P("Access comprehensive historical presentation reports and analytics", 
                                      style={'color': COLORS['neutral_text'], 'font-size': '16px'}),
                                html.Hr(style={'border-color': COLORS['gold_primary']}),
                                
                                # Filter section
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Filter by Report Type:", style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                        dcc.Dropdown(
                                            id='archive-filter',
                                            options=[{'label': 'All Reports', 'value': 'all'}] + 
                                                   [{'label': rt, 'value': rt} for rt in report_types],
                                            value='all',
                                            style={'background-color': COLORS['dark_grey']}
                                        )
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Label("Search:", style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                        dbc.Input(id='archive-search', placeholder="Search reports...", 
                                                style={'background-color': COLORS['dark_grey'], 'border-color': COLORS['gold_primary']})
                                    ], width=6)
                                ], className="mb-4"),
                                
                                dbc.Row(archive_cards, id="archive-cards-container")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}', 'border-radius': '10px'})
                    ])
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Enhanced Google Slides integration
def get_google_slides_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("📈 Live Google Slides Integration"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H3("Current Executive Presentation", style={'color': COLORS['gold_primary']}),
                                html.P("Interactive view of the latest business intelligence presentation", 
                                      style={'color': COLORS['neutral_text']}),
                                html.Hr(style={'border-color': COLORS['gold_primary']}),
                                
                                # Presentation viewer
                                html.Div([
                                    html.Iframe(
                                        src="https://docs.google.com/presentation/d/e/2PACX-1vSampleID/embed?start=false&loop=false&delayms=3000",
                                        style={
                                            'width': '100%',
                                            'height': '600px',
                                            'border': f'3px solid {COLORS["gold_primary"]}',
                                            'border-radius': '10px',
                                            'box-shadow': '0 10px 30px rgba(0, 0, 0, 0.4)'
                                        }
                                    )
                                ], className="mb-4"),
                                
                                # Action buttons
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("🔗 Open in Google Slides", id="open-slides-btn", color="warning",
                                                  size="lg", className="w-100",
                                                  style={'background-color': COLORS['gold_primary'],
                                                        'border-color': COLORS['gold_primary'],
                                                        'font-weight': '600'})
                                    ], width=4),
                                    dbc.Col([
                                        dbc.Button("📥 Download PDF", id="download-slides-btn", color="secondary",
                                                  size="lg", className="w-100",
                                                  style={'font-weight': '600'})
                                    ], width=4),
                                    dbc.Col([
                                        dbc.Button("🔄 Refresh View", id="refresh-slides-btn", color="info",
                                                  size="lg", className="w-100",
                                                  style={'font-weight': '600'})
                                    ], width=4)
                                ])
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}', 'border-radius': '10px'})
                    ])
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Enhanced Settings page
def get_settings_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("⚙️ Dashboard Settings & Configuration"),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Dashboard Preferences", style={'background-color': COLORS['gold_primary'], 'color': COLORS['charcoal'], 'font-weight': '600'}),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Auto-refresh Interval:", style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                        dcc.Dropdown(
                                            id='refresh-interval-setting',
                                            options=[
                                                {'label': '1 minute', 'value': 60000},
                                                {'label': '5 minutes', 'value': 300000},
                                                {'label': '10 minutes', 'value': 600000},
                                                {'label': '30 minutes', 'value': 1800000}
                                            ],
                                            value=300000
                                        )
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Label("Chart Animation:", style={'color': COLORS['neutral_text'], 'font-weight': '500'}),
                                        dbc.Switch(
                                            id="animation-toggle",
                                            label="Enable animations",
                                            value=True,
                                            style={'color': COLORS['neutral_text']}
                                        )
                                    ], width=6)
                                ], className="mb-3"),
                                
                                html.Hr(style={'border-color': COLORS['gold_primary']}),
                                
                                dbc.Row([
                                    dbc.Col([
                                        html.H5("Export Settings", style={'color': COLORS['gold_primary']}),
                                        dbc.Label("Default Export Format:", style={'color': COLORS['neutral_text']}),
                                        dcc.Dropdown(
                                            id='export-format-setting',
                                            options=[
                                                {'label': 'PDF Report', 'value': 'pdf'},
                                                {'label': 'Excel Spreadsheet', 'value': 'excel'},
                                                {'label': 'PowerPoint', 'value': 'pptx'}
                                            ],
                                            value='pdf'
                                        )
                                    ], width=6),
                                    dbc.Col([
                                        html.H5("Notification Settings", style={'color': COLORS['gold_primary']}),
                                        dbc.Switch(
                                            id="notifications-toggle",
                                            label="Enable system notifications",
                                            value=True,
                                            style={'color': COLORS['neutral_text']}
                                        ),
                                        dbc.Switch(
                                            id="email-alerts-toggle",
                                            label="Email critical alerts",
                                            value=False,
                                            style={'color': COLORS['neutral_text']}
                                        )
                                    ], width=6)
                                ])
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}', 'margin-bottom': '20px'}),
                
                # Charts Grid Container with enhanced animations
                html.Div([
                    # Financial Impact Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='financial-impact-chart',
                                figure=create_financial_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Deadline Tracker Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='deadline-tracker-chart',
                                figure=create_deadline_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Alert Severity Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='alert-severity-chart',
                                figure=create_alert_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Historical Trends Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='historical-trends-chart',
                                figure=create_historical_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Growth vs Decline Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='growth-decline-chart',
                                figure=create_growth_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Performance Comparison Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='performance-comparison-chart',
                                figure=create_performance_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Risk & Compliance Gauge
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='risk-compliance-gauge',
                                figure=create_risk_gauge(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                    # Projection & Forecast Chart
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='projection-forecast-chart',
                                figure=create_projection_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card animated-card"),
                    
                ], className="chart-grid"),
                
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

# Enhanced CSS with animations and logo intro
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>LexCura Executive Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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
            
            /* Keyframe animations */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeInScale {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes loadingBar {
                from {
                    transform: scaleX(0);
                }
                to {
                    transform: scaleX(1);
                }
            }
            
            @keyframes pulse {
                0%, 100% {
                    opacity: 1;
                }
                50% {
                    opacity: 0.7;
                }
            }
            
            @keyframes chartEntrance {
                from {
                    opacity: 0;
                    transform: translateY(20px) scale(0.95);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            /* Logo intro animations */
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
            
            .intro-fade-out {
                opacity: 0 !important;
                transform: scale(1.1) !important;
                transition: all 0.8s ease-in-out !important;
            }
            
            /* Sidebar styling */
            .sidebar {
                background: linear-gradient(180deg, #1B1D1F 0%, #0F1113 100%);
                border-right: 3px solid #D4AF37;
                height: 100vh;
                position: fixed;
                width: 280px;
                padding: 30px 20px;
                z-index: 1000;
                box-shadow: 4px 0 25px rgba(0, 0, 0, 0.4);
                animation: slideInRight 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .logo {
                font-size: 18px;
                font-weight: 700;
                color: #D4AF37;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #2A2D30;
                animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
            }
            
            .nav-item {
                color: #B8B9BB;
                padding: 18px 20px;
                margin: 8px 0;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 500;
                border-left: 4px solid transparent;
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) calc(0.1s * var(--index)) both;
            }
            
            .nav-item::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.1), transparent);
                transition: left 0.5s ease;
            }
            
            .nav-item:hover::before {
                left: 100%;
            }
            
            .nav-item:hover {
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(255, 207, 102, 0.1));
                color: #FFCF66;
                border-left-color: #D4AF37;
                transform: translateX(8px) scale(1.02);
                box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2);
            }
            
            .nav-item.active {
                background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(255, 207, 102, 0.15));
                color: #FFCF66;
                border-left-color: #D4AF37;
                transform: translateX(8px);
                box-shadow: 0 8px 25px rgba(212, 175, 55, 0.25);
            }
            
            /* Main content */
            .main-content {
                min-height: 100vh;
                animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.3s both;
            }
            
            .header {
                background: linear-gradient(135deg, #1B1D1F 0%, #2A2D30 50%, #1B1D1F 100%);
                padding: 35px;
                border-radius: 20px;
                margin-bottom: 30px;
                border-left: 6px solid #D4AF37;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                animation: fadeInScale 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #D4AF37, #FFCF66, #D4AF37);
                animation: pulse 2s infinite;
            }
            
            .header h1 {
                color: #D4AF37;
                margin: 0;
                font-size: 36px;
                font-weight: 800;
                letter-spacing: -0.5px;
                text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
            }
            
            .header p {
                color: #B8B9BB;
                margin: 20px 0 0 0;
                font-size: 16px;
                opacity: 0.9;
                font-weight: 400;
            }
            
            /* Enhanced card styling */
            .card {
                background: linear-gradient(145deg, #1B1D1F 0%, #252830 50%, #1B1D1F 100%);
                border-radius: 20px;
                padding: 30px;
                margin: 15px;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
                border: 2px solid #2A2D30;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #D4AF37, #FFCF66);
                transform: scaleX(0);
                transform-origin: left;
                transition: transform 0.3s ease;
            }
            
            .card::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent 30%, rgba(212, 175, 55, 0.05) 50%, transparent 70%);
                transform: rotate(-45deg);
                transition: all 0.6s ease;
                opacity: 0;
            }
            
            .card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
                border-color: #D4AF37;
            }
            
            .card:hover::before {
                transform: scaleX(1);
            }
            
            .card:hover::after {
                opacity: 1;
                transform: rotate(-45deg) translate(50%, 50%);
            }
            
            /* Animated card entrance */
            .animated-card {
                animation: chartEntrance 0.8s cubic-bezier(0.4, 0, 0.2, 1) calc(0.1s * var(--index)) both;
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
                gap: 25px;
                margin-top: 25px;
            }
            
            .chart-grid .card:nth-child(1) { --index: 1; }
            .chart-grid .card:nth-child(2) { --index: 2; }
            .chart-grid .card:nth-child(3) { --index: 3; }
            .chart-grid .card:nth-child(4) { --index: 4; }
            .chart-grid .card:nth-child(5) { --index: 5; }
            .chart-grid .card:nth-child(6) { --index: 6; }
            .chart-grid .card:nth-child(7) { --index: 7; }
            .chart-grid .card:nth-child(8) { --index: 8; }
            
            /* Loading spinner customization */
            ._dash-loading {
                color: #D4AF37 !important;
            }
            
            ._dash-loading-callback {
                background-color: rgba(15, 17, 19, 0.8) !important;
                border-radius: 20px;
            }
            
            /* Status indicator animation */
            .status-indicator {
                animation: pulse 2s infinite;
            }
            
            /* Button enhancements */
            .btn {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 600;
                border-radius: 10px;
                position: relative;
                overflow: hidden;
            }
            
            .btn::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
                transform: translate(-50%, -50%);
            }
            
            .btn:hover::before {
                width: 300px;
                height: 300px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            }
            
            /* Mobile responsive */
            @media (max-width: 1200px) {
                .chart-grid {
                    grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
                    gap: 20px;
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
                
                .card {
                    margin: 8px;
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 28px;
                }
            }
            
            @media (max-width: 600px) {
                .header {
                    padding: 25px;
                }
                
                .card {
                    padding: 20px;
                    margin: 5px;
                }
                
                .header h1 {
                    font-size: 24px;
                }
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0F1113;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #D4AF37, #FFCF66);
                border-radius: 5px;
                border: 2px solid #0F1113;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(180deg, #FFCF66, #D4AF37);
            }
            
            /* Custom dropdown styling */
            .Select-control {
                background-color: #1B1D1F !important;
                border-color: #D4AF37 !important;
                color: #B8B9BB !important;
            }
            
            .Select-menu {
                background-color: #1B1D1F !important;
                border-color: #D4AF37 !important;
            }
            
            .Select-option {
                background-color: #1B1D1F !important;
                color: #B8B9BB !important;
            }
            
            .Select-option:hover {
                background-color: #2A2D30 !important;
                color: #FFCF66 !important;
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
            // Logo intro animation script
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
            
            // Add stagger animation to nav items
            document.addEventListener('DOMContentLoaded', function() {
                const navItems = document.querySelectorAll('.nav-item');
                navItems.forEach((item, index) => {
                    item.style.setProperty('--index', index);
                });
            });
        </script>
    </body>
</html>
'''

# Main app layout with URL routing and logo intro
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Store(id='show-intro', storage_type='session', data={'show': False}),
    html.Div(id='page-content')
])

# Main page routing callback with logo intro
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('intro-timer', 'n_intervals')],
    [State('session-store', 'data'),
     State('show-intro', 'data')]
)
def display_page(pathname, intro_intervals, session_data, intro_data):
    session_id = session_data.get('session_id') if session_data else None
    
    # Check authentication
    if not session_id or not is_authenticated(session_id):
        return get_login_layout()
    
    # Show logo intro only once after login
    if intro_data and not intro_data.get('intro_shown', False):
        if intro_intervals == 0:
            return get_logo_intro()
    
    # Route to appropriate page
    if pathname == '/archive':
        return get_archive_layout()
    elif pathname == '/slides':
        return get_google_slides_layout()
    elif pathname == '/analytics':
        return get_dashboard_layout()
    elif pathname == '/reports':
        return get_dashboard_layout()
    elif pathname == '/settings':
        return get_settings_layout()
    else:
        return get_dashboard_layout()

# Login callback with intro trigger
@app.callback(
    [Output('session-store', 'data'),
     Output('login-alert', 'children'),
     Output('url', 'pathname'),
     Output('show-intro', 'data')],
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'),
     State('password-input', 'value')]
)
def handle_login(n_clicks, username, password):
    if n_clicks and username and password:
        if verify_credentials(username, password):
            session_id = generate_session_id()
            session_store[session_id] = {
                'username': username,
                'login_time': datetime.now()
            }
            return (
                {'session_id': session_id, 'username': username},
                dbc.Alert("Login successful!", color="success"),
                "/",
                {'show': True, 'intro_shown': False}
            )
        else:
            return (
                {},
                dbc.Alert("Invalid credentials. Please try again.", color="danger"),
                "/login",
                {'show': False, 'intro_shown': True}
            )
    return {}, "", "/login", {'show': False, 'intro_shown': True}

# Logo intro completion callback
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

# Enhanced navigation callbacks
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
    
    navigation_map = {
        'nav-overview': "/",
        'nav-analytics': "/analytics", 
        'nav-reports': "/reports",
        'nav-slides': "/slides",
        'nav-archive': "/archive",
        'nav-settings': "/settings"
    }
    
    return navigation_map.get(button_id, "/")

# Enhanced dashboard refresh callback with animations
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
        
        # Add realistic variations for live data simulation
        if n_intervals > 0 or refresh_clicks:
            # Vary financial data with market-like fluctuations
            for i in range(len(data['financial']['current'])):
                variation = random.uniform(-0.03, 0.04)  # ±3-4% variation
                data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
            
            # Adjust risk score gradually
            risk_change = random.uniform(-1.5, 1.5)
            data['risk_score'] = max(0, min(100, data['risk_score'] + risk_change))
            
            # Update some deadlines (simulate project progress)
            for i in range(len(data['deadlines']['progress'])):
                if random.random() < 0.3:  # 30% chance of progress update
                    progress_increase = random.uniform(1, 5)
                    data['deadlines']['progress'][i] = min(100, data['deadlines']['progress'][i] + progress_increase)
        
        current_time = datetime.now().strftime('%I:%M %p')
        status_indicator = [
            html.Span("● ", style={'color': COLORS['success_green'], 'font-size': '20px'}),
            html.Span(f"Live Data - Updated at {current_time}", 
                     style={'color': COLORS['neutral_text'], 'font-weight': '500'})
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
                                    filename=f"LexCura_Executive_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        except Exception as e:
            print(f"Error exporting PDF: {str(e)}")
    return None

# PDF generation function
def generate_pdf_report():
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Enhanced title with styling
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            textColor=HexColor('#D4AF37'),
            alignment=1  # Center alignment
        )
        story.append(Paragraph("LexCura Executive Dashboard", title_style))
        story.append(Paragraph("Business Intelligence Report", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Executive summary
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Financial Summary Table
        story.append(Paragraph("Executive Financial Summary", styles['Heading2']))
        financial_data_table = [
            ['Metric', 'Current Period', 'Previous Period', 'Change (%)', 'Status'],
        ]
        
        for i, category in enumerate(data['financial']['categories']):
            current = data['financial']['current'][i] if i < len(data['financial']['current']) else 0
            previous = data['financial']['previous'][i] if i < len(data['financial']['previous']) else 1
            change = ((current - previous) / previous * 100) if previous != 0 else 0
            status = "↗ Positive" if change > 0 else "↘ Negative" if change < 0 else "→ Stable"
            
            financial_data_table.append([
                category,
                f"${current:,.0f}",
                f"${previous:,.0f}",
                f"{change:+.1f}%",
                status
            ])
        
        table = Table(financial_data_table, colWidths=[2.5*72, 1.5*72, 1.5*72, 1*72, 1*72])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D4AF37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#0F1113')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F8F8')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#FFFFFF'), HexColor('#F8F8F8')])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Risk Assessment
        story.append(Paragraph("Risk & Compliance Assessment", styles['Heading2']))
        risk_color = "Green" if data['risk_score'] <= 30 else "Yellow" if data['risk_score'] <= 70 else "Red"
        story.append(Paragraph(f"Current Risk Score: <b>{data['risk_score']}/100</b> ({risk_color} Zone)", styles['Normal']))
        story.append(Paragraph("Risk levels are continuously monitored across all business operations.", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Project Status
        story.append(Paragraph("Critical Project Status", styles['Heading2']))
        critical_projects = [task for i, task in enumerate(data['deadlines']['tasks']) 
                           if data['deadlines']['urgency'][i] == 'Critical']
        if critical_projects:
            story.append(Paragraph(f"Critical Projects Requiring Attention: {', '.join(critical_projects)}", styles['Normal']))
        else:
            story.append(Paragraph("All projects are on track with no critical deadlines.", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None

# Google Slides callbacks
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('open-slides-btn', 'n_clicks'),
    prevent_initial_call=True
)
def open_google_slides(n_clicks):
    if n_clicks:
        # In production, this would open the actual Google Slides URL
        return "/slides"
    return dash.no_update

# Archive filtering callback
@app.callback(
    Output('archive-cards-container', 'children'),
    [Input('archive-filter', 'value'),
     Input('archive-search', 'value')]
)
def filter_archive(filter_value, search_value):
    filtered_data = data['archive']
    
    # Apply type filter
    if filter_value and filter_value != 'all':
        filtered_data = [item for item in filtered_data if item['type'] == filter_value]
    
    # Apply search filter
    if search_value:
        search_lower = search_value.lower()
        filtered_data = [item for item in filtered_data 
                        if search_lower in item['title'].lower() or search_lower in item['type'].lower()]
    
    # Generate filtered cards
    archive_cards = []
    for item in filtered_data:
        card = dbc.Card([
            dbc.CardImg(src=item['thumbnail'], top=True, 
                       style={'height': '120px', 'object-fit': 'contain', 'padding': '20px', 'background-color': COLORS['charcoal']}),
            dbc.CardBody([
                html.H5(item['title'], className="card-title", style={'color': COLORS['gold_primary'], 'font-weight': '600'}),
                html.P(f"Created: {item['date']}", className="card-text", style={'color': COLORS['neutral_text'], 'font-size': '14px'}),
                dbc.Badge(item['type'], color="info", className="mb-2", 
                         style={'background-color': COLORS['deep_blue']}),
                html.Br(),
                dbc.Button("Open Presentation", href=item['url'], target="_blank", 
                          color="warning", className="mt-2",
                          style={'background-color': COLORS['gold_primary'],
                                'border-color': COLORS['gold_primary'],
                                'font-weight': '500'})
            ])
        ], style={'background-color': COLORS['dark_grey'], 
                 'border': f'1px solid {COLORS["gold_primary"]}',
                 'margin-bottom': '20px',
                 'border-radius': '10px',
                 'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
                 'box-shadow': '0 4px 15px rgba(0, 0, 0, 0.3)'})
        archive_cards.append(dbc.Col(card, width=12, md=6, lg=4))
    
    if not archive_cards:
        return [dbc.Col([
            html.Div([
                html.H4("No Results Found", style={'color': COLORS['neutral_text']}),
                html.P("Try adjusting your search criteria.", style={'color': COLORS['neutral_text']})
            ], style={'text-align': 'center', 'padding': '50px'})
        ], width=12)]
    
    return archive_cards

# Settings callbacks
@app.callback(
    Output('auto-refresh-interval', 'interval'),
    Input('refresh-interval-setting', 'value')
)
def update_refresh_interval(interval_value):
    return interval_value if interval_value else 300000

# Fullscreen callback
@app.callback(
    Output('dashboard-content', 'style'),
    Input('fullscreen-btn', 'n_clicks'),
    State('dashboard-content', 'style'),
    prevent_initial_call=True
)
def toggle_fullscreen(n_clicks, current_style):
    if n_clicks and n_clicks % 2 == 1:
        # Fullscreen mode
        return {
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'background-color': COLORS['charcoal'],
            'z-index': '9998',
            'overflow': 'auto',
            'padding': '20px'
        }
    else:
        # Normal mode
        return current_style or {}

# Health check endpoint for deployment
@app.server.route('/health')
def health_check():
    return {
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'version': '2.1.0',
        'features': ['authentication', 'charts', 'pdf_export', 'google_slides', 'archive']
    }

# Performance monitoring endpoint
@app.server.route('/metrics')
def metrics():
    return {
        'active_sessions': len(session_store),
        'charts_loaded': 8,
        'last_data_update': datetime.now().isoformat(),
        'system_status': 'operational'
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=port,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )20px'})
                    ])
                ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("System Information", style={'background-color': COLORS['deep_blue'], 'color': 'white', 'font-weight': '600'}),
                            dbc.CardBody([
                                html.P(f"Dashboard Version: 2.1.0", style={'color': COLORS['neutral_text']}),
                                html.P(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style={'color': COLORS['neutral_text']}),
                                html.P(f"Active Charts: 8", style={'color': COLORS['neutral_text']}),
                                html.P(f"Data Sources: 5", style={'color': COLORS['neutral_text']}),
                                dbc.Button("Clear Cache", color="warning", size="sm", 
                                          style={'background-color': COLORS['warning_orange'], 'border-color': COLORS['warning_orange']})
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["deep_blue"]}', 'border-radius': '10px'})
                    ], width=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("User Session", style={'background-color': COLORS['success_green'], 'color': 'white', 'font-weight': '600'}),
                            dbc.CardBody([
                                html.P(f"Login Time: {datetime.now().strftime('%H:%M:%S')}", style={'color': COLORS['neutral_text']}),
                                html.P(f"Session Duration: Active", style={'color': COLORS['neutral_text']}),
                                html.P(f"Role: Executive", style={'color': COLORS['neutral_text']}),
                                html.P(f"Access Level: Full", style={'color': COLORS['neutral_text']}),
                                dbc.Button("Download Session Log", color="info", size="sm")
                            ])
                        ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["success_green"]}', 'border-radius': '10px'})
                    ], width=6)
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

def get_sidebar():
    return html.Div([
        html.Div([
            html.Img(src="/assets/lexcura_logo.png", style={'width': '40px', 'height': 'auto', 'margin-right': '15px'}),
            html.Span("LexCura Dashboard", style={'font-size': '22px', 'font-weight': '700'})
        ], className="logo", style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Overview")
            ], id="nav-overview", className="nav-item", n_clicks=0),
            
            html.Div([
                html.I(className="fas fa-analytics", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Analytics")
            ], id="nav-analytics", className="nav-item", n_clicks=0),
            
            html.Div([
                html.I(className="fas fa-file-alt", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Reports")
            ], id="nav-reports", className="nav-item", n_clicks=0),
            
            html.Div([
                html.I(className="fas fa-presentation", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Google Slides")
            ], id="nav-slides", className="nav-item", n_clicks=0),
            
            html.Div([
                html.I(className="fas fa-archive", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Archive")
            ], id="nav-archive", className="nav-item", n_clicks=0),
            
            html.Div([
                html.I(className="fas fa-cog", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Settings")
            ], id="nav-settings", className="nav-item", n_clicks=0),
            
            html.Hr(style={'border-color': COLORS['gold_primary'], 'margin': '25px 0'}),
            
            html.Div([
                html.I(className="fas fa-sign-out-alt", style={'margin-right': '15px', 'width': '20px'}),
                html.Span("Logout")
            ], id="logout-btn", className="nav-item", n_clicks=0,
                    style={'color': COLORS['danger_red']})
        ])
    ], className="sidebar")

def get_header(title):
    return html.Div([
        html.H1(title, style={'margin-bottom': '10px'}),
        html.P(f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", 
               style={'margin': '0', 'font-size': '14px', 'opacity': '0.8'})
    ], className="header")

# Enhanced main dashboard layout
def get_dashboard_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("🎯 Executive Business Intelligence Dashboard"),
            html.Div([
                # Enhanced control panel
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.ButtonGroup([
                                    dbc.Button([html.I(className="fas fa-file-pdf", style={'margin-right': '8px'}), "Export PDF"], 
                                              id="export-pdf-btn", color="warning",
                                              style={'background-color': COLORS['gold_primary'], 'border-color': COLORS['gold_primary']}),
                                    dbc.Button([html.I(className="fas fa-sync-alt", style={'margin-right': '8px'}), "Refresh Data"], 
                                              id="refresh-data-btn", color="secondary"),
                                    dbc.Button([html.I(className="fas fa-expand", style={'margin-right': '8px'}), "Full Screen"], 
                                              id="fullscreen-btn", color="info")
                                ])
                            ], width=8),
                            dbc.Col([
                                html.Div(id='status-indicator', children=[
                                    html.Span("● ", style={'color': COLORS['success_green'], 'font-size': '20px'}),
                                    html.Span("System Operational", style={'color': COLORS['neutral_text'], 'font-weight': '500'})
                                ], style={'text-align': 'right', 'padding': '8px 0'})
                            ], width=4)
                        ])
                    ])
                ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}', 'margin-bottom': '

# UI-REFACTOR-GOLD-2025: Elite Fortune-500 dashboard transformation
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math
import os

# UI-REFACTOR-GOLD-2025: Import elite plotly theme
from plotly_templates import register_gold_dark_template, styled_plotly_chart

# Initialize the Dash app with elite assets
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                assets_folder='assets',
                external_stylesheets=[
                    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
                ])
server = app.server  # Required for Render deployment

# UI-REFACTOR-GOLD-2025: Initialize elite theme
register_gold_dark_template()

# UI-REFACTOR-GOLD-2025: Elite color palette (exact Fortune-500 specification)
ELITE_COLORS = {
    'charcoal': '#0F1113',
    'dark_card': '#1B1D1F', 
    'soft_surface': '#252728',
    'gold_primary': '#D4AF37',
    'gold_highlight': '#FFCF66',
    'neutral_text': '#B8B9BB',
    'high_contrast': '#F5F6F7',
    'error_subtle': '#E4574C',
    'success_subtle': '#3DBC6B'
}

# Preserve existing data generation logic (DO NOT CHANGE)
def generate_sample_data():
    try:
        random.seed(42)
        
        financial_data = {
            'categories': ['Revenue', 'Operating Costs', 'Net Profit', 'Investments', 'Returns'],
            'current': [2850000, -1320000, 1530000, -480000, 720000],
            'previous': [2600000, -1450000, 1150000, -520000, 580000]
        }
        
        deadline_data = {
            'tasks': ['Q4 Financial Report', 'System Infrastructure Upgrade', 'Compliance Audit Review', 'Annual Budget Planning', 'Security Assessment'],
            'days_left': [3, 15, 1, 12, 8],
            'progress': [85, 45, 95, 60, 70]
        }
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        alert_data = {
            'severity': ['Critical', 'Warning', 'Info'],
            'count': [8, 24, 42]
        }
        
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
        
        growth_data = {
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            'growth_rate': [12, 18, 15, 22, 28, 25, 30, 35],
            'decline_rate': [5, 8, 4, 6, 9, 7, 8, 6]
        }
        
        performance_data = {
            'kpis': ['Operational Efficiency', 'Quality Score', 'Response Time', 'Cost Optimization', 'Customer Satisfaction'],
            'current_score': [85, 92, 78, 88, 91],
            'target_score': [90, 95, 85, 90, 95],
            'industry_avg': [75, 85, 80, 82, 87]
        }
        
        risk_score = 68
        
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

# Initialize data (preserve existing logic)
data = generate_sample_data()

# UI-REFACTOR-GOLD-2025: Elite KPI calculation helpers
def calculate_kpi_metrics():
    """Calculate top-level KPIs for the executive summary row"""
    try:
        total_revenue = data['financial']['current'][0]
        previous_revenue = data['financial']['previous'][0]
        revenue_change = ((total_revenue - previous_revenue) / previous_revenue) * 100
        
        total_alerts = sum(data['alerts']['count'])
        critical_alerts = data['alerts']['count'][0] if len(data['alerts']['count']) > 0 else 0
        
        avg_performance = sum(data['performance']['current_score']) / len(data['performance']['current_score'])
        
        active_projects = len(data['deadlines']['tasks'])
        critical_deadlines = len([d for d in data['deadlines']['urgency'] if d == 'Critical'])
        
        return {
            'revenue': {'value': total_revenue, 'delta': revenue_change, 'format': 'currency'},
            'alerts': {'value': total_alerts, 'delta': -12.5, 'format': 'number'},
            'performance': {'value': avg_performance, 'delta': 5.2, 'format': 'percent'},
            'projects': {'value': active_projects, 'delta': 0, 'format': 'number'},
            'risk_score': {'value': data['risk_score'], 'delta': -8.3, 'format': 'score'}
        }
    except:
        return {
            'revenue': {'value': 2850000, 'delta': 9.6, 'format': 'currency'},
            'alerts': {'value': 74, 'delta': -12.5, 'format': 'number'},
            'performance': {'value': 86.8, 'delta': 5.2, 'format': 'percent'},
            'projects': {'value': 5, 'delta': 0, 'format': 'number'},
            'risk_score': {'value': 68, 'delta': -8.3, 'format': 'score'}
        }

# UI-REFACTOR-GOLD-2025: Elite chart creation functions (preserve data logic)
def create_financial_chart():
    try:
        fig = go.Figure()
        
        colors_current = [ELITE_COLORS['success_subtle'] if x > 0 else ELITE_COLORS['error_subtle'] for x in data['financial']['current']]
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<br><extra></extra>',
            text=[f"${x:,.0f}" for x in data['financial']['current']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=ELITE_COLORS['gold_primary'],
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<br><extra></extra>'
        ))
        
        fig.update_layout(
            title='Financial Impact Analysis',
            yaxis_tickformat='$,.0f',
            barmode='group'
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating financial chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_deadline_chart():
    try:
        urgency_colors = {
            'Critical': ELITE_COLORS['error_subtle'],
            'Warning': ELITE_COLORS['gold_highlight'], 
            'Normal': ELITE_COLORS['success_subtle']
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
        
        fig.update_layout(
            title='Project Deadline Tracker',
            xaxis_title='Days Remaining'
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating deadline chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_alert_chart():
    try:
        severity_colors = [ELITE_COLORS['error_subtle'], ELITE_COLORS['gold_highlight'], ELITE_COLORS['success_subtle']]
        
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
            font={'size': 16, 'color': ELITE_COLORS['high_contrast']},
            showarrow=False
        )
        
        fig.update_layout(
            title='Alert Severity Distribution',
            showlegend=False
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating alert chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_historical_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['performance'],
            mode='lines',
            line={'color': ELITE_COLORS['gold_primary'], 'width': 3},
            fill='tonexty',
            fillcolor=f"rgba(212, 175, 55, 0.3)",
            name='Performance Metric',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Performance: %{y:,.1f}<extra></extra>'
        ))
        
        fig.add_hline(
            y=data['historical']['target'],
            line_dash="dash",
            line_color=ELITE_COLORS['success_subtle'],
            line_width=2,
            annotation_text="Performance Target",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title='Historical Performance Trends',
            xaxis_title='Date',
            yaxis_title='Performance Score'
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating historical chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_growth_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data['growth']['months'],
            y=data['growth']['growth_rate'],
            name='Growth Rate',
            marker_color=ELITE_COLORS['success_subtle'],
            hovertemplate='<b>%{x}</b><br>Growth: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['growth_rate']],
            textposition='outside'
        ))
        
        decline_negative = [-rate for rate in data['growth']['decline_rate']]
        fig.add_trace(go.Bar(
            x=data['growth']['months'],
            y=decline_negative,
            name='Decline Rate',
            marker_color=ELITE_COLORS['error_subtle'],
            hovertemplate='<b>%{x}</b><br>Decline: %{y}%<extra></extra>',
            text=[f"-{rate}%" for rate in data['growth']['decline_rate']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Growth vs Decline Analysis',
            yaxis_title='Rate (%)',
            yaxis_ticksuffix='%',
            xaxis_title='Month'
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating growth chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_performance_chart():
    try:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['current_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Current Performance',
            line_color=ELITE_COLORS['gold_primary'],
            fillcolor=f"rgba(212, 175, 55, 0.4)",
            hovertemplate='<b>%{theta}</b><br>Current: %{r}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            fill='toself',
            name='Target',
            line_color=ELITE_COLORS['success_subtle'],
            fillcolor=f"rgba(61, 188, 107, 0.2)",
            hovertemplate='<b>%{theta}</b><br>Target: %{r}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['industry_avg'],
            theta=data['performance']['kpis'],
            mode='lines',
            name='Industry Average',
            line_color=ELITE_COLORS['neutral_text'],
            line_dash='dot',
            hovertemplate='<b>%{theta}</b><br>Industry Avg: %{r}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Performance vs Target KPIs',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    color=ELITE_COLORS['neutral_text'],
                    ticksuffix='%'
                ),
                angularaxis=dict(color=ELITE_COLORS['neutral_text'])
            )
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating performance chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

def create_risk_gauge():
    try:
        if data['risk_score'] <= 30:
            gauge_color = ELITE_COLORS['success_subtle']
        elif data['risk_score'] <= 70:
            gauge_color = ELITE_COLORS['gold_highlight']
        else:
            gauge_color = ELITE_COLORS['error_subtle']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=data['risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk & Compliance Score", 'font': {'color': ELITE_COLORS['high_contrast'], 'size': 16}},
            delta={
                'reference': 50,
                'increasing': {'color': ELITE_COLORS['error_subtle']},
                'decreasing': {'color': ELITE_COLORS['success_subtle']}
            },
            gauge={
                'axis': {
                    'range': [None, 100],
                    'tickcolor': ELITE_COLORS['neutral_text'],
                    'tickfont': {'color': ELITE_COLORS['neutral_text']}
                },
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(61, 188, 107, 0.3)'},
                    {'range': [30, 70], 'color': 'rgba(255, 207, 102, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(228, 87, 76, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': ELITE_COLORS['neutral_text'], 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            },
            number={'font': {'color': ELITE_COLORS['high_contrast'], 'size': 24}}
        ))
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating risk gauge: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

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
            line={'color': ELITE_COLORS['gold_primary'], 'width': 4},
            marker={'size': 8, 'color': ELITE_COLORS['gold_highlight']},
            name='Revenue Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='12-Month Revenue Projection',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            yaxis_tickformat='$,.0f'
        )
        
        return styled_plotly_chart(fig, height=420)
    except Exception as e:
        print(f"Error creating projection chart: {str(e)}")
        return go.Figure().add_annotation(text="Chart Loading Error", x=0.5, y=0.5)

# UI-REFACTOR-GOLD-2025: Elite UI components
def create_elite_header():
    """Create the elite Fortune-500 header component"""
    return html.Div([
        # UI-REFACTOR-GOLD-2025: Animated background
        html.Div(className="animated-background"),
        html.Div(className="particle-overlay"),
        
        html.Div([
            html.Div([
                html.Img(src='/assets/lexcuralogo.png', style={'height': '32px'}, className="header-logo"),
                html.H1("LexCura Executive Dashboard", className="app-title")
            ], className="logo-section"),
            
            html.Div([
                html.Span(f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", 
                         className="last-updated")
            ])
        ], className="header-content")
    ], className="elite-header")

def create_elite_sidebar():
    """Create the collapsible elite sidebar"""
    return html.Div([
        html.Div([
            html.Div("LexCura", className="sidebar-logo")
        ], className="sidebar-header"),
        
        html.Div([
            html.Div([
                html.Span("📊"), 
                html.Span(" Overview")
            ], className="nav-item active"),
            html.Div([
                html.Span("📈"), 
                html.Span(" Analytics")
            ], className="nav-item"),
            html.Div([
                html.Span("📋"), 
                html.Span(" Reports")
            ], className="nav-item"),
            html.Div([
                html.Span("⚙️"), 
                html.Span(" Settings")
            ], className="nav-item"),
            html.Div([
                html.Span("🔒"), 
                html.Span(" Security")
            ], className="nav-item")
        ], className="nav-section")
    ], className="elite-sidebar")

def create_kpi_row():
    """Create the elite KPI summary row"""
    kpis = calculate_kpi_metrics()
    
    def format_kpi_value(value, format_type):
        if format_type == 'currency':
            return f"${value:,.0f}"
        elif format_type == 'percent':
            return f"{value:.1f}%"
        elif format_type == 'score':
            return f"{value:.0f}/100"
        else:
            return f"{value:,.0f}"
    
    def create_kpi_card(title, kpi_data):
        value = kpi_data['value']
        delta = kpi_data['delta']
        format_type = kpi_data['format']
        
        delta_class = "kpi-delta" if delta >= 0 else "kpi-delta negative"
        delta_symbol = "↗" if delta >= 0 else "↘"
        
        return html.Div([
            html.Div(title.upper(), className="kpi-label"),
            html.Div(format_kpi_value(value, format_type), className="kpi-value"),
            html.Div([
                html.Span(delta_symbol),
                html.Span(f"{abs(delta):.1f}%")
            ], className=delta_class),
            # UI-REFACTOR-GOLD-2025: Add sparkline placeholder
            html.Div(className="kpi-sparkline")
        ], className="kpi-card")
    
    return html.Div([
        create_kpi_card("Total Revenue", kpis['revenue']),
        create_kpi_card("Active Alerts", kpis['alerts']),
        create_kpi_card("Performance Score", kpis['performance']),
        create_kpi_card("Active Projects", kpis['projects']),
        create_kpi_card("Risk Level", kpis['risk_score'])
    ], className="kpi-row")

# UI-REFACTOR-GOLD-2025: Elite layout structure
app.layout = html.Div([
    create_elite_header(),
    create_elite_sidebar(),
    
    html.Div([
        create_kpi_row(),
        
        # UI-REFACTOR-GOLD-2025: Elite chart grid with proper responsive columns
        html.Div([
            html.Div([
                dcc.Graph(
                    id='financial-impact-chart',
                    figure=create_financial_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            html.Div([
                dcc.Graph(
                    id='deadline-tracker-chart',
                    figure=create_deadline_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            html.Div([
                dcc.Graph(
                    id='alert-severity-chart',
                    figure=create_alert_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third"),
            
            html.Div([
                dcc.Graph(
                    id='historical-trends-chart',
                    figure=create_historical_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third"),
            
            html.Div([
                dcc.Graph(
                    id='risk-compliance-gauge',
                    figure=create_risk_gauge(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third"),
            
            html.Div([
                dcc.Graph(
                    id='growth-decline-chart',
                    figure=create_growth_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            html.Div([
                dcc.Graph(
                    id='performance-comparison-chart',
                    figure=create_performance_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            html.Div([
                dcc.Graph(
                    id='projection-forecast-chart',
                    figure=create_projection_chart(),
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-full")
            
        ], className="chart-grid"),
        
        # Auto-refresh interval (preserve existing logic)
        dcc.Interval(
            id='auto-refresh-interval',
            interval=300000,
            n_intervals=0
        ),
        
        # UI-REFACTOR-GOLD-2025: Elite status indicator
        html.Div([
            html.Div(id='status-indicator', children=[
                html.Span("🟢 ", className="status-online"),
                html.Span("System Online - Real-time Data", style={'color': ELITE_COLORS['neutral_text']})
            ], style={'text-align': 'center', 'padding': '20px', 'font-size': '13px'})
        ])
        
    ], className="main-content")
])

# Preserve existing callback (DO NOT CHANGE DATA LOGIC)
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
    """Auto-refresh all charts every 5 minutes (preserve existing logic)"""
    try:
        global data
        
        if n_intervals > 0:
            for i in range(len(data['financial']['current'])):
                variation = random.uniform(-0.05, 0.05)
                data['financial']['current'][i] = int(data['financial']['current'][i] * (1 + variation))
            
            data['risk_score'] = max(0, min(100, data['risk_score'] + random.uniform(-3, 3)))
        
        current_time = datetime.now().strftime('%I:%M %p')
        status_indicator = [
            html.Span("🟢 ", className="status-online"),
            html.Span(f"Live Data - Updated at {current_time}", 
                     style={'color': ELITE_COLORS['neutral_text']})
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
        error_status = [
            html.Span("🔴 ", className="status-error"),
            html.Span("Update Error - Using Cached Data", 
                     style={'color': ELITE_COLORS['neutral_text']})
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

# Preserve existing health check and main entry point
@app.server.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=port
    )

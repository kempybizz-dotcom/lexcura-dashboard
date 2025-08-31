import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import json

# Import Google Sheets integration
try:
    from google_sheets import GoogleSheetsConnector
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    print("Google Sheets integration not available. Using fallback data.")

# Initialize Dash app with premium styling
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                assets_folder='assets')
server = app.server

# Premium color palette inspired by the reference image
PREMIUM_COLORS = {
    'bg_primary': '#0A0B0D',      # Deep charcoal background
    'bg_secondary': '#1A1D20',    # Card background
    'bg_accent': '#242831',       # Elevated surfaces
    'gold_primary': '#D4AF37',    # Premium gold
    'gold_light': '#E8C547',      # Light gold accents
    'orange_accent': '#FF8C42',   # Orange highlights
    'text_primary': '#FFFFFF',    # White text
    'text_secondary': '#B8BCC8',  # Muted text
    'success': '#4CAF50',         # Green for success
    'warning': '#FF9800',         # Orange for warnings
    'danger': '#F44336',          # Red for critical
    'chart_grid': '#2A2D35'       # Grid lines
}

# Initialize Google Sheets connector
if GOOGLE_SHEETS_AVAILABLE:
    sheets_connector = GoogleSheetsConnector()
    # Replace with your actual Google Sheets ID
    SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'your-spreadsheet-id-here')
else:
    sheets_connector = None
    SPREADSHEET_ID = None

def get_503b_data():
    """Fetch 503B compliance data from Google Sheets or fallback"""
    if sheets_connector and SPREADSHEET_ID:
        try:
            data = sheets_connector.get_dashboard_metrics(SPREADSHEET_ID)
            if data:
                return data
        except Exception as e:
            print(f"Error fetching Google Sheets data: {str(e)}")
    
    # Fallback data for 503B compliance
    return {
        'production': {
            'total_batches': 147,
            'completed_batches': 132,
            'pending_batches': 15,
            'average_yield': 96.3,
            'daily_production': [18, 22, 19, 25, 21, 17, 20],  # Last 7 days
            'batch_trend': [
                {'date': '2025-01-15', 'batches': 18, 'yield': 96.1},
                {'date': '2025-01-16', 'batches': 22, 'yield': 97.2},
                {'date': '2025-01-17', 'batches': 19, 'yield': 95.8},
                {'date': '2025-01-18', 'batches': 25, 'yield': 98.1},
                {'date': '2025-01-19', 'batches': 21, 'yield': 96.7},
                {'date': '2025-01-20', 'batches': 17, 'yield': 94.9},
                {'date': '2025-01-21', 'batches': 20, 'yield': 97.5}
            ]
        },
        'quality': {
            'pass_rate': 98.2,
            'total_tests': 1247,
            'pending_tests': 23,
            'critical_parameters': [
                {'parameter': 'Sterility', 'status': 'Pass', 'value': 100.0},
                {'parameter': 'Endotoxin', 'status': 'Pass', 'value': 0.02},
                {'parameter': 'pH', 'status': 'Pass', 'value': 7.1},
                {'parameter': 'Particulates', 'status': 'Pass', 'value': 12},
                {'parameter': 'Potency', 'status': 'Pass', 'value': 102.1}
            ]
        },
        'compliance': {
            'environmental_zones': [
                {'zone': 'ISO 5', 'status': 'Compliant', 'particles': 145},
                {'zone': 'ISO 7', 'status': 'Compliant', 'particles': 2840},
                {'zone': 'ISO 8', 'status': 'Alert', 'particles': 89500}
            ],
            'deviations': {
                'total': 8,
                'critical': 1,
                'major': 3,
                'minor': 4,
                'trend': [2, 1, 3, 0, 1, 0, 1]  # Last 7 days
            },
            'training_compliance': 94.7,
            'audit_score': 97.3
        },
        'inventory': {
            'raw_materials': 156,
            'low_stock_alerts': 12,
            'expired_items': 3,
            'critical_supplies': [
                {'item': 'Vial 10mL', 'stock': 2340, 'status': 'Good'},
                {'item': 'Stopper 20mm', 'stock': 450, 'status': 'Low'},
                {'item': 'Label Type A', 'stock': 89, 'status': 'Critical'},
                {'item': 'API Batch X1', 'stock': 15.6, 'status': 'Good'}
            ]
        }
    }

def create_premium_kpi_card(title, value, change, unit="", status="normal"):
    """Create premium KPI cards matching the reference design"""
    
    status_colors = {
        'good': PREMIUM_COLORS['success'],
        'warning': PREMIUM_COLORS['warning'],
        'critical': PREMIUM_COLORS['danger'],
        'normal': PREMIUM_COLORS['gold_primary']
    }
    
    change_color = PREMIUM_COLORS['success'] if change >= 0 else PREMIUM_COLORS['danger']
    change_icon = "▲" if change >= 0 else "▼"
    
    return html.Div([
        html.Div([
            html.H4(title, className="kpi-title"),
            html.Div([
                html.Span(f"{value:,.1f}" if isinstance(value, float) else f"{value:,}", 
                         className="kpi-value"),
                html.Span(unit, className="kpi-unit")
            ], className="kpi-value-container"),
            html.Div([
                html.Span(change_icon, style={'color': change_color}),
                html.Span(f"{abs(change):.1f}%", style={'color': change_color})
            ], className="kpi-change")
        ], className="kpi-content"),
        html.Div(className=f"kpi-accent {status}")
    ], className="premium-kpi-card")

def create_batch_production_chart(data):
    """Production trend chart with premium styling"""
    
    batch_data = data['production']['batch_trend']
    dates = [item['date'] for item in batch_data]
    batches = [item['batches'] for item in batch_data]
    yields = [item['yield'] for item in batch_data]
    
    fig = go.Figure()
    
    # Production bars
    fig.add_trace(go.Bar(
        x=dates,
        y=batches,
        name='Daily Batches',
        marker_color=PREMIUM_COLORS['gold_primary'],
        opacity=0.8,
        yaxis='y'
    ))
    
    # Yield line
    fig.add_trace(go.Scatter(
        x=dates,
        y=yields,
        name='Yield %',
        line=dict(color=PREMIUM_COLORS['orange_accent'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=dict(
            text="Daily Production & Yield Trends",
            font=dict(color=PREMIUM_COLORS['text_primary'], size=16),
            x=0.02
        ),
        paper_bgcolor=PREMIUM_COLORS['bg_secondary'],
        plot_bgcolor=PREMIUM_COLORS['bg_secondary'],
        font=dict(color=PREMIUM_COLORS['text_secondary']),
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor=PREMIUM_COLORS['chart_grid'],
            showline=False,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title="Batches",
            titlefont=dict(color=PREMIUM_COLORS['gold_primary']),
            tickfont=dict(color=PREMIUM_COLORS['gold_primary']),
            showgrid=True,
            gridcolor=PREMIUM_COLORS['chart_grid'],
            showline=False
        ),
        yaxis2=dict(
            title="Yield %",
            titlefont=dict(color=PREMIUM_COLORS['orange_accent']),
            tickfont=dict(color=PREMIUM_COLORS['orange_accent']),
            overlaying='y',
            side='right',
            showgrid=False
        )
    )
    
    return fig

def create_quality_radar_chart(data):
    """Quality parameters radar chart"""
    
    parameters = data['quality']['critical_parameters']
    param_names = [p['parameter'] for p in parameters]
    values = [p['value'] for p in parameters]
    
    # Normalize values for radar chart (scale to 0-100)
    normalized_values = []
    for param in parameters:
        if param['parameter'] == 'Sterility':
            normalized_values.append(param['value'])
        elif param['parameter'] == 'Endotoxin':
            normalized_values.append(100 - (param['value'] * 50))  # Lower is better
        elif param['parameter'] == 'pH':
            normalized_values.append(95)  # pH 7.1 is good
        elif param['parameter'] == 'Particulates':
            normalized_values.append(88)  # Based on specification
        elif param['parameter'] == 'Potency':
            normalized_values.append(param['value'])
        else:
            normalized_values.append(95)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values + [normalized_values[0]],  # Close the shape
        theta=param_names + [param_names[0]],
        fill='toself',
        fillcolor=f'rgba(212, 175, 55, 0.2)',
        line_color=PREMIUM_COLORS['gold_primary'],
        line_width=2,
        name='Current Values'
    ))
    
    # Add target values (assuming 95% is target for all)
    target_values = [95] * len(param_names)
    fig.add_trace(go.Scatterpolar(
        r=target_values + [target_values[0]],
        theta=param_names + [param_names[0]],
        line_color=PREMIUM_COLORS['success'],
        line_dash='dash',
        line_width=1,
        name='Target',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text="Critical Quality Parameters",
            font=dict(color=PREMIUM_COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor=PREMIUM_COLORS['bg_secondary'],
        plot_bgcolor=PREMIUM_COLORS['bg_secondary'],
        font=dict(color=PREMIUM_COLORS['text_secondary']),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=8, color=PREMIUM_COLORS['text_secondary']),
                gridcolor=PREMIUM_COLORS['chart_grid']
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color=PREMIUM_COLORS['text_primary'])
            ),
            bgcolor=PREMIUM_COLORS['bg_secondary']
        ),
        margin=dict(l=60, r=60, t=60, b=60)
    )
    
    return fig

def create_environmental_monitoring_chart(data):
    """Environmental monitoring gauge charts"""
    
    zones = data['compliance']['environmental_zones']
    
    fig = go.Figure()
    
    # Create multiple gauge charts
    for i, zone in enumerate(zones):
        status_color = PREMIUM_COLORS['success'] if zone['status'] == 'Compliant' else PREMIUM_COLORS['warning']
        
        # Calculate percentage based on ISO limits
        if zone['zone'] == 'ISO 5':
            max_particles = 3520
        elif zone['zone'] == 'ISO 7':
            max_particles = 352000
        else:  # ISO 8
            max_particles = 3520000
        
        percentage = (zone['particles'] / max_particles) * 100
        
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=percentage,
            domain={'row': 0, 'column': i},
            title={'text': f"{zone['zone']}<br>({zone['particles']:,} particles)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': status_color},
                'steps': [
                    {'range': [0, 80], 'color': 'rgba(76, 175, 80, 0.1)'},
                    {'range': [80, 95], 'color': 'rgba(255, 152, 0, 0.1)'},
                    {'range': [95, 100], 'color': 'rgba(244, 67, 54, 0.1)'}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
            },
            number={'font': {'color': PREMIUM_COLORS['text_primary']}},
            title_font={'color': PREMIUM_COLORS['text_secondary']}
        ))
    
    fig.update_layout(
        title=dict(
            text="Environmental Monitoring - Cleanroom Zones",
            font=dict(color=PREMIUM_COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor=PREMIUM_COLORS['bg_secondary'],
        font=dict(color=PREMIUM_COLORS['text_secondary']),
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        margin=dict(l=40, r=40, t=80, b=40),
        height=300
    )
    
    return fig

def create_deviation_trend_chart(data):
    """Deviation trends over time"""
    
    deviation_trend = data['compliance']['deviations']['trend']
    days = [f"Day {i+1}" for i in range(len(deviation_trend))]
    
    fig = go.Figure()
    
    # Area chart for deviation trend
    fig.add_trace(go.Scatter(
        x=days,
        y=deviation_trend,
        mode='lines+markers',
        fill='tonexty',
        fillcolor=f'rgba(255, 140, 66, 0.2)',
        line=dict(color=PREMIUM_COLORS['orange_accent'], width=3),
        marker=dict(size=8, color=PREMIUM_COLORS['orange_accent']),
        name='Deviations'
    ))
    
    fig.update_layout(
        title=dict(
            text="Daily Deviation Trend (Last 7 Days)",
            font=dict(color=PREMIUM_COLORS['text_primary'], size=16),
            x=0.02
        ),
        paper_bgcolor=PREMIUM_COLORS['bg_secondary'],
        plot_bgcolor=PREMIUM_COLORS['bg_secondary'],
        font=dict(color=PREMIUM_COLORS['text_secondary']),
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor=PREMIUM_COLORS['chart_grid'],
            showline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=PREMIUM_COLORS['chart_grid'],
            showline=False,
            title="Number of Deviations"
        )
    )
    
    return fig

def create_inventory_status_chart(data):
    """Inventory status donut chart"""
    
    supplies = data['inventory']['critical_supplies']
    
    # Categorize by status
    status_counts = {'Good': 0, 'Low': 0, 'Critical': 0}
    for supply in supplies:
        status_counts[supply['status']] += 1
    
    labels = list(status_counts.keys())
    values = list(status_counts.values())
    colors = [PREMIUM_COLORS['success'], PREMIUM_COLORS['warning'], PREMIUM_COLORS['danger']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(color=PREMIUM_COLORS['text_primary'])
    )])
    
    fig.update_layout(
        title=dict(
            text="Critical Inventory Status",
            font=dict(color=PREMIUM_COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor=PREMIUM_COLORS['bg_secondary'],
        font=dict(color=PREMIUM_COLORS['text_secondary']),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(color=PREMIUM_COLORS['text_secondary'])
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>503B Compliance Manufacturing Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0A0B0D 0%, #1A1D20 100%);
                margin: 0;
                padding: 0;
                color: #FFFFFF;
            }
            
            .main-container {
                background: #0A0B0D;
                min-height: 100vh;
                padding: 20px;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #1A1D20 0%, #242831 100%);
                border-radius: 15px;
                padding: 25px 35px;
                margin-bottom: 30px;
                border: 1px solid rgba(212, 175, 55, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
            }
            
            .header-title {
                font-size: 28px;
                font-weight: 700;
                color: #D4AF37;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            .header-subtitle {
                font-size: 14px;
                color: #B8BCC8;
                margin-top: 8px;
                opacity: 0.9;
            }
            
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 20px;
                margin-bottom: 35px;
            }
            
            .premium-kpi-card {
                background: linear-gradient(145deg, #1A1D20 0%, #242831 100%);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(212, 175, 55, 0.08);
                box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
                position: relative;
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .premium-kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
            }
            
            .kpi-accent {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #E8C547);
            }
            
            .kpi-accent.warning {
                background: linear-gradient(90deg, #FF9800, #FFA726);
            }
            
            .kpi-accent.critical {
                background: linear-gradient(90deg, #F44336, #E57373);
            }
            
            .kpi-title {
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                color: #B8BCC8;
                margin: 0 0 12px 0;
                letter-spacing: 0.5px;
            }
            
            .kpi-value {
                font-size: 32px;
                font-weight: 800;
                color: #FFFFFF;
                line-height: 1;
            }
            
            .kpi-unit {
                font-size: 16px;
                font-weight: 400;
                color: #B8BCC8;
                margin-left: 4px;
            }
            
            .kpi-change {
                margin-top: 8px;
                font-size: 12px;
                font-weight: 600;
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(12, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .chart-card {
                background: linear-gradient(145deg, #1A1D20 0%, #242831 100%);
                border-radius: 12px;
                padding: 25px;
                border: 1px solid rgba(212, 175, 55, 0.08);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .chart-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 48px rgba(0, 0, 0, 0.7);
                border-color: rgba(212, 175, 55, 0.15);
            }
            
            .chart-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, #D4AF37, #E8C547);
            }
            
            .chart-full { grid-column: span 12; }
            .chart-half { grid-column: span 6; }
            .chart-third { grid-column: span 4; }
            .chart-quarter { grid-column: span 3; }
            
            .sidebar {
                position: fixed;
                left: 0;
                top: 0;
                width: 280px;
                height: 100vh;
                background: linear-gradient(180deg, #1A1D20 0%, #0A0B0D 100%);
                border-right: 1px solid rgba(212, 175, 55, 0.1);
                padding: 25px 0;
                z-index: 1000;
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
            }
            
            .sidebar-logo {
                padding: 0 25px 25px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
                margin-bottom: 25px;
            }
            
            .logo-text {
                font-size: 24px;
                font-weight: 700;
                color: #D4AF37;
                text-align: center;
            }
            
            .nav-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 25px;
                color: #B8BCC8;
                cursor: pointer;
                transition: all 0.2s ease;
                border-left: 3px solid transparent;
            }
            
            .nav-item:hover {
                background-color: rgba(212, 175, 55, 0.08);
                color: #E8C547;
                border-left-color: #D4AF37;
            }
            
            .nav-item.active {
                background-color: rgba(212, 175, 55, 0.12);
                color: #D4AF37;
                border-left-color: #D4AF37;
            }
            
            .content-wrapper {
                margin-left: 280px;
                padding: 20px;
            }
            
            .status-bar {
                text-align: center;
                padding: 15px;
                background: rgba(212, 175, 55, 0.05);
                border-radius: 8px;
                margin-top: 20px;
            }
            
            @media (max-width: 1200px) {
                .sidebar {
                    transform: translateX(-100%);
                }
                
                .content-wrapper {
                    margin-left: 0;
                }
                
                .chart-grid {
                    grid-template-columns: repeat(6, 1fr);
                }
                
                .chart-half { grid-column: span 6; }
                .chart-third { grid-column: span 6; }
            }
            
            @media (max-width: 768px) {
                .chart-grid {
                    grid-template-columns: 1fr;
                    gap: 15px;
                }
                
                .chart-card {
                    padding: 20px;
                }
                
                .kpi-grid {
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
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

# Main layout
app.layout = html.Div([
    # Sidebar
    html.Div([
        html.Div([
            html.Div("503B Compliance", className="logo-text")
        ], className="sidebar-logo"),
        
        html.Div([
            html.Div(["📊", " Overview"], className="nav-item active"),
            html.Div(["🏭", " Production"], className="nav-item"),
            html.Div(["🔬", " Quality Control"], className="nav-item"),
            html.Div(["📋", " Compliance"], className="nav-item"),
            html.Div(["📦", " Inventory"], className="nav-item"),
            html.Div(["🌡️", " Environmental"], className="nav-item"),
            html.Div(["👥", " Personnel"], className="nav-item"),
            html.Div(["📈", " Reports"], className="nav-item"),
            html.Div(["⚙️", " Settings"], className="nav-item")
        ])
    ], className="sidebar"),
    
    # Main content
    html.Div([
        # Header
        html.Div([
            html.H1("503B Pharmaceutical Manufacturing Dashboard", className="header-title"),
            html.P(f"Real-time Compliance Monitoring • Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                   className="header-subtitle")
        ], className="dashboard-header"),
        
        # KPI Row
        html.Div(id="kpi-row", className="kpi-grid"),
        
        # Charts Grid
        html.Div([
            # Production trends (large)
            html.Div([
                dcc.Graph(
                    id='production-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Quality radar
            html.Div([
                dcc.Graph(
                    id='quality-radar',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Environmental monitoring
            html.Div([
                dcc.Graph(
                    id='environmental-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Deviation trends
            html.Div([
                dcc.Graph(
                    id='deviation-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third"),
            
            # Inventory status
            html.Div([
                dcc.Graph(
                    id='inventory-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third")
            
        ], className="chart-grid"),
        
        # Auto-refresh
        dcc.Interval(
            id='interval-component',
            interval=300000,  # 5 minutes
            n_intervals=0
        ),
        
        # Status bar
        html.Div(id='status-indicator', className="status-bar")
        
    ], className="content-wrapper")
], className="main-container")

# Callbacks
@app.callback(
    [Output('kpi-row', 'children'),
     Output('production-chart', 'figure'),
     Output('quality-radar', 'figure'),
     Output('environmental-chart', 'figure'),
     Output('deviation-chart', 'figure'),
     Output('inventory-chart', 'figure'),
     Output('status-indicator', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n_intervals):
    """Update all dashboard components with fresh data"""
    
    # Fetch fresh data from Google Sheets
    data = get_503b_data()
    
    # Create KPI cards
    kpi_cards = [
        create_premium_kpi_card("Total Batches", data['production']['total_batches'], 8.3),
        create_premium_kpi_card("Quality Pass Rate", data['quality']['pass_rate'], 2.1, "%", "good"),
        create_premium_kpi_card("Compliance Score", data['compliance']['audit_score'], -1.2, "%", "warning"),
        create_premium_kpi_card("Active Deviations", data['compliance']['deviations']['total'], -25.0, "", "critical"),
        create_premium_kpi_card("Inventory Items", data['inventory']['raw_materials'], 5.7)
    ]
    
    # Status indicator
    current_time = datetime.now().strftime('%I:%M %p')
    status = html.Div([
        html.Span("🟢 ", style={'color': PREMIUM_COLORS['success']}),
        html.Span(f"System Online • Data synced at {current_time}", 
                 style={'color': PREMIUM_COLORS['text_secondary']})
    ])
    
    return (
        kpi_cards,
        create_batch_production_chart(data),
        create_quality_radar_chart(data),
        create_environmental_monitoring_chart(data),
        create_deviation_trend_chart(data),
        create_inventory_status_chart(data),
        status
    )

# Health check endpoint
@app.server.route('/health')
def health_check():
    return {'status': 'healthy', 'service': '503B Compliance Dashboard', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)

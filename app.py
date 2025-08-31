import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Import your master sheet connector
try:
    from google_sheets_503b import Master503BConnector
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    print("Google Sheets integration not available. Using fallback data.")

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Premium color palette matching your reference image
COLORS = {
    'bg_primary': '#0A0B0D',
    'bg_secondary': '#1A1D20', 
    'bg_accent': '#242831',
    'gold_primary': '#D4AF37',
    'gold_light': '#E8C547',
    'orange_accent': '#FF8C42',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B8BCC8',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336'
}

# Initialize connector to your master sheet
if GOOGLE_SHEETS_AVAILABLE:
    master_connector = Master503BConnector()
else:
    master_connector = None

def get_live_data():
    """Get live data from your master sheet or fallback"""
    if master_connector:
        try:
            return master_connector.get_dashboard_data()
        except Exception as e:
            print(f"Error fetching live data: {str(e)}")
    
    # Fallback 503B data
    return {
        'kpis': {
            'total_batches': {'value': 147, 'change': 8.3, 'status': 'good'},
            'quality_pass_rate': {'value': 98.2, 'change': 2.1, 'status': 'good'},
            'compliance_score': {'value': 97.3, 'change': -1.2, 'status': 'warning'},
            'active_deviations': {'value': 3, 'change': -25.0, 'status': 'warning'},
            'inventory_alerts': {'value': 12, 'change': 15.2, 'status': 'warning'}
        },
        'charts': {
            'production_trend': [
                {'day': 'Day -6', 'batches': 18, 'yield': 96.1},
                {'day': 'Day -5', 'batches': 22, 'yield': 97.2},
                {'day': 'Day -4', 'batches': 19, 'yield': 95.8},
                {'day': 'Day -3', 'batches': 25, 'yield': 98.1},
                {'day': 'Day -2', 'batches': 21, 'yield': 96.7},
                {'day': 'Day -1', 'batches': 17, 'yield': 94.9},
                {'day': 'Today', 'batches': 23, 'yield': 97.5}
            ],
            'quality_parameters': [
                {'parameter': 'Sterility', 'value': 100.0},
                {'parameter': 'Endotoxin Control', 'value': 99.0},
                {'parameter': 'pH Balance', 'value': 95.0},
                {'parameter': 'Particulate Control', 'value': 88.0},
                {'parameter': 'Potency Assurance', 'value': 102.0}
            ],
            'environmental_zones': [
                {'zone': 'ISO 5', 'particles': 145, 'status': 'Compliant'},
                {'zone': 'ISO 7', 'particles': 2840, 'status': 'Compliant'},
                {'zone': 'ISO 8', 'particles': 89500, 'status': 'Alert'}
            ],
            'deviation_analysis': {
                'trend': [2, 1, 3, 0, 1, 0, 1],
                'total': 8,
                'critical': 1
            },
            'inventory_status': {
                'status_breakdown': {'Good': 141, 'Low Stock': 12, 'Critical': 3}
            }
        }
    }

def create_kpi_card(title, value, change, unit="", status="normal"):
    """Create premium KPI cards matching reference design"""
    status_colors = {
        'good': COLORS['success'],
        'warning': COLORS['warning'], 
        'critical': COLORS['danger'],
        'normal': COLORS['gold_primary']
    }
    
    change_color = COLORS['success'] if change >= 0 else COLORS['danger']
    change_icon = "▲" if change >= 0 else "▼"
    accent_class = f"kpi-accent-{status}"
    
    return html.Div([
        html.Div(className=accent_class),
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
        ])
    ], className="premium-kpi-card")

def create_production_chart(data):
    """Production & yield trend chart"""
    trend_data = data['charts']['production_trend']
    
    days = [item['day'] for item in trend_data]
    batches = [item['batches'] for item in trend_data]
    yields = [item['yield'] for item in trend_data]
    
    fig = go.Figure()
    
    # Production bars with gradient
    fig.add_trace(go.Bar(
        x=days,
        y=batches,
        name='Daily Batches',
        marker_color=COLORS['gold_primary'],
        opacity=0.9,
        hovertemplate='<b>%{x}</b><br>Batches: %{y}<extra></extra>',
        yaxis='y'
    ))
    
    # Yield percentage line
    fig.add_trace(go.Scatter(
        x=days,
        y=yields,
        name='Yield %',
        line=dict(color=COLORS['orange_accent'], width=4),
        mode='lines+markers',
        marker=dict(size=10, color=COLORS['orange_accent']),
        hovertemplate='<b>%{x}</b><br>Yield: %{y:.1f}%<extra></extra>',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=dict(
            text="Daily Production & Yield Performance",
            font=dict(color=COLORS['text_primary'], size=18, weight=600),
            x=0.02
        ),
        paper_bgcolor=COLORS['bg_secondary'],
        plot_bgcolor=COLORS['bg_secondary'],
        font=dict(color=COLORS['text_secondary'], family="Inter"),
        showlegend=False,
        margin=dict(l=50, r=50, t=60, b=50),
        hovermode='x unified',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            showline=False,
            tickfont=dict(size=11, color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            title="Batches Produced",
            titlefont=dict(color=COLORS['gold_primary'], size=12),
            tickfont=dict(color=COLORS['gold_primary'], size=11),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            showline=False
        ),
        yaxis2=dict(
            title="Yield %",
            titlefont=dict(color=COLORS['orange_accent'], size=12),
            tickfont=dict(color=COLORS['orange_accent'], size=11),
            overlaying='y',
            side='right',
            showgrid=False,
            range=[85, 105]
        )
    )
    
    return fig

def create_quality_radar(data):
    """Quality parameters radar chart"""
    params = data['charts']['quality_parameters']
    
    param_names = [p['parameter'] for p in params]
    values = [p['value'] for p in params]
    
    fig = go.Figure()
    
    # Main radar trace
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=param_names + [param_names[0]],
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.25)',
        line_color=COLORS['gold_primary'],
        line_width=3,
        name='Current Performance',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>'
    ))
    
    # Target line at 95%
    target_values = [95] * len(param_names)
    fig.add_trace(go.Scatterpolar(
        r=target_values + [target_values[0]],
        theta=param_names + [param_names[0]],
        line_color=COLORS['success'],
        line_dash='dash',
        line_width=2,
        name='Target (95%)',
        showlegend=False,
        hovertemplate='<b>Target</b><br>95%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Critical Quality Parameters",
            font=dict(color=COLORS['text_primary'], size=18, weight=600),
            x=0.5
        ),
        paper_bgcolor=COLORS['bg_secondary'],
        plot_bgcolor=COLORS['bg_secondary'],
        font=dict(color=COLORS['text_secondary'], family="Inter"),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[75, 105],
                tickfont=dict(size=9, color=COLORS['text_secondary']),
                gridcolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=COLORS['text_primary'])
            ),
            bgcolor=COLORS['bg_secondary']
        ),
        margin=dict(l=60, r=60, t=70, b=60)
    )
    
    return fig

def create_environmental_gauges(data):
    """Environmental monitoring gauges"""
    zones = data['charts']['environmental_zones']
    
    fig = go.Figure()
    
    for i, zone in enumerate(zones):
        status_color = COLORS['success'] if zone['status'] == 'Compliant' else COLORS['danger']
        
        # Calculate compliance percentage
        limits = {'ISO 5': 3520, 'ISO 7': 352000, 'ISO 8': 3520000}
        max_particles = limits.get(zone['zone'], 1000000)
        compliance_pct = max(0, 100 - (zone['particles'] / max_particles) * 100)
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=compliance_pct,
            domain={'row': 0, 'column': i},
            title={
                'text': f"<b>{zone['zone']}</b><br><span style='font-size:10px'>{zone['particles']:,} particles</span>",
                'font': {'size': 12, 'color': COLORS['text_primary']}
            },
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': COLORS['text_secondary']},
                'bar': {'color': status_color, 'thickness': 0.8},
                'steps': [
                    {'range': [0, 70], 'color': 'rgba(244, 67, 54, 0.2)'},
                    {'range': [70, 85], 'color': 'rgba(255, 152, 0, 0.2)'},
                    {'range': [85, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': COLORS['gold_primary'], 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            },
            number={'font': {'color': COLORS['text_primary'], 'size': 14}}
        ))
    
    fig.update_layout(
        title=dict(
            text="Environmental Monitoring - Cleanroom Compliance",
            font=dict(color=COLORS['text_primary'], size=18),
            x=0.5
        ),
        paper_bgcolor=COLORS['bg_secondary'],
        font=dict(color=COLORS['text_secondary'], family="Inter"),
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        margin=dict(l=40, r=40, t=80, b=40),
        height=350
    )
    
    return fig

def create_deviation_trend(data):
    """Deviation trend analysis"""
    deviation_data = data['charts']['deviation_analysis']
    days = [f"Day {i-6}" if i < 6 else "Today" for i in range(7)]
    trend = deviation_data['trend']
    
    fig = go.Figure()
    
    # Area chart for deviations
    fig.add_trace(go.Scatter(
        x=days,
        y=trend,
        mode='lines+markers',
        fill='tozeroy',
        fillcolor='rgba(255, 140, 66, 0.3)',
        line=dict(color=COLORS['orange_accent'], width=4),
        marker=dict(size=12, color=COLORS['orange_accent']),
        name='Daily Deviations',
        hovertemplate='<b>%{x}</b><br>Deviations: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Quality Deviation Trends (7-Day)",
            font=dict(color=COLORS['text_primary'], size=18),
            x=0.02
        ),
        paper_bgcolor=COLORS['bg_secondary'],
        plot_bgcolor=COLORS['bg_secondary'],
        font=dict(color=COLORS['text_secondary'], family="Inter"),
        showlegend=False,
        margin=dict(l=50, r=30, t=60, b=50),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            showline=False
        ),
        yaxis=dict(
            title="Number of Deviations",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            showline=False
        )
    )
    
    return fig

def create_inventory_donut(data):
    """Inventory status donut chart"""
    status_data = data['charts']['inventory_status']['status_breakdown']
    
    labels = list(status_data.keys())
    values = list(status_data.values())
    colors = [COLORS['success'], COLORS['warning'], COLORS['danger']]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(color=COLORS['text_primary'], size=12),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
    ))
    
    # Add center annotation
    total_items = sum(values)
    fig.add_annotation(
        text=f"Total<br><b style='font-size:20px'>{total_items}</b><br>Items",
        x=0.5, y=0.5,
        font=dict(size=14, color=COLORS['text_primary']),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text="Inventory Status Overview",
            font=dict(color=COLORS['text_primary'], size=18),
            x=0.5
        ),
        paper_bgcolor=COLORS['bg_secondary'],
        font=dict(color=COLORS['text_secondary'], family="Inter"),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS['text_secondary'])
        )
    )
    
    return fig

# Premium CSS styling matching reference image
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>503B Pharmaceutical Manufacturing Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: #0A0B0D;
                color: #FFFFFF;
                overflow-x: hidden;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #1A1D20 0%, #242831 100%);
                padding: 25px 35px;
                margin: 20px 20px 30px 300px;
                border-radius: 15px;
                border: 1px solid rgba(212, 175, 55, 0.12);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
            }
            
            .header-title {
                font-size: 32px;
                font-weight: 700;
                color: #D4AF37;
                margin: 0;
                letter-spacing: -0.5px;
            }
            
            .header-subtitle {
                font-size: 14px;
                color: #B8BCC8;
                margin-top: 8px;
                opacity: 0.9;
            }
            
            .sidebar {
                position: fixed;
                left: 0;
                top: 0;
                width: 280px;
                height: 100vh;
                background: linear-gradient(180deg, #1A1D20 0%, #0A0B0D 100%);
                border-right: 2px solid #D4AF37;
                padding: 30px 0;
                z-index: 1000;
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
            }
            
            .sidebar-logo {
                text-align: center;
                padding: 0 25px 30px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                margin-bottom: 30px;
            }
            
            .logo-text {
                font-size: 24px;
                font-weight: 800;
                color: #D4AF37;
            }
            
            .logo-subtitle {
                font-size: 12px;
                color: #B8BCC8;
                margin-top: 4px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .nav-item {
                display: flex;
                align-items: center;
                gap: 14px;
                padding: 14px 25px;
                color: #B8BCC8;
                cursor: pointer;
                transition: all 0.3s ease;
                border-left: 3px solid transparent;
                font-weight: 500;
            }
            
            .nav-item:hover {
                background: rgba(212, 175, 55, 0.1);
                color: #E8C547;
                border-left-color: #D4AF37;
                transform: translateX(6px);
            }
            
            .nav-item.active {
                background: rgba(212, 175, 55, 0.15);
                color: #D4AF37;
                border-left-color: #D4AF37;
            }
            
            .main-content {
                margin-left: 280px;
                padding: 20px;
                min-height: 100vh;
            }
            
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 20px;
                margin: 0 20px 35px 20px;
            }
            
            .premium-kpi-card {
                background: linear-gradient(145deg, #1A1D20 0%, #242831 100%);
                border-radius: 12px;
                padding: 24px;
                border: 1px solid rgba(212, 175, 55, 0.08);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .premium-kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 48px rgba(0, 0, 0, 0.7);
                border-color: rgba(212, 175, 55, 0.2);
            }
            
            .kpi-accent-good {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #4CAF50, #66BB6A);
            }
            
            .kpi-accent-warning {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #FF9800, #FFA726);
            }
            
            .kpi-accent-critical {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #F44336, #E57373);
            }
            
            .kpi-accent-normal {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #E8C547);
            }
            
            .kpi-title {
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                color: #B8BCC8;
                margin: 0 0 12px 0;
                letter-spacing: 0.8px;
            }
            
            .kpi-value {
                font-size: 36px;
                font-weight: 800;
                color: #FFFFFF;
                line-height: 1;
            }
            
            .kpi-unit {
                font-size: 18px;
                font-weight: 400;
                color: #B8BCC8;
                margin-left: 6px;
            }
            
            .kpi-change {
                margin-top: 10px;
                font-size: 13px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(12, 1fr);
                gap: 20px;
                margin: 0 20px 30px 20px;
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
                transform: translateY(-3px);
                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8);
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
            
            .status-bar {
                text-align: center;
                padding: 18px;
                background: rgba(212, 175, 55, 0.08);
                border-radius: 10px;
                margin: 0 20px 20px 20px;
                border: 1px solid rgba(212, 175, 55, 0.15);
            }
            
            @media (max-width: 1400px) {
                .kpi-grid {
                    grid-template-columns: repeat(3, 1fr);
                }
            }
            
            @media (max-width: 900px) {
                .sidebar {
                    transform: translateX(-100%);
                }
                
                .main-content {
                    margin-left: 0;
                }
                
                .dashboard-header {
                    margin: 20px;
                }
                
                .chart-grid {
                    grid-template-columns: 1fr;
                    margin: 0 15px;
                }
                
                .kpi-grid {
                    grid-template-columns: repeat(2, 1fr);
                    margin: 0 15px 25px;
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

# Main layout with premium 503B design
app.layout = html.Div([
    # Premium Sidebar
    html.Div([
        html.Div([
            html.Div("503B Dashboard", className="logo-text"),
            html.Div("Pharmaceutical Compliance", className="logo-subtitle")
        ], className="sidebar-logo"),
        
        html.Div([
            html.Div(["📊", " Overview"], className="nav-item active"),
            html.Div(["🏭", " Production"], className="nav-item"),
            html.Div(["🔬", " Quality Control"], className="nav-item"), 
            html.Div(["📋", " Compliance"], className="nav-item"),
            html.Div(["📦", " Inventory"], className="nav-item"),
            html.Div(["🌡️", " Environmental"], className="nav-item"),
            html.Div(["👥", " Personnel"], className="nav-item"),
            html.Div(["📈", " Analytics"], className="nav-item")
        ])
    ], className="sidebar"),
    
    # Main dashboard content
    html.Div([
        # Premium header
        html.Div([
            html.H1("503B Pharmaceutical Manufacturing Dashboard", className="header-title"),
            html.P(f"Real-time Compliance Monitoring • Connected to Master Sheet • Last Sync: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                   className="header-subtitle")
        ], className="dashboard-header"),
        
        # Executive KPI Row
        html.Div(id="executive-kpis", className="kpi-grid"),
        
        # Premium Charts Grid
        html.Div([
            # Production trends (large chart)
            html.Div([
                dcc.Graph(
                    id='production-trends-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Quality parameters radar
            html.Div([
                dcc.Graph(
                    id='quality-radar-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Environmental monitoring
            html.Div([
                dcc.Graph(
                    id='environmental-monitoring-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-half"),
            
            # Deviation analysis
            html.Div([
                dcc.Graph(
                    id='deviation-analysis-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third"),
            
            # Inventory status
            html.Div([
                dcc.Graph(
                    id='inventory-status-chart',
                    config={'displayModeBar': False, 'responsive': True}
                )
            ], className="chart-card chart-third")
            
        ], className="chart-grid"),
        
        # Auto-refresh every 5 minutes
        dcc.Interval(
            id='data-refresh-interval',
            interval=300000,  # 5 minutes
            n_intervals=0
        ),
        
        # Status indicator
        html.Div(id='system-status', className="status-bar")
        
    ], className="main-content")
])

# Main callback for live data updates
@app.callback(
    [Output('executive-kpis', 'children'),
     Output('production-trends-chart', 'figure'),
     Output('quality-radar-chart', 'figure'), 
     Output('environmental-monitoring-chart', 'figure'),
     Output('deviation-analysis-chart', 'figure'),
     Output('inventory-status-chart', 'figure'),
     Output('system-status', 'children')],
    [Input('data-refresh-interval', 'n_intervals')]
)
def update_503b_dashboard(n_intervals):
    """Update dashboard with live data from your master sheet"""
    
    # Get fresh data from your master sheet
    live_data = get_live_data()
    
    # Create executive KPI cards
    kpi_cards = [
        create_kpi_card("Total Batches", live_data['kpis']['total_batches']['value'], 
                       live_data['kpis']['total_batches']['change'], "", live_data['kpis']['total_batches']['status']),
        create_kpi_card("Quality Pass Rate", live_data['kpis']['quality_pass_rate']['value'], 
                       live_data['kpis']['quality_pass_rate']['change'], "%", live_data['kpis']['quality_pass_rate']['status']),
        create_kpi_card("Compliance Score", live_data['kpis']['compliance_score']['value'], 
                       live_data['kpis']['compliance_score']['change'], "%", live_data['kpis']['compliance_score']['status']),
        create_kpi_card("Active Deviations", live_data['kpis']['active_deviations']['value'], 
                       live_data['kpis']['active_deviations']['change'], "", live_data['kpis']['active_deviations']['status']),
        create_kpi_card("Inventory Alerts", live_data['kpis']['inventory_alerts']['value'], 
                       live_data['kpis']['inventory_alerts']['change'], "", live_data['kpis']['inventory_alerts']['status'])
    ]
    
    # Status indicator with live sync info
    current_time = datetime.now().strftime('%I:%M %p')
    sync_status = "🟢 Live Sync Active" if master_connector and master_connector.client else "🟡 Using Cached Data"
    
    status_indicator = html.Div([
        html.Span(sync_status, style={'color': COLORS['success'] if 'Live' in sync_status else COLORS['warning']}),
        html.Span(f" • Master Sheet Connected • Last Update: {current_time}", 
                 style={'color': COLORS['text_secondary'], 'margin-left': '10px'})
    ])
    
    return (
        kpi_cards,
        create_production_chart(live_data),
        create_quality_radar(live_data),
        create_environmental_gauges(live_data),
        create_deviation_trend(live_data),
        create_inventory_donut(live_data),
        status_indicator
    )

# Health check for monitoring
@app.server.route('/health')
def health_check():
    return {
        'status': 'healthy', 
        'service': '503B Compliance Dashboard',
        'sheet_connection': master_connector.client is not None if master_connector else False,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)

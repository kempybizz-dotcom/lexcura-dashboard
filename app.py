import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import random
import math

# Initialize Dash app with meta tags
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')
server = app.server

# LexCura Premium Colors (matching reference image)
COLORS = {
    'bg_dark': '#0B0C0F',
    'card_bg': '#1A1D23',  
    'accent_gold': '#D4AF37',
    'accent_orange': '#FF8A42',
    'text_primary': '#FFFFFF',
    'text_secondary': '#8B9DC3',
    'success': '#4AE54A',
    'warning': '#FFB020', 
    'danger': '#FF4757',
    'grid': 'rgba(255,255,255,0.1)'
}

# Session state for login
logged_in_users = set()

def generate_realistic_data():
    """Generate realistic 503B pharmaceutical data"""
    return {
        'kpis': {
            'total_batches': 1025,
            'completion_rate': 96.8,
            'quality_score': 98.2,
            'deviation_count': 3,
            'compliance_rating': 97.5
        },
        'production_data': {
            'daily_batches': [18, 22, 19, 25, 21, 17, 23, 20, 24, 19, 26, 22],
            'yield_rates': [96.1, 97.2, 95.8, 98.1, 96.7, 94.9, 97.5, 95.3, 98.2, 96.8, 97.9, 96.4],
            'dates': [(datetime.now() - timedelta(days=11-i)).strftime('%m/%d') for i in range(12)]
        },
        'quality_data': {
            'sterility': 100.0,
            'endotoxin': 99.8,
            'potency': 102.1,
            'ph_balance': 96.5,
            'particulates': 94.2
        },
        'environmental': {
            'iso5_particles': 145,
            'iso7_particles': 2840,
            'iso8_particles': 89500,
            'temperature': 21.2,
            'humidity': 45.3
        },
        'inventory': {
            'total_items': 1247,
            'low_stock': 23,
            'expired': 5,
            'critical': 8
        }
    }

def create_login_page():
    """Create LexCura login page"""
    return html.Div([
        html.Div([
            html.Div([
                html.Img(src='/assets/lexcura_logo.png', style={
                    'height': '60px', 
                    'marginBottom': '30px'
                }),
                html.H2('LexCura 503B Dashboard', style={
                    'color': COLORS['accent_gold'],
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'fontFamily': 'Inter, sans-serif'
                }),
                html.P('Pharmaceutical Manufacturing Intelligence', style={
                    'color': COLORS['text_secondary'],
                    'textAlign': 'center',
                    'marginBottom': '40px',
                    'fontSize': '14px'
                }),
                
                dcc.Input(
                    id='login-username',
                    type='text',
                    placeholder='Username',
                    style={
                        'width': '100%',
                        'padding': '15px',
                        'marginBottom': '20px',
                        'border': f'1px solid {COLORS["text_secondary"]}',
                        'borderRadius': '8px',
                        'backgroundColor': 'transparent',
                        'color': COLORS['text_primary'],
                        'fontSize': '14px'
                    }
                ),
                
                dcc.Input(
                    id='login-password',
                    type='password',
                    placeholder='Password',
                    style={
                        'width': '100%',
                        'padding': '15px',
                        'marginBottom': '30px',
                        'border': f'1px solid {COLORS["text_secondary"]}',
                        'borderRadius': '8px',
                        'backgroundColor': 'transparent',
                        'color': COLORS['text_primary'],
                        'fontSize': '14px'
                    }
                ),
                
                html.Button('Sign In', id='login-button', n_clicks=0, style={
                    'width': '100%',
                    'padding': '15px',
                    'background': f'linear-gradient(135deg, {COLORS["accent_gold"]}, {COLORS["accent_orange"]})',
                    'border': 'none',
                    'borderRadius': '8px',
                    'color': '#000',
                    'fontWeight': '600',
                    'fontSize': '16px',
                    'cursor': 'pointer'
                }),
                
                html.Div(id='login-message', style={'marginTop': '20px', 'textAlign': 'center'})
                
            ], style={
                'background': f'linear-gradient(145deg, {COLORS["card_bg"]}, #252A35)',
                'padding': '50px',
                'borderRadius': '15px',
                'border': f'1px solid {COLORS["accent_gold"]}',
                'boxShadow': '0 20px 60px rgba(0,0,0,0.8)',
                'width': '400px',
                'textAlign': 'center'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'minHeight': '100vh',
            'background': f'linear-gradient(135deg, {COLORS["bg_dark"]}, #1A1D23)',
            'padding': '20px'
        })
    ])

def create_kpi_card(title, value, change, icon="📊"):
    """Create animated KPI cards"""
    change_color = COLORS['success'] if change >= 0 else COLORS['danger']
    change_icon = "↗" if change >= 0 else "↘"
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '24px', 'marginRight': '10px'}),
                html.H4(title, style={
                    'margin': '0',
                    'fontSize': '12px',
                    'textTransform': 'uppercase',
                    'color': COLORS['text_secondary'],
                    'letterSpacing': '0.5px'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '15px'}),
            
            html.Div(f"{value:,}", style={
                'fontSize': '36px',
                'fontWeight': '800',
                'color': COLORS['text_primary'],
                'marginBottom': '10px',
                'lineHeight': '1'
            }),
            
            html.Div([
                html.Span(change_icon, style={'color': change_color, 'marginRight': '5px'}),
                html.Span(f"{abs(change):.1f}%", style={'color': change_color, 'fontWeight': '600'})
            ], style={'fontSize': '14px'})
        ])
    ], className='kpi-card')

def create_production_chart():
    """Create production trend chart matching reference style"""
    data = generate_realistic_data()
    
    fig = go.Figure()
    
    # Production bars
    fig.add_trace(go.Bar(
        x=data['production_data']['dates'],
        y=data['production_data']['daily_batches'],
        name='Daily Production',
        marker_color=COLORS['accent_gold'],
        opacity=0.8,
        hovertemplate='<b>%{x}</b><br>Batches: %{y}<extra></extra>'
    ))
    
    # Yield line
    fig.add_trace(go.Scatter(
        x=data['production_data']['dates'],
        y=data['production_data']['yield_rates'],
        mode='lines+markers',
        name='Yield %',
        line=dict(color=COLORS['accent_orange'], width=3),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Yield: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Production Performance & Yield',
            font=dict(color=COLORS['text_primary'], size=16),
            x=0.02
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary']),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS['grid'],
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            title='Batches',
            showgrid=True,
            gridcolor=COLORS['grid'],
            zeroline=False
        ),
        yaxis2=dict(
            title='Yield %',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[90, 105]
        )
    )
    
    return fig

def create_quality_radar():
    """Create quality parameters radar chart"""
    data = generate_realistic_data()
    
    categories = ['Sterility', 'Endotoxin', 'Potency', 'pH Balance', 'Particulates']
    values = [data['quality_data'][key] for key in ['sterility', 'endotoxin', 'potency', 'ph_balance', 'particulates']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba(212, 175, 55, 0.3)',
        line_color=COLORS['accent_gold'],
        line_width=3,
        name='Current',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>'
    ))
    
    # Target line
    target = [95] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=target,
        theta=categories,
        line_color=COLORS['success'],
        line_dash='dash',
        line_width=2,
        name='Target',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text='Quality Control Parameters',
            font=dict(color=COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary']),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[80, 105],
                gridcolor=COLORS['grid'],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                gridcolor=COLORS['grid'],
                tickfont=dict(color=COLORS['text_primary'], size=12)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    return fig

def create_environmental_gauges():
    """Create environmental monitoring gauges"""
    data = generate_realistic_data()
    
    fig = go.Figure()
    
    zones = [
        {'name': 'ISO 5', 'particles': data['environmental']['iso5_particles'], 'limit': 3520},
        {'name': 'ISO 7', 'particles': data['environmental']['iso7_particles'], 'limit': 352000},
        {'name': 'ISO 8', 'particles': data['environmental']['iso8_particles'], 'limit': 3520000}
    ]
    
    for i, zone in enumerate(zones):
        compliance = max(0, 100 - (zone['particles'] / zone['limit']) * 100)
        color = COLORS['success'] if compliance > 85 else COLORS['warning'] if compliance > 70 else COLORS['danger']
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=compliance,
            domain={'row': 0, 'column': i},
            title={'text': f"<b>{zone['name']}</b><br>{zone['particles']:,} particles"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 70], 'color': 'rgba(255, 71, 87, 0.2)'},
                    {'range': [70, 85], 'color': 'rgba(255, 176, 32, 0.2)'},
                    {'range': [85, 100], 'color': 'rgba(74, 229, 74, 0.2)'}
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
    
    fig.update_layout(
        title=dict(
            text='Environmental Monitoring',
            font=dict(color=COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary']),
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        margin=dict(l=40, r=40, t=80, b=40),
        height=300
    )
    
    return fig

def create_deviation_trend():
    """Create deviation trend chart"""
    dates = [(datetime.now() - timedelta(days=6-i)).strftime('%m/%d') for i in range(7)]
    deviations = [2, 1, 3, 0, 1, 0, 1]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=deviations,
        mode='lines+markers',
        fill='tonexty',
        fillcolor=f'rgba(255, 138, 66, 0.3)',
        line=dict(color=COLORS['accent_orange'], width=3),
        marker=dict(size=10, color=COLORS['accent_orange']),
        name='Daily Deviations'
    ))
    
    fig.update_layout(
        title=dict(
            text='Quality Deviations (7-Day Trend)',
            font=dict(color=COLORS['text_primary'], size=16),
            x=0.02
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary']),
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
        yaxis=dict(showgrid=True, gridcolor=COLORS['grid'])
    )
    
    return fig

def create_inventory_donut():
    """Create inventory status donut chart"""
    data = generate_realistic_data()
    
    labels = ['Good Stock', 'Low Stock', 'Critical']
    values = [data['inventory']['total_items'] - data['inventory']['low_stock'] - data['inventory']['critical'],
              data['inventory']['low_stock'], data['inventory']['critical']]
    colors = [COLORS['success'], COLORS['warning'], COLORS['danger']]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(color=COLORS['text_primary'])
    ))
    
    fig.add_annotation(
        text=f"<b>{sum(values):,}</b><br>Total Items",
        x=0.5, y=0.5,
        font=dict(size=16, color=COLORS['text_primary']),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text='Inventory Status',
            font=dict(color=COLORS['text_primary'], size=16),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary']),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=40, r=40, t=60, b=60)
    )
    
    return fig

def create_dashboard():
    """Create main dashboard layout"""
    data = generate_realistic_data()
    
    return html.Div([
        # Animated background
        html.Div(className='animated-bg'),
        
        # Sidebar
        html.Div([
            html.Div([
                html.Img(src='/assets/lexcura_logo.png', style={'height': '40px', 'marginBottom': '10px'}),
                html.H3('LexCura', style={'color': COLORS['accent_gold'], 'margin': '0', 'fontFamily': 'Inter'}),
                html.P('503B Dashboard', style={'color': COLORS['text_secondary'], 'fontSize': '12px', 'margin': '5px 0 0 0'})
            ], style={'textAlign': 'center', 'padding': '20px', 'borderBottom': f'1px solid {COLORS["grid"]}', 'marginBottom': '20px'}),
            
            html.Div([
                html.Div(['📊', ' Overview'], className='nav-item active'),
                html.Div(['🏭', ' Production'], className='nav-item'),
                html.Div(['🔬', ' Quality Control'], className='nav-item'),
                html.Div(['📋', ' Compliance'], className='nav-item'),
                html.Div(['📦', ' Inventory'], className='nav-item'),
                html.Div(['🌡️', ' Environmental'], className='nav-item'),
                html.Div(['📈', ' Analytics'], className='nav-item'),
                html.Div(['⚙️', ' Settings'], className='nav-item'),
                html.Div(['🚪', ' Logout'], id='logout-btn', className='nav-item')
            ])
        ], className='sidebar'),
        
        # Main content
        html.Div([
            # Header
            html.Div([
                html.Div([
                    html.H1('LexCura 503B Manufacturing Intelligence', style={
                        'color': COLORS['accent_gold'],
                        'margin': '0',
                        'fontSize': '28px',
                        'fontFamily': 'Inter'
                    }),
                    html.P(f'Real-time Compliance Monitoring • Last Updated: {datetime.now().strftime("%I:%M %p")}', style={
                        'color': COLORS['text_secondary'],
                        'margin': '8px 0 0 0',
                        'fontSize': '14px'
                    })
                ]),
                html.Div([
                    html.Button('Export Report', className='header-btn'),
                    html.Button('Settings', className='header-btn')
                ], style={'display': 'flex', 'gap': '10px'})
            ], className='header'),
            
            # KPI Cards
            html.Div([
                create_kpi_card('Total Batches', data['kpis']['total_batches'], 8.3, '🏭'),
                create_kpi_card('Quality Score', data['kpis']['quality_score'], 2.1, '🔬'),
                create_kpi_card('Completion Rate', data['kpis']['completion_rate'], -1.2, '✅'),
                create_kpi_card('Active Deviations', data['kpis']['deviation_count'], -25.0, '⚠️'),
                create_kpi_card('Compliance Rating', data['kpis']['compliance_rating'], 5.7, '📋')
            ], className='kpi-grid'),
            
            # Charts Grid
            html.Div([
                html.Div([dcc.Graph(figure=create_production_chart(), config={'displayModeBar': False})], className='chart-card chart-large'),
                html.Div([dcc.Graph(figure=create_quality_radar(), config={'displayModeBar': False})], className='chart-card chart-medium'),
                html.Div([dcc.Graph(figure=create_environmental_gauges(), config={'displayModeBar': False})], className='chart-card chart-large'),
                html.Div([dcc.Graph(figure=create_deviation_trend(), config={'displayModeBar': False})], className='chart-card chart-small'),
                html.Div([dcc.Graph(figure=create_inventory_donut(), config={'displayModeBar': False})], className='chart-card chart-small'),
            ], className='charts-grid'),
            
            # Status bar
            html.Div([
                html.Span('🟢 ', style={'color': COLORS['success']}),
                html.Span('System Operational • All systems nominal • Data refreshed automatically')
            ], className='status-bar')
            
        ], className='main-content'),
        
        # Auto refresh
        dcc.Interval(id='refresh-interval', interval=30000, n_intervals=0)
        
    ], id='dashboard-container')

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>LexCura 503B Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', sans-serif;
                background: #0B0C0F;
                color: #FFFFFF;
                overflow-x: hidden;
            }
            
            .animated-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at 20% 80%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
                           radial-gradient(circle at 80% 20%, rgba(255, 138, 66, 0.02) 0%, transparent 50%);
                z-index: -1;
                animation: pulse 20s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 0.8; transform: scale(1); }
                50% { opacity: 1; transform: scale(1.05); }
            }
            
            .sidebar {
                position: fixed;
                left: 0;
                top: 0;
                width: 280px;
                height: 100vh;
                background: linear-gradient(180deg, #1A1D23 0%, #0B0C0F 100%);
                border-right: 2px solid #D4AF37;
                z-index: 1000;
                box-shadow: 4px 0 20px rgba(0,0,0,0.5);
            }
            
            .nav-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 15px 25px;
                color: #8B9DC3;
                cursor: pointer;
                transition: all 0.3s ease;
                border-left: 3px solid transparent;
                font-weight: 500;
            }
            
            .nav-item:hover {
                background: rgba(212, 175, 55, 0.1);
                color: #D4AF37;
                border-left-color: #D4AF37;
                transform: translateX(5px);
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
            
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: linear-gradient(135deg, #1A1D23 0%, #252A35 100%);
                padding: 25px 35px;
                border-radius: 12px;
                border: 1px solid #D4AF37;
                margin-bottom: 30px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            }
            
            .header-btn {
                padding: 10px 20px;
                background: linear-gradient(135deg, #D4AF37, #FF8A42);
                border: none;
                border-radius: 6px;
                color: #000;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            
            .header-btn:hover {
                transform: translateY(-2px);
            }
            
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .kpi-card {
                background: linear-gradient(145deg, #1A1D23 0%, #252A35 100%);
                padding: 25px;
                border-radius: 12px;
                border: 1px solid rgba(212, 175, 55, 0.2);
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .kpi-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            }
            
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #D4AF37, #FF8A42);
            }
            
            .charts-grid {
                display: grid;
                grid-template-columns: repeat(12, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .chart-card {
                background: linear-gradient(145deg, #1A1D23 0%, #252A35 100%);
                border-radius: 12px;
                padding: 25px;
                border: 1px solid rgba(212, 175, 55, 0.2);
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
                transition: all 0.3s ease;
            }
            
            .chart-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 30px rgba(0,0,0,0.6);
            }
            
            .chart-large { grid-column: span 6; }
            .chart-medium { grid-column: span 6; }
            .chart-small { grid-column: span 4; }
            
            .status-bar {
                text-align: center;
                padding: 15px;
                background: rgba(212, 175, 55, 0.1);
                border-radius: 8px;
                color: #8B9DC3;
            }
            
            @media (max-width: 1200px) {
                .kpi-grid { grid-template-columns: repeat(3, 1fr); }
                .chart-large, .chart-medium { grid-column: span 12; }
                .chart-small { grid-column: span 6; }
            }
            
            @media (max-width: 768px) {
                .sidebar { transform: translateX(-100%); }
                .main-content { margin-left: 0; }
                .kpi-grid { grid-template-columns: repeat(2, 1fr); }
                .charts-grid { grid-template-columns: 1fr; }
                .chart-card { grid-column: span 1; }
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

# Layout with session management
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', data={'logged_in': False}),
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    [Output('page-content', 'children'),
     Output('session-store', 'data')],
    [Input('url', 'pathname'),
     Input('login-button', 'n_clicks'),
     Input('logout-btn', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State('session-store', 'data')]
)
def display_page(pathname, login_clicks, logout_clicks, username, password, session_data):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return create_login_page(), {'logged_in': False}
    
    trigger = ctx.triggered[0]['prop_id']
    
    if trigger == 'login-button.n_clicks' and login_clicks:
        # Simple auth - replace with real authentication
        if username == 'lexcura' and password == 'admin123':
            return create_dashboard(), {'logged_in': True}
        else:
            return create_login_page(), {'logged_in': False}
    
    elif trigger == 'logout-btn.n_clicks' and logout_clicks:
        return create_login_page(), {'logged_in': False}
    
    elif session_data.get('logged_in'):
        return create_dashboard(), session_data
    else:
        return create_login_page(), {'logged_in': False}

@app.callback(
    Output('login-message', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value')]
)
def update_login_message(n_clicks, username, password):
    if n_clicks and username and password:
        if username != 'lexcura' or password != 'admin123':
            return html.Div('Invalid credentials. Try: lexcura / admin123', 
                           style={'color': COLORS['danger'], 'fontSize': '14px'})
    return ""

# Health check endpoint
@app.server.route('/health')
def health_check():
    return {
        'status': 'healthy', 
        'service': 'LexCura 503B Dashboard',
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)

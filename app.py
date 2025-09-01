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

def get_sidebar():
    return html.Div([
        html.Div([
            html.Img(src="/assets/lexcura_logo.png", style={'width': '40px', 'height': 'auto', 'margin-right': '15px'}),
            html.Span("LexCura Dashboard", style={'font-size': '22px', 'font-weight': '700'})
        ], className="logo", style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        
        html.Div([
            html.Div("📊 Overview", id="nav-overview", className="nav-item", n_clicks=0),
            html.Div("📈 Analytics", id="nav-analytics", className="nav-item", n_clicks=0),
            html.Div("📄 Reports", id="nav-reports", className="nav-item", n_clicks=0),
            html.Div("🎯 Google Slides", id="nav-slides", className="nav-item", n_clicks=0),
            html.Div("📚 Archive", id="nav-archive", className="nav-item", n_clicks=0),
            html.Div("⚙️ Settings", id="nav-settings", className="nav-item", n_clicks=0),
            html.Hr(style={'border-color': COLORS['gold_primary'], 'margin': '25px 0'}),
            html.Div("🚪 Logout", id="logout-btn", className="nav-item", n_clicks=0,
                    style={'color': COLORS['danger_red']})
        ])
    ], className="sidebar")

def get_header(title):
    return html.Div([
        html.H1(title, style={'margin-bottom': '10px'}),
        html.P(f"Last Updated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", 
               style={'margin': '0', 'font-size': '14px', 'opacity': '0.8'})
    ], className="header")

def get_dashboard_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("LexCura Executive Business Intelligence Dashboard"),
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.ButtonGroup([
                                    dbc.Button("📄 Export PDF", id="export-pdf-btn", color="warning",
                                              style={'background-color': COLORS['gold_primary'], 'border-color': COLORS['gold_primary']}),
                                    dbc.Button("🔄 Refresh Data", id="refresh-data-btn", color="secondary"),
                                    dbc.Button("🔍 Full Screen", id="fullscreen-btn", color="info")
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
                ], style={'background-color': COLORS['dark_grey'], 'border': f'1px solid {COLORS["gold_primary"]}', 'margin-bottom': '20px'}),
                
                html.Div([
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='financial-impact-chart',
                                figure=create_financial_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='deadline-tracker-chart',
                                figure=create_deadline_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='alert-severity-chart',
                                figure=create_alert_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='historical-trends-chart',
                                figure=create_historical_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='growth-decline-chart',
                                figure=create_growth_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='performance-comparison-chart',
                                figure=create_performance_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='risk-compliance-gauge',
                                figure=create_risk_gauge(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(
                                id='projection-forecast-chart',
                                figure=create_projection_chart(),
                                config={'displayModeBar': False, 'responsive': True},
                                style={'height': '450px'}
                            )
                        ], color=COLORS['gold_primary'], type="dot")
                    ], className="card"),
                    
                ], className="chart-grid"),
                
            ], id="dashboard-content"),
            
            dcc.Interval(
                id='auto-refresh-interval',
                interval=300000,
                n_intervals=0
            ),
            
            dcc.Download(id="download-pdf")
            
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

def get_archive_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Document Archive - Historical Reports"),
            dbc.Container([
                html.H3("📚 Google Slides Archive", style={'color': COLORS['gold_primary']}),
                html.P("Access historical presentation reports", style={'color': COLORS['neutral_text']}),
                html.Hr(style={'border-color': COLORS['gold_primary']}),
                html.P("Archive system coming soon...", style={'color': COLORS['neutral_text']})
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

def get_google_slides_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Live Google Slides Integration"),
            dbc.Container([
                html.H3("🎯 Current Presentation", style={'color': COLORS['gold_primary']}),
                html.P("Interactive view of latest presentation", style={'color': COLORS['neutral_text']}),
                html.Hr(style={'border-color': COLORS['gold_primary']}),
                html.Div([
                    html.Iframe(
                        src="https://docs.google.com/presentation/d/e/2PACX-1vSampleID/embed?start=false&loop=false&delayms=3000",
                        style={
                            'width': '100%',
                            'height': '600px',
                            'border': f'3px solid {COLORS["gold_primary"]}',
                            'border-radius': '10px'
                        }
                    )
                ])
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

def get_settings_layout():
    return html.Div([
        get_sidebar(),
        html.Div([
            get_header("Dashboard Settings & Configuration"),
            dbc.Container([
                html.H3("⚙️ Settings Panel", style={'color': COLORS['gold_primary']}),
                html.P("Configure dashboard preferences", style={'color': COLORS['neutral_text']}),
                html.Hr(style={'border-color': COLORS['gold_primary']}),
                html.P("Settings panel coming soon...", style={'color': COLORS['neutral_text']})
            ], fluid=True)
        ], className="main-content", style={'margin-left': '280px', 'padding': '20px'})
    ])

# Enhanced CSS with animations
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
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: #0F1113;
                color: #B8B9BB;
                overflow-x: hidden;
            }
            
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
            
            @keyframes loadingBar {
                from {
                    transform: scaleX(0);
                }
                to {
                    transform: scaleX(1);
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
                animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) both;
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
            }
            
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
                animation: fadeInUp 0.6s ease-out both;
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
            
            .card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
                border-color: #D4AF37;
            }
            
            .card:hover::before {
                transform: scaleX(1);
            }
            
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
                gap: 25px;
                margin-top: 25px;
            }
            
            ._dash-loading {
                color: #D4AF37 !important;
            }
            
            .btn {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 600;
                border-radius: 10px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            }
            
            @media (max-width: 1200px) {
                .chart-grid {
                    grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
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
                }
                
                .header h1 {
                    font-size: 28px;
                }
            }
            
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0F1113;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #D4AF37, #FFCF66);
                border-radius: 5px;
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
    [Input('url', 'pathname'),
     Input('intro-timer', 'n_intervals')],
    [State('session-store', 'data'),
     State('show-intro', 'data')]
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
    elif pathname == '/analytics':
        return get_dashboard_layout()
    elif pathname == '/reports':
        return get_dashboard_layout()
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
    
    navigation_map = {
        'nav-overview': "/",
        'nav-analytics': "/analytics", 
        'nav-reports': "/reports",
        'nav-slides': "/slides",
        'nav-archive': "/archive",
        'nav-settings': "/settings"
    }
    
    return navigation_map.get(button_id, "/")

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

# PDF Export callback (simplified version without reportlab for now)
@app.callback(
    Output("download-pdf", "data"),
    Input("export-pdf-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_pdf_report(n_clicks):
    if n_clicks:
        try:
            # Create a simple text report for now
            report_content = f"""
LexCura Executive Dashboard Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Financial Summary:
- Current Revenue: ${data['financial']['current'][0]:,.0f}
- Risk Score: {data['risk_score']}/100
- Total Alerts: {sum(data['alerts']['count'])}

This is a simplified export. Full PDF generation with charts coming soon.
            """
            
            return dict(content=report_content, filename=f"LexCura_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
        except Exception as e:
            print(f"Error exporting report: {str(e)}")
    return None

# Health check endpoint
@app.server.route('/health')
def health_check():
    return {
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'features': ['authentication', 'charts', 'export', 'navigation']
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        debug=False,
        host='0.0.0.0',
        port=port,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )import dash
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

# Enhanced data generation
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
            'tasks': ['Q4 Financial Audit', 'Cloud Migration', 'Compliance Review', 'Budget 2025', 'Security Upgrade', 'Client Onboarding', 'Legal Documentation'],
            'days_left': [2, 18, 1, 15, 25, 8, 12],
            'progress': [92, 35, 98, 55, 20, 75, 60],
            'priority': ['Critical', 'High', 'Critical', 'Medium', 'Low', 'High', 'Medium']
        }
        deadline_data['urgency'] = ['Critical' if d <= 3 else 'Warning' if d <= 7 else 'Normal' for d in deadline_data['days_left']]
        
        # Alert data
        alert_data = {
            'severity': ['Critical', 'High', 'Medium', 'Low', 'Info'],
            'count': [5, 12, 18, 25, 40],
            'categories': ['Security', 'Performance', 'Compliance', 'System', 'User']
        }
        
        # Historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        historical_dates = []
        current_date = start_date
        while current_date <= end_date:
            historical_dates.append(current_date)
            current_date += timedelta(days=1)
        
        historical_data = {
            'dates': historical_dates,
            'revenue_performance': [],
            'operational_efficiency': [],
            'client_satisfaction': [],
            'targets': {'revenue': 1200, 'efficiency': 85, 'satisfaction': 90}
        }
        
        base_values = {'revenue': 1000, 'efficiency': 75, 'satisfaction': 80}
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
        
        # Growth data
        growth_data = {
            'quarters': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024 (Proj)'],
            'revenue_growth': [15, 22, 18, 28],
            'market_expansion': [8, 12, 15, 20],
            'client_acquisition': [25, 18, 30, 35],
            'operational_decline': [5, 3, 2, 1]
        }
        
        # Performance KPIs
        performance_data = {
            'kpis': ['Legal Efficiency', 'Client Satisfaction', 'Response Time', 'Cost Optimization', 'Revenue Growth', 'Market Position'],
            'current_score': [88, 94, 82, 91, 85, 78],
            'target_score': [92, 96, 88, 95, 90, 85],
            'industry_avg': [75, 87, 78, 83, 80, 72],
            'last_quarter': [85, 91, 79, 88, 82, 75]
        }
        
        risk_score = random.randint(45, 75)
        
        # Projection data
        future_dates = []
        current_month = datetime.now().replace(day=1)
        for i in range(18):
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
            forecast = base_forecast * (1 + growth_rate) ** i
            projection_data['revenue_forecast'].append(forecast)
            projection_data['conservative_forecast'].append(base_forecast * (1 + growth_rate * 0.7) ** i)
            projection_data['optimistic_forecast'].append(base_forecast * (1 + growth_rate * 1.3) ** i)
            projection_data['lower_confidence'].append(forecast * 0.85)
            projection_data['upper_confidence'].append(forecast * 1.15)
        
        # Archive data
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
        'transition': {'duration': 800, 'easing': 'cubic-in-out'},
        'hovermode': 'x unified'
    }

# Chart creation functions
def create_financial_chart():
    try:
        fig = go.Figure()
        
        colors_current = []
        for i, x in enumerate(data['financial']['current']):
            if x > 0:
                colors_current.append(f'rgba(61, 188, 107, {0.8 + i*0.05})')
            else:
                colors_current.append(f'rgba(228, 87, 76, {0.8 + i*0.05})')
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['current'],
            name='Current Period',
            marker_color=colors_current,
            marker_line=dict(width=2, color=COLORS['gold_primary']),
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<br><extra></extra>',
            text=[f"${x:,.0f}" for x in data['financial']['current']],
            textposition='outside',
            textfont={'size': 12, 'color': COLORS['neutral_text']}
        ))
        
        fig.add_trace(go.Bar(
            x=data['financial']['categories'],
            y=data['financial']['previous'],
            name='Previous Period',
            marker_color=COLORS['gold_primary'],
            marker_line=dict(width=1, color=COLORS['highlight_gold']),
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Previous: $%{y:,.0f}<br><extra></extra>'
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
        
        fig.add_trace(go.Bar(
            y=data['deadlines']['tasks'],
            x=data['deadlines']['days_left'],
            orientation='h',
            marker_color=colors,
            marker_line=dict(width=1, color='white'),
            hovertemplate='<b>%{y}</b><br>Days Left: %{x}<br>Progress: %{customdata}%<br><extra></extra>',
            customdata=data['deadlines']['progress'],
            name='Days Remaining'
        ))
        
        layout = get_animated_layout('Project Timeline & Progress Tracker')
        layout['xaxis']['title'] = 'Days Remaining'
        layout['height'] = 500
        
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
        
        fig.add_trace(go.Pie(
            labels=data['alerts']['severity'],
            values=data['alerts']['count'],
            hole=0.65,
            marker_colors=severity_colors,
            marker_line=dict(color='white', width=3),
            hovertemplate='<b>%{label} Priority</b><br>Count: %{value}<br>Percentage: %{percent}<br><extra></extra>',
            textinfo='label+percent',
            textfont={'color': 'white', 'size': 11, 'family': 'Inter'},
            textposition='inside'
        ))
        
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
        
        fig.add_trace(go.Scatter(
            x=data['historical']['dates'],
            y=data['historical']['operational_efficiency'],
            mode='lines',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'},
            name='Operational Efficiency (%)',
            yaxis='y2',
            hovertemplate='<b>Efficiency</b><br>Date: %{x}<br>Value: %{y:.1f}%<br><extra></extra>'
        ))
        
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
            title='Efficiency (%)',
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
        
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['revenue_growth'],
            name='Revenue Growth',
            marker_color=COLORS['success_green'],
            hovertemplate='<b>%{x}</b><br>Revenue Growth: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['revenue_growth']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=data['growth']['quarters'],
            y=data['growth']['market_expansion'],
            name='Market Expansion',
            marker_color=COLORS['gold_primary'],
            hovertemplate='<b>%{x}</b><br>Market Expansion: +%{y}%<extra></extra>',
            text=[f"+{rate}%" for rate in data['growth']['market_expansion']],
            textposition='outside'
        ))
        
        layout = get_animated_layout('Quarterly Growth Analysis')
        layout['yaxis']['title'] = 'Growth Rate (%)'
        layout['yaxis']['ticksuffix'] = '%'
        layout['xaxis']['title'] = 'Quarter'
        layout['barmode'] = 'group'
        
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
        
        fig.add_trace(go.Scatterpolar(
            r=data['performance']['target_score'],
            theta=data['performance']['kpis'],
            mode='lines+markers',
            name='Target Goals',
            line={'color': COLORS['success_green'], 'width': 2, 'dash': 'dot'},
            marker={'size': 6, 'symbol': 'diamond'},
            hovertemplate='<b>%{theta}</b><br>Target: %{r}%<br><extra></extra>'
        ))
        
        layout = get_animated_layout('Performance KPIs vs Benchmarks')
        layout['polar'] = {
            'bgcolor': COLORS['dark_grey'],
            'radialaxis': {
                'visible': True,
                'range': [0, 100],
                'color': COLORS['neutral_text'],
                'ticksuffix': '%'
            },
            'angularaxis': {
                'color': COLORS['neutral_text']
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
        
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['upper_confidence'],
            mode='lines',
            line={'width': 0},
            showlegend=False,
            hoverinfo='skip',
            name='Upper Confidence'
        ))
        
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['lower_confidence'],
            mode='lines',
            line={'width': 0},
            fill='tonexty',
            fillcolor='rgba(212, 175, 55, 0.15)',
            name='Confidence Range',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Range: $%{y:,.0f}<br><extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=data['projections']['dates'],
            y=data['projections']['revenue_forecast'],
            mode='lines+markers',
            line={'color': COLORS['gold_primary'], 'width': 4},
            marker={'size': 8, 'color': COLORS['highlight_gold']},
            name='Base Forecast',
            hovertemplate='<b>%{x|%Y-%m}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
        ))
        
        layout = get_animated_layout('18-Month Revenue Projection')
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
                    'transform':

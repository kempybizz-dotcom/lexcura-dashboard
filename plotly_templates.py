# UI-REFACTOR-GOLD-2025: Elite Plotly theme for Fortune-500 dashboards
import plotly.io as pio
import plotly.graph_objects as go

def register_gold_dark_template():
    """Register the elite gold dark theme for all charts"""
    
    gold_dark_template = go.layout.Template(
        layout=go.Layout(
            # Core background colors
            paper_bgcolor="#0F1113",
            plot_bgcolor="#1B1D1F",
            
            # Typography
            font=dict(
                family="Inter, Roboto, system-ui",
                color="#F5F6F7",
                size=13
            ),
            
            # Color palette for data series
            colorway=["#D4AF37", "#FFCF66", "#B8B9BB", "#3DBC6B", "#E4574C"],
            
            # Axes styling
            xaxis=dict(
                color="#B8B9BB",
                gridcolor="rgba(255,255,255,0.04)",
                zeroline=False,
                showline=False,
                tickfont=dict(color="#B8B9BB", size=12)
            ),
            yaxis=dict(
                color="#B8B9BB",
                gridcolor="rgba(255,255,255,0.04)",
                zeroline=False,
                showline=False,
                tickfont=dict(color="#B8B9BB", size=12)
            ),
            
            # Hover styling
            hoverlabel=dict(
                bgcolor="#121314",
                bordercolor="rgba(255,255,255,0.06)",
                font=dict(color="#F5F6F7", size=12)
            ),
            hovermode="x unified",
            
            # Layout margins
            margin=dict(l=40, r=20, t=40, b=40),
            
            # Title styling
            title=dict(
                font=dict(color="#D4AF37", size=18, family="Inter"),
                x=0.5,
                xanchor="center"
            ),
            
            # Legend styling
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(255,255,255,0.06)",
                borderwidth=1,
                font=dict(color="#B8B9BB")
            )
        )
    )
    
    # Register template
    pio.templates["gold_dark"] = gold_dark_template
    pio.templates.default = "gold_dark"

def styled_plotly_chart(fig, height=400, use_modebar=False):
    """Apply consistent styling to any Plotly figure"""
    
    # Ensure template is applied
    fig.update_layout(template="gold_dark")
    
    # Override specific layout properties for consistency
    fig.update_layout(
        height=height,
        paper_bgcolor="#0F1113",
        plot_bgcolor="#1B1D1F",
        font=dict(family="Inter, Roboto, system-ui", color="#F5F6F7"),
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode="x unified" if fig.layout.hovermode is None else fig.layout.hovermode
    )
    
    # Style axes consistently
    fig.update_xaxes(
        color="#B8B9BB",
        gridcolor="rgba(255,255,255,0.04)",
        zeroline=False,
        showline=False
    )
    fig.update_yaxes(
        color="#B8B9BB", 
        gridcolor="rgba(255,255,255,0.04)",
        zeroline=False,
        showline=False
    )
    
    return fig

# Initialize the template when module is imported
register_gold_dark_template()

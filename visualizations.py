import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Define premium dark theme colors
BACKGROUND_COLOR = 'rgba(0,0,0,0)'
TEXT_COLOR = '#e0e0e0'
GRID_COLOR = 'rgba(255,255,255,0.1)'
PRIMARY_COLOR = '#00f3ff'
SECONDARY_COLOR = '#b026ff'
COLOR_SEQ = [PRIMARY_COLOR, SECONDARY_COLOR, '#00ffd1', '#ff0095', '#0077ff']

def update_layout(fig):
    """Applies premium glassmorphism dark theme to a plotly figure."""
    fig.update_layout(
        plot_bgcolor=BACKGROUND_COLOR,
        paper_bgcolor=BACKGROUND_COLOR,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, gridwidth=1, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, gridwidth=1, zeroline=False),
        margin=dict(l=20, r=20, t=40, b=20),
        title_font=dict(size=18, family="Poppins, sans-serif", color=PRIMARY_COLOR),
        legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1)
    )
    return fig

def plot_missing_heatmap(df):
    """Creates a heatmap of missing values."""
    missing_matrix = df.isnull().astype(int)
    fig = px.imshow(
        missing_matrix, 
        color_continuous_scale=[[0, BACKGROUND_COLOR], [1, SECONDARY_COLOR]],
        zmin=0, zmax=1,
        aspect="auto",
        title="Missing Values Heatmap"
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(xaxis_title="Columns", yaxis_title="Rows", yaxis_showticklabels=False)
    return update_layout(fig)

def plot_datatype_pie(df):
    """Creates a pie chart showing proportion of datatypes."""
    dtypes_counts = df.dtypes.astype(str).value_counts().reset_index()
    dtypes_counts.columns = ['Data Type', 'Count']
    fig = px.pie(
        dtypes_counts, 
        names='Data Type', 
        values='Count', 
        title="Column Data Types",
        color_discrete_sequence=COLOR_SEQ,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#050505', width=2)))
    return update_layout(fig)

def plot_null_percentage(df):
    """Creates a bar chart of null percentages per column."""
    null_percentages = (df.isnull().sum() / len(df)) * 100
    null_percentages = null_percentages[null_percentages > 0].sort_values(ascending=False).reset_index()
    if null_percentages.empty:
        # Return empty plot with a message
        fig = go.Figure()
        fig.add_annotation(text="No Null Values Found", x=0.5, y=0.5, showarrow=False, font=dict(size=20, color=PRIMARY_COLOR))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(title="Null Value Percentages")
        return update_layout(fig)
        
    null_percentages.columns = ['Column', 'Missing Percentage']
    fig = px.bar(
        null_percentages, 
        x='Column', 
        y='Missing Percentage',
        title="Null Percentage by Column",
        color='Missing Percentage',
        color_continuous_scale=[[0, PRIMARY_COLOR], [1, '#ff0095']]
    )
    return update_layout(fig)

def plot_correlation_matrix(df):
    """Creates a correlation matrix for numeric columns."""
    num_df = df.select_dtypes(include=['number'])
    if num_df.empty or len(num_df.columns) < 2:
        fig = go.Figure()
        fig.add_annotation(text="Not enough numeric columns for correlation", x=0.5, y=0.5, showarrow=False, font=dict(size=16, color=SECONDARY_COLOR))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(title="Correlation Matrix")
        return update_layout(fig)

    corr = num_df.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix",
        color_continuous_scale="Viridis"
    )
    return update_layout(fig)

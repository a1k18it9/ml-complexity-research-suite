"""Visualization utilities."""

from typing import Any, Dict, List, Optional
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


class Plotter:
    """Unified plotting interface."""
    
    THEME = {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e",
        "success": "#2ca02c",
        "danger": "#d62728",
        "warning": "#ffbb78",
        "info": "#17becf",
    }
    
    def __init__(self):
        sns.set_palette("husl")
    
    def line_plot(
        self,
        x: np.ndarray,
        y: np.ndarray,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        labels: Optional[List[str]] = None,
    ) -> go.Figure:
        """Create interactive line plot."""
        fig = go.Figure()
        
        if y.ndim == 1:
            y = y.reshape(1, -1)
            labels = labels or ["Series 1"]
        
        for i, (series, label) in enumerate(zip(y, labels or [f"Series {i+1}" for i in range(len(y))])):
            fig.add_trace(go.Scatter(x=x, y=series, mode='lines+markers', name=label))
        
        fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, template="plotly_white")
        return fig
    
    def bar_plot(
        self,
        categories: List[str],
        values: List[float],
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
    ) -> go.Figure:
        """Create bar plot."""
        fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=self.THEME["primary"])])
        fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, template="plotly_white")
        return fig
    
    def heatmap(
        self,
        data: np.ndarray,
        title: str = "",
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
    ) -> go.Figure:
        """Create heatmap."""
        fig = go.Figure(data=go.Heatmap(z=data, x=xticklabels, y=yticklabels, colorscale='Viridis'))
        fig.update_layout(title=title, template="plotly_white")
        return fig
    
    def scatter_plot(
        self,
        x: np.ndarray,
        y: np.ndarray,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        color: Optional[np.ndarray] = None,
    ) -> go.Figure:
        """Create scatter plot."""
        fig = go.Figure(data=go.Scatter(
            x=x, y=y, mode='markers',
            marker=dict(size=8, color=color, colorscale='Viridis', showscale=color is not None),
        ))
        fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, template="plotly_white")
        return fig


def create_comparison_plot(
    results: Dict[str, List[float]],
    x_values: List[float],
    title: str = "Algorithm Comparison",
    xlabel: str = "Input Size",
    ylabel: str = "Time (s)",
) -> go.Figure:
    """Create comparison plot for multiple algorithms."""
    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    for i, (name, values) in enumerate(results.items()):
        fig.add_trace(go.Scatter(
            x=x_values, y=values, mode='lines+markers', name=name,
            line=dict(color=colors[i % len(colors)], width=2),
        ))
    
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, template="plotly_white")
    return fig

"""
Interactive plots using Plotly for SPC analysis
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional


class SPCPlotter:
    """Create interactive SPC control charts"""
    
    @staticmethod
    def plot_individuals_chart(
        data: np.ndarray,
        control_limits: dict,
        title: str = "Gráfico de Individuos (I-MR)",
    ) -> go.Figure:
        """Plot individuals control chart"""
        fig = go.Figure()
        
        # Add data points
        fig.add_trace(
            go.Scatter(
                y=data,
                mode="lines+markers",
                name="Observaciones",
                line=dict(color="blue", width=2),
                marker=dict(size=6),
            )
        )
        
        # Add center line
        center = control_limits.get("center", np.mean(data))
        fig.add_hline(
            y=center,
            line_dash="dash",
            line_color="green",
            name="Línea Central",
            annotation_text="Centro",
        )
        
        # Add control limits
        ucl = control_limits.get("ucl", center + 3 * np.std(data))
        lcl = control_limits.get("lcl", center - 3 * np.std(data))
        
        fig.add_hline(
            y=ucl,
            line_dash="dash",
            line_color="red",
            name="LCS",
            annotation_text="LCS",
        )
        fig.add_hline(
            y=lcl,
            line_dash="dash",
            line_color="red",
            name="LCI",
            annotation_text="LCI",
        )
        
        # Highlight out-of-control points
        out_of_control = (data > ucl) | (data < lcl)
        if out_of_control.any():
            indices = np.where(out_of_control)[0]
            fig.add_trace(
                go.Scatter(
                    x=indices,
                    y=data[indices],
                    mode="markers",
                    marker=dict(size=10, color="red", symbol="x"),
                    name="Fuera de Control",
                )
            )
        
        fig.update_layout(
            title=title,
            xaxis_title="Número de Muestra",
            yaxis_title="Valor",
            hovermode="x unified",
            height=500,
            template="plotly_white",
        )
        
        return fig
    
    @staticmethod
    def plot_xbar_r_chart(
        data: np.ndarray,
        subgroup_size: int,
        control_limits: dict,
    ) -> go.Figure:
        """Plot Xbar-R control chart with two subplots"""
        n_subgroups = len(data) // subgroup_size
        reshaped = data[: n_subgroups * subgroup_size].reshape(-1, subgroup_size)
        
        xbar_vals = np.mean(reshaped, axis=1)
        r_vals = np.max(reshaped, axis=1) - np.min(reshaped, axis=1)
        
        xbar_lcl = control_limits["xbar"]["lcl"]
        xbar_center = control_limits["xbar"]["center"]
        xbar_ucl = control_limits["xbar"]["ucl"]
        
        r_lcl = control_limits["r"]["lcl"]
        r_center = control_limits["r"]["center"]
        r_ucl = control_limits["r"]["ucl"]
        
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("Gráfico Xbar", "Gráfico R"),
            shared_xaxes=True,
            vertical_spacing=0.12,
        )
        
        # Xbar chart
        fig.add_trace(
            go.Scatter(
                y=xbar_vals,
                mode="lines+markers",
                name="Medias",
                line=dict(color="blue", width=2),
                marker=dict(size=6),
            ),
            row=1,
            col=1,
        )
        
        fig.add_hline(
            y=xbar_center,
            line_dash="dash",
            line_color="green",
            row=1,
            col=1,
        )
        
        fig.add_hline(y=xbar_ucl, line_dash="dash", line_color="red", row=1, col=1)
        fig.add_hline(y=xbar_lcl, line_dash="dash", line_color="red", row=1, col=1)
        
        # R chart
        fig.add_trace(
            go.Scatter(
                y=r_vals,
                mode="lines+markers",
                name="Rangos",
                line=dict(color="purple", width=2),
                marker=dict(size=6),
            ),
            row=2,
            col=1,
        )
        
        fig.add_hline(
            y=r_center,
            line_dash="dash",
            line_color="green",
            row=2,
            col=1,
        )
        
        fig.add_hline(y=r_ucl, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=r_lcl, line_dash="dash", line_color="red", row=2, col=1)
        
        fig.update_yaxes(title_text="Medias", row=1, col=1)
        fig.update_yaxes(title_text="Rangos", row=2, col=1)
        fig.update_xaxes(title_text="Número de Subgrupo", row=2, col=1)
        
        fig.update_layout(
            title_text="Gráfico Xbar-R de Control",
            height=700,
            template="plotly_white",
            hovermode="x unified",
        )
        
        return fig
    
    @staticmethod
    def plot_power_curve(
        delta_range: np.ndarray,
        power_values: np.ndarray,
        current_delta: float = None,
    ) -> go.Figure:
        """Plot power curve vs shift size"""
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=delta_range,
                y=power_values,
                mode="lines+markers",
                name="Potencia",
                line=dict(color="blue", width=2),
                marker=dict(size=6),
            )
        )
        
        # Add reference line at 80% power
        fig.add_hline(
            y=0.8,
            line_dash="dot",
            line_color="gray",
            annotation_text="80% potencia",
        )
        
        if current_delta is not None:
            # Add vertical line at current delta
            idx = np.argmin(np.abs(delta_range - current_delta))
            current_power = power_values[idx]
            
            fig.add_vline(
                x=current_delta,
                line_dash="dash",
                line_color="red",
                annotation_text=f"δ={current_delta:.2f}<br>Potencia={current_power:.1%}",
            )
        
        fig.update_layout(
            title="Curva de Potencia vs Corrimiento (δ)",
            xaxis_title="Corrimiento (en sigmas)",
            yaxis_title="Potencia (1-β)",
            hovermode="x unified",
            height=500,
            template="plotly_white",
            yaxis=dict(range=[0, 1.05]),
        )
        
        return fig
    
    @staticmethod
    def plot_arl_curve(
        delta_range: np.ndarray,
        arl1_values: np.ndarray,
        arl0: float,
    ) -> go.Figure:
        """Plot ARL₁ vs shift size"""
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=delta_range,
                y=arl1_values,
                mode="lines+markers",
                name="ARL₁ (con cambio)",
                line=dict(color="purple", width=2),
                marker=dict(size=6),
            )
        )
        
        # Add ARL0 reference line
        fig.add_hline(
            y=arl0,
            line_dash="dash",
            line_color="green",
            annotation_text=f"ARL₀ = {arl0:.1f}",
        )
        
        fig.update_layout(
            title="Longitud Promedio de Secuencia (ARL)",
            xaxis_title="Corrimiento (en sigmas)",
            yaxis_title="ARL₁ (muestras)",
            hovermode="x unified",
            height=500,
            template="plotly_white",
        )
        
        return fig
    
    @staticmethod
    def plot_histogram_with_normal(
        data: np.ndarray,
        mean: float,
        std_dev: float,
        lsl: Optional[float] = None,
        usl: Optional[float] = None,
    ) -> go.Figure:
        """Plot histogram with normal distribution overlay"""
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(
            go.Histogram(
                x=data,
                name="Datos",
                nbinsx=20,
                opacity=0.7,
                marker_color="lightblue",
            )
        )
        
        # Normal distribution curve
        x_range = np.linspace(data.min() - 3 * std_dev, data.max() + 3 * std_dev, 200)
        from scipy.stats import norm
        
        y_normal = norm.pdf(x_range, loc=mean, scale=std_dev)
        # Scale to match histogram
        y_normal = y_normal * len(data) * (data.max() - data.min()) / 20
        
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_normal,
                mode="lines",
                name="Normal Teórica",
                line=dict(color="red", width=2),
            )
        )
        
        # Add spec limits if provided
        if lsl is not None:
            fig.add_vline(
                x=lsl,
                line_dash="dash",
                line_color="blue",
                annotation_text="LIE",
            )
        
        if usl is not None:
            fig.add_vline(
                x=usl,
                line_dash="dash",
                line_color="blue",
                annotation_text="LSE",
            )
        
        fig.update_layout(
            title="Distribución de Datos vs Normal Teórica",
            xaxis_title="Valor",
            yaxis_title="Frecuencia",
            height=500,
            template="plotly_white",
            hovermode="x unified",
        )
        
        return fig

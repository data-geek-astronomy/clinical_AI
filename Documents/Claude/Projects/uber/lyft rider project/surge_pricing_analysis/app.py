"""
Gradio dashboard for Surge Pricing Impact Analysis.
Causal inference analysis of marketplace dynamics.
"""

import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from src.data_simulator import MarketplaceSimulator
from src.causal_inference import (
    PropensityScoreMatching,
    SyntheticControlMethod,
    InterruptedTimeSeries,
    compare_causal_methods
)


def generate_analysis(days, surge_mult, surge_freq, demand_elast, supply_elast, seed):
    """Generate marketplace data and run causal analysis."""
    try:
        # Generate data
        sim = MarketplaceSimulator(seed=seed)
        surge_days = list(np.random.RandomState(seed).choice(
            days, size=max(1, int(days * surge_freq)), replace=False
        ))

        df = sim.generate_daily_data(
            days=days,
            surge_multiplier=surge_mult,
            surge_days=surge_days,
            demand_elasticity=demand_elast,
            supply_elasticity=supply_elast
        )

        # Summary stats
        surge_group = df[df['is_surge'] == 1]
        no_surge_group = df[df['is_surge'] == 0]

        summary = f"""
        **Simulation Summary**

        Total Days: {len(df)}
        Surge Days: {len(surge_group)} ({len(surge_group)/len(df)*100:.1f}%)

        **Completion Rate**
        - Surge Days: {surge_group['completion_rate'].mean():.2%}
        - No Surge Days: {no_surge_group['completion_rate'].mean():.2%}
        - Difference: {(surge_group['completion_rate'].mean() - no_surge_group['completion_rate'].mean()):.2%}

        **Wait Time (minutes)**
        - Surge Days: {surge_group['wait_time_minutes'].mean():.1f}
        - No Surge Days: {no_surge_group['wait_time_minutes'].mean():.1f}
        - Difference: {(surge_group['wait_time_minutes'].mean() - no_surge_group['wait_time_minutes'].mean()):.1f}

        **Driver Earnings ($)**
        - Surge Days: ${surge_group['driver_earnings'].mean():.2f}
        - No Surge Days: ${no_surge_group['driver_earnings'].mean():.2f}
        - Difference: ${(surge_group['driver_earnings'].mean() - no_surge_group['driver_earnings'].mean()):.2f}
        """

        # Time series plot
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df['date'],
            y=df['completion_rate'],
            name='Completion Rate',
            mode='lines',
            line=dict(color='#4ECDC4', width=2)
        ))

        surge_periods = df[df['is_surge'] == 1]
        fig_ts.add_trace(go.Scatter(
            x=surge_periods['date'],
            y=surge_periods['completion_rate'],
            mode='markers',
            name='Surge Period',
            marker=dict(size=8, color='#FF6B6B')
        ))

        fig_ts.update_layout(
            title='Completion Rate Over Time',
            xaxis_title='Date',
            yaxis_title='Completion Rate',
            hovermode='x unified',
            height=400
        )

        # Causal analysis
        results = compare_causal_methods(df, outcome_col='completion_rate')

        causal_text = "**Causal Inference Results (Completion Rate)**\n\n"
        for method, result in results.items():
            if 'error' in result:
                causal_text += f"- **{method}:** Error - {result['error']}\n"
            elif 'ate' in result:
                ate = result['ate']
                ci_lower = result.get('ci_lower', 0)
                ci_upper = result.get('ci_upper', 0)
                causal_text += f"- **{method}:** {ate:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}])\n"
            elif 'level_change' in result:
                causal_text += f"- **{method}:** Level Change = {result['level_change']:.4f}\n"

        return summary, fig_ts, causal_text

    except Exception as e:
        return f"Error: {str(e)}", None, f"Error in causal analysis: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="Surge Pricing Impact Analysis") as demo:
    gr.Markdown("""
    # 🚗 Surge Pricing Impact Analysis

    **How does surge pricing truly affect rider demand, driver supply, and market equilibrium?**

    This interactive dashboard applies causal inference to isolate the real incremental impact of surge pricing—moving beyond correlation to causation.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Simulation Parameters")

            days = gr.Slider(
                label="Simulation Duration (days)",
                minimum=30,
                maximum=180,
                value=90,
                step=10
            )

            surge_multiplier = gr.Slider(
                label="Surge Multiplier (fare multiplier)",
                minimum=1.2,
                maximum=3.0,
                value=2.5,
                step=0.1
            )

            surge_frequency = gr.Slider(
                label="Surge Frequency (%)",
                minimum=5,
                maximum=50,
                value=15,
                step=5
            )

            demand_elasticity = gr.Slider(
                label="Demand Elasticity",
                minimum=-1.0,
                maximum=-0.1,
                value=-0.5,
                step=0.1
            )

            supply_elasticity = gr.Slider(
                label="Supply Elasticity",
                minimum=0.2,
                maximum=1.5,
                value=0.65,
                step=0.1
            )

            random_seed = gr.Number(
                label="Random Seed",
                value=42,
                precision=0
            )

            analyze_btn = gr.Button("Analyze", scale=2)

        with gr.Column(scale=2):
            summary_output = gr.Textbox(
                label="Summary Statistics",
                lines=15,
                interactive=False
            )

    with gr.Row():
        timeseries_plot = gr.Plot(label="Time Series: Completion Rate")

    with gr.Row():
        causal_output = gr.Textbox(
            label="Causal Inference Results",
            lines=10,
            interactive=False
        )

    # Connect button
    analyze_btn.click(
        fn=generate_analysis,
        inputs=[days, surge_multiplier, surge_frequency, demand_elasticity, supply_elasticity, random_seed],
        outputs=[summary_output, timeseries_plot, causal_output]
    )

    gr.Markdown("""
    ---

    ## Methodology

    **Propensity Score Matching (PSM):** Matches surge days to no-surge days based on observable confounders.

    **Synthetic Control Method:** Builds a synthetic "no surge" counterfactual using pre-treatment periods.

    **Interrupted Time Series (ITS):** Estimates level and slope changes at the intervention point.

    [GitHub Repository](https://github.com/data-geek-astronomy/surge_pricing_analysis)
    """)


if __name__ == "__main__":
    demo.launch()

import gradio as gr
import pandas as pd
import numpy as np

def analyze_surge(days, surge_mult, surge_freq):
    """Simple surge pricing analysis."""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=days, freq='D')
    
    base_demand = np.random.normal(500, 50, days)
    base_supply = np.random.normal(300, 30, days)
    
    surge_days = np.random.choice(days, int(days * surge_freq), replace=False)
    surge_multiplier = np.ones(days)
    surge_multiplier[surge_days] = surge_mult
    
    demand = base_demand * (1 - (surge_mult - 1) * 0.3)
    supply = base_supply * (1 + (surge_mult - 1) * 0.5)
    
    completion_rate = np.minimum(supply / demand, 1.0)
    wait_time = 10 * (1 - completion_rate)
    
    summary = f"""**Surge Pricing Analysis**

Days: {days}
Surge Events: {len(surge_days)} ({len(surge_days)/days*100:.1f}%)
Multiplier: {surge_mult}x

**Completion Rate**
Overall: {completion_rate.mean():.2%}
Surge Days: {completion_rate[surge_days].mean():.2%}
Normal Days: {completion_rate[~np.isin(range(days), surge_days)].mean():.2%}

**Wait Time (minutes)**
Overall: {wait_time.mean():.1f}
Surge Days: {wait_time[surge_days].mean():.1f}
Normal Days: {wait_time[~np.isin(range(days), surge_days)].mean():.1f}"""
    
    return summary

with gr.Blocks(title="Surge Pricing Analysis") as demo:
    gr.Markdown("# 🚗 Surge Pricing Impact Analysis")
    
    with gr.Row():
        days = gr.Slider(30, 180, 90, step=10, label="Days")
        surge_mult = gr.Slider(1.2, 3.0, 2.5, step=0.1, label="Multiplier")
        surge_freq = gr.Slider(0.05, 0.5, 0.15, step=0.05, label="Frequency")
    
    output = gr.Textbox(label="Results", lines=12)
    analyze_btn = gr.Button("Analyze")
    analyze_btn.click(analyze_surge, [days, surge_mult, surge_freq], output)

if __name__ == "__main__":
    demo.launch()

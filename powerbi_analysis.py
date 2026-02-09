"""
Power BI Style Revenue Analytics Dashboard
Blueprint Technologies Business Operations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Load data
df = pd.read_csv('data/revenue_opportunities.csv')
df['Created_Date'] = pd.to_datetime(df['Created_Date'])

# Create dashboard
fig = plt.figure(figsize=(18, 10))
fig.suptitle('Revenue Operations Dashboard - Cybersecurity SME Segment\nQ1-Q4 2024 Performance', 
             fontsize=16, fontweight='bold')

# 1. Revenue by Region (KPI Card style)
ax1 = plt.subplot(2, 3, 1)
region_revenue = df.groupby('Region')['Actual_Revenue'].sum().sort_values(ascending=True)
colors = ['#4472C4' if x > region_revenue.mean() else '#ED7D31' for x in region_revenue]
bars = ax1.barh(region_revenue.index, region_revenue.values/1e6, color=colors)
ax1.set_xlabel('Revenue ($ Millions)')
ax1.set_title('Revenue by Region', fontweight='bold')
for i, v in enumerate(region_revenue.values):
    ax1.text(v/1e6 + 0.1, i, f'${v/1e6:.1f}M', va='center', fontweight='bold')

# 2. Sales Pipeline Funnel
ax2 = plt.subplot(2, 3, 2)
stage_data = df.groupby('Sales_Stage')['Deal_Size'].sum()
stage_order = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
stage_values = [stage_data.get(s, 0) for s in stage_order]
colors2 = ['#70AD47' if s == 'Closed Won' else '#C00000' if s == 'Closed Lost' else '#4472C4' 
           for s in stage_order]
ax2.bar(range(len(stage_order)), [v/1e6 for v in stage_values], color=colors2)
ax2.set_xticks(range(len(stage_order)))
ax2.set_xticklabels(stage_order, rotation=45, ha='right')
ax2.set_ylabel('Pipeline ($ Millions)')
ax2.set_title('Sales Pipeline by Stage', fontweight='bold')

# 3. Monthly Trend (Line chart)
ax3 = plt.subplot(2, 3, 3)
monthly = df.groupby(df['Created_Date'].dt.month).agg({
    'Actual_Revenue': 'sum',
    'Expected_Revenue': 'sum'
})
ax3.plot(monthly.index, monthly['Actual_Revenue']/1e6, marker='o', label='Actual Revenue', linewidth=2)
ax3.plot(monthly.index, monthly['Expected_Revenue']/1e6, marker='s', label='Expected Revenue', 
         linewidth=2, linestyle='--')
ax3.set_xlabel('Month')
ax3.set_ylabel('Revenue ($ Millions)')
ax3.set_title('Monthly Revenue Trend', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Channel Performance
ax4 = plt.subplot(2, 3, 4)
channel_perf = df.groupby('Channel').agg({
    'Actual_Revenue': 'sum',
    'Opportunity_ID': 'count'
})
channel_perf['Avg_Deal_Size'] = channel_perf['Actual_Revenue'] / channel_perf['Opportunity_ID']
ax4.scatter(channel_perf['Opportunity_ID'], channel_perf['Actual_Revenue']/1e6, 
           s=channel_perf['Avg_Deal_Size']/100, alpha=0.6, c='#4472C4')
for i, txt in enumerate(channel_perf.index):
    ax4.annotate(txt, (channel_perf['Opportunity_ID'].iloc[i], 
                      channel_perf['Actual_Revenue'].iloc[i]/1e6), fontsize=8)
ax4.set_xlabel('Number of Deals')
ax4.set_ylabel('Total Revenue ($ Millions)')
ax4.set_title('Channel Performance Matrix', fontweight='bold')

# 5. Product Mix
ax5 = plt.subplot(2, 3, 5)
product_revenue = df.groupby('Product')['Actual_Revenue'].sum().sort_values(ascending=True)
ax5.barh(product_revenue.index, product_revenue.values/1e6, color='#ED7D31')
ax5.set_xlabel('Revenue ($ Millions)')
ax5.set_title('Revenue by Product Line', fontweight='bold')

# 6. Marketing Program ROI
ax6 = plt.subplot(2, 3, 6)
program_roi = df.groupby('Marketing_Program')['Actual_Revenue'].sum().sort_values(ascending=False)
colors6 = ['#70AD47', '#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#C00000']
ax6.bar(range(len(program_roi)), program_roi.values/1e6, color=colors6[:len(program_roi)])
ax6.set_xticks(range(len(program_roi)))
ax6.set_xticklabels(program_roi.index, rotation=45, ha='right')
ax6.set_ylabel('Attributed Revenue ($ Millions)')
ax6.set_title('Marketing Program Performance', fontweight='bold')

plt.tight_layout()
plt.savefig('assets/revenue_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Dashboard saved: assets/revenue_dashboard.png")
plt.show()

# Executive Summary
print("\n" + "="*60)
print("EXECUTIVE SUMMARY - REVENUE OPERATIONS")
print("="*60)
print(f"Total Pipeline Value: ${df['Deal_Size'].sum():,.2f}")
print(f"Closed Won Revenue: ${df[df['Sales_Stage']=='Closed Won']['Actual_Revenue'].sum():,.2f}")
print(f"Win Rate: {(df['Sales_Stage']=='Closed Won').mean()*100:.1f}%")
print(f"Average Deal Size: ${df['Deal_Size'].mean():,.2f}")
print(f"Top Region: {region_revenue.idxmax()} (${region_revenue.max():,.2f})")
print(f"Top Channel: {df.groupby('Channel')['Actual_Revenue'].sum().idxmax()}")

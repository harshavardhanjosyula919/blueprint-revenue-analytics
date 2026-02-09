"""
Blueprint Technologies - Revenue Operations Analytics
Cybersecurity SME and Channel Segment Business Data
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

def generate_revenue_data():
    """Generate multi-source revenue and program data"""
    print("Generating Blueprint revenue operations data...")
    
    n_opportunities = 5000
    n_programs = 1200
    start_date = datetime(2024, 1, 1)
    
    # Regions (global business)
    regions = ['North America', 'EMEA', 'APAC', 'Latin America']
    
    # Product lines (cybersecurity focused)
    products = ['Endpoint Security', 'Cloud Security', 'Network Security', 
                'Identity Management', 'Threat Intelligence', 'Security Consulting']
    
    # Channels
    channels = ['Direct Sales', 'VAR Partner', 'MSP Partner', 'Distributor', 'Online']
    
    # Sales stages
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    
    data = []
    
    # Generate opportunities
    for i in range(n_opportunities):
        created_date = start_date + timedelta(days=random.randint(0, 364))
        close_date = created_date + timedelta(days=random.randint(30, 180))
        
        region = random.choice(regions)
        product = random.choice(products)
        channel = random.choice(channels)
        stage = random.choices(stages, weights=[15, 20, 25, 20, 15, 5])[0]
        
        # Revenue calculations
        deal_size = np.random.lognormal(10, 1.5)  # Skewed distribution
        if stage == 'Closed Won':
            actual_revenue = deal_size
            probability = 100
        elif stage == 'Closed Lost':
            actual_revenue = 0
            probability = 0
        else:
            probability = {'Prospecting': 20, 'Qualification': 40, 
                          'Proposal': 60, 'Negotiation': 80}[stage]
            actual_revenue = deal_size * (probability / 100)
        
        # Marketing program influence
        program_influence = random.choice(['Email Campaign', 'Webinar', 'Trade Show', 
                                         'Partner Referral', 'Direct', 'Content Download'])
        
        data.append({
            'Opportunity_ID': f"OPP_{i:05d}",
            'Created_Date': created_date.strftime('%Y-%m-%d'),
            'Close_Date': close_date.strftime('%Y-%m-%d'),
            'Region': region,
            'Product': product,
            'Channel': channel,
            'Sales_Stage': stage,
            'Deal_Size': round(deal_size, 2),
            'Probability': probability,
            'Expected_Revenue': round(deal_size * (probability/100), 2),
            'Actual_Revenue': round(actual_revenue, 2),
            'Marketing_Program': program_influence,
            'Quarter': (created_date.month - 1) // 3 + 1,
            'Month': created_date.month
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/revenue_opportunities.csv', index=False)
    
    print(f"✓ Generated {len(df)} opportunities")
    print(f"✓ Total Pipeline: ${df['Deal_Size'].sum():,.2f}")
    print(f"✓ Expected Revenue: ${df['Expected_Revenue'].sum():,.2f}")
    print(f"✓ Actual Revenue: ${df['Actual_Revenue'].sum():,.2f}")
    return df

if __name__ == "__main__":
    generate_revenue_data()

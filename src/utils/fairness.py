import pandas as pd
import numpy as np
import streamlit as st

<<<<<<< HEAD

def generate_fairness_report(df: pd.DataFrame) -> dict:
    """
    Analyzes resource allocation equity across three dimensions:
    - Geographic Coverage: spread of resources across lat/lon quadrants
    - Urgency Distribution: whether high-urgency needs are being matched fairly
    - Response Equity: match rates compared across all categories
    """
    if df.empty:
        return {"error": "No data available for fairness analysis."}

    report = {}

    # --- 1. Geographic Coverage ---
    # Divide the map into NW/NE/SW/SE quadrants around the centroid
    lat_mid = df['latitude'].median()
    lon_mid = df['longitude'].median()

    def quadrant(row):
        ns = 'North' if row['latitude'] >= lat_mid else 'South'
        ew = 'East'  if row['longitude'] >= lon_mid else 'West'
        return f"{ns}-{ew}"

    df = df.copy()
    df['quadrant'] = df.apply(quadrant, axis=1)
    geo = df.groupby('quadrant').agg(
        total_needs=('status', 'count'),
        matched=('status', lambda x: (x == 'Matched').sum()),
    )
    geo['match_rate_pct'] = (geo['matched'] / geo['total_needs'] * 100).round(1)
    report['geographic_coverage'] = geo[['total_needs', 'matched', 'match_rate_pct']].to_dict()

    # --- 2. Urgency Distribution ---
    bins   = [0, 3, 6, 10]
    labels = ['Low (1-3)', 'Medium (4-6)', 'High (7-10)']
    df['urgency_band'] = pd.cut(df['urgency'], bins=bins, labels=labels)
    urg = df.groupby('urgency_band', observed=True).agg(
        total=('status', 'count'),
        matched=('status', lambda x: (x == 'Matched').sum()),
        avg_urgency=('urgency', 'mean'),
    )
    urg['match_rate_pct'] = (urg['matched'] / urg['total'] * 100).round(1)
    urg['avg_urgency']    = urg['avg_urgency'].round(2)
    report['urgency_distribution'] = urg[['total', 'matched', 'match_rate_pct', 'avg_urgency']].to_dict()

    # --- 3. Response Equity (by Category) ---
    resp = df.groupby('category').agg(
        total=('status', 'count'),
        matched=('status', lambda x: (x == 'Matched').sum()),
        avg_urgency=('urgency', 'mean'),
    )
    resp['match_rate_pct'] = (resp['matched'] / resp['total'] * 100).round(1)
    resp['avg_urgency']    = resp['avg_urgency'].round(2)
    # Flag under-served: match_rate below overall average
    overall_match_rate = (df['status'] == 'Matched').mean() * 100
    resp['status'] = resp['match_rate_pct'].apply(
        lambda r: '✅ Equitable' if r >= overall_match_rate else '⚠️ Under-Served'
    )
    report['response_equity'] = resp[['total', 'matched', 'match_rate_pct', 'avg_urgency', 'status']].to_dict()

    # --- Summary ---
    report['summary'] = {
        'overall_match_rate_pct': round(overall_match_rate, 1),
        'total_needs_analyzed': int(len(df)),
        'parity_score_pct': float(calculate_parity_score(df)),
        'under_served_categories': [
            cat for cat, s in resp['status'].items() if '⚠️' in s
        ],
    }

    return report

=======
@st.cache_data
>>>>>>> 978ae7b52b392d91b7b0b1de59e4a27fca9ab4c1
def calculate_parity_score(needs_df):
    """
    Calculates a 'Parity Score' based on the ratio of Matched vs Pending tasks
    across different geospatial sectors/categories, normalized by Urgency.
    100% = Perfectly Equitable (resources going where urgency is highest).
    < 70% = High Risk of Operational Bias.
    """
    if needs_df.empty: return 100
    
    # 1. Group by Category (Sectors)
    groups = needs_df.groupby('category')
    sector_metrix = []
    
    for name, group in groups:
        matched = len(group[group['status'] == 'Matched'])
        pending = len(group[group['status'] == 'Pending'])
        avg_urgency = group['urgency'].mean()
        
        # Sector Match Rate
        match_rate = matched / (matched + pending) if (matched + pending) > 0 else 1.0
        # Ideal Rate: Higher urgency sectors SHOULD have higher match rates
        sector_metrix.append(match_rate * (10 / avg_urgency)) # Normalized
        
    parity = (sum(sector_metrix) / len(sector_metrix)) * 100 if sector_metrix else 100
    return round(min(100, parity), 1)

@st.cache_data
def audit_for_bias(needs_df):
    """
    Analyzes data for under-served high-urgency clusters.
    Returns a list of warnings.
    """
    warnings = []
    if needs_df.empty: return warnings
    
    # Check for 'Silent Clusters': High urgency, multiple reports, but 0 matches.
    v_df = needs_df[needs_df['verified'] == True]
    high_urg = v_df[v_df['urgency'] >= 8]
    
    for category in high_urg['category'].unique():
        cat_df = high_urg[high_urg['category'] == category]
        unassigned = len(cat_df[cat_df['status'] == 'Pending'])
        if unassigned > 3:
            warnings.append({
                "severity": "CRITICAL",
                "message": f"🚨 **BIAS WARNING:** Cluster detection in '{category}' Sector. {unassigned} High-Urgency reports detected with ZERO resource allocation missions.",
                "remedy": f"Action Suggestion: Pivot generalist volunteers from low-urgency 'General' tasks to the '{category}' sector immediately."
            })
            
    return warnings

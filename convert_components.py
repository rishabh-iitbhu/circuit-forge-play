#!/usr/bin/env python3
"""
Convert Excel component databases to CSV and standardize naming
"""

import pandas as pd
import os

def convert_excel_to_csv():
    """Convert Excel files to standardized CSV format"""
    
    base_path = "assets/component_data"
    
    # Convert input capacitors
    print("📋 Converting input capacitors...")
    try:
        input_cap_df = pd.read_excel(f"{base_path}/input_capacitor_db_powercrux.xlsx")
        
        # Standardize column names for input capacitors
        input_cap_df.columns = [col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '').replace('µ', 'u') for col in input_cap_df.columns]
        
        # Save as CSV
        input_cap_df.to_csv(f"{base_path}/input_capacitors.csv", index=False)
        print(f"✅ Created input_capacitors.csv with {len(input_cap_df)} components")
        print(f"   Columns: {list(input_cap_df.columns)}")
        
    except Exception as e:
        print(f"❌ Error converting input capacitors: {e}")
    
    # Convert inductors
    print("\n🧲 Converting inductors...")
    try:
        # Try different sheet names that might exist
        inductors_df = pd.read_excel(f"{base_path}/powercrux_inductors_20parts (2).xlsx")
        
        # Standardize column names for inductors
        inductors_df.columns = [col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '').replace('µ', 'u') for col in inductors_df.columns]
        
        # Save as CSV (this will replace the existing inductors.csv)
        inductors_df.to_csv(f"{base_path}/inductors.csv", index=False)
        print(f"✅ Updated inductors.csv with {len(inductors_df)} components")
        print(f"   Columns: {list(inductors_df.columns)}")
        
    except Exception as e:
        print(f"❌ Error converting inductors: {e}")
    
    # Rename existing files to standard names
    print("\n📂 Standardizing existing files...")
    
    # Rename capacitors.csv to output_capacitors.csv if it exists
    old_capacitors = f"{base_path}/capacitors.csv"
    new_output_capacitors = f"{base_path}/output_capacitors.csv"
    
    if os.path.exists(old_capacitors):
        if os.path.exists(new_output_capacitors):
            os.remove(new_output_capacitors)
        os.rename(old_capacitors, new_output_capacitors)
        print("✅ Renamed capacitors.csv → output_capacitors.csv")
    
    # mosfets.csv already has the right name
    print("✅ mosfets.csv already properly named")
    
    print("\n🎯 Final standardized component files:")
    for filename in ["input_capacitors.csv", "output_capacitors.csv", "inductors.csv", "mosfets.csv"]:
        filepath = f"{base_path}/{filename}"
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            print(f"   ✅ {filename}: {len(df)} components")
        else:
            print(f"   ❌ {filename}: Missing")

if __name__ == "__main__":
    convert_excel_to_csv()
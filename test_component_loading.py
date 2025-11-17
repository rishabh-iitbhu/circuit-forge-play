#!/usr/bin/env python3
"""
Test script to debug component loading issues
"""

import sys
import os

print("Testing component data loading...")

try:
    # Test basic imports
    print("1. Testing basic imports...")
    import pandas as pd
    print("   ✓ pandas imported successfully")
    
    # Test if pyarrow is available
    try:
        import pyarrow
        print("   ✓ pyarrow is available")
    except ImportError:
        print("   ⚠ pyarrow not available (this is OK)")
    
    # Test component data loading
    print("\n2. Testing component data imports...")
    from lib.component_data import MOSFET_LIBRARY, CAPACITOR_LIBRARY, INPUT_CAPACITOR_LIBRARY, INDUCTOR_LIBRARY
    
    print(f"   ✓ MOSFETs loaded: {len(MOSFET_LIBRARY)} components")
    print(f"   ✓ Output capacitors loaded: {len(CAPACITOR_LIBRARY)} components")
    print(f"   ✓ Input capacitors loaded: {len(INPUT_CAPACITOR_LIBRARY)} components")
    print(f"   ✓ Inductors loaded: {len(INDUCTOR_LIBRARY)} components")
    
    # Test DataFrame creation without pyarrow
    print("\n3. Testing DataFrame creation...")
    if INPUT_CAPACITOR_LIBRARY:
        test_data = []
        for cap in INPUT_CAPACITOR_LIBRARY[:2]:  # Test first 2
            test_data.append({
                "Part": cap.part_number,
                "Manufacturer": cap.manufacturer,
                "Capacitance": cap.capacitance,
                "Voltage": cap.voltage
            })
        
        df = pd.DataFrame(test_data)
        print("   ✓ DataFrame created successfully")
        print(f"   DataFrame shape: {df.shape}")
        print("   DataFrame columns:", df.columns.tolist())
    
    print("\n✅ All tests passed! Component loading should work.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
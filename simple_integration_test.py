#!/usr/bin/env python3
"""
Simple test for web component integration - no external deps
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.web_component_scraper import WebComponentScraper
from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors, suggest_input_capacitors

def test_mosfet_suggestions_web():
    """Test MOSFET suggestions with web search"""
    print("🔹 Testing MOSFET suggestions with web search...")
    try:
        # Test parameters
        voltage_input = 24.0
        voltage_output = 5.0
        current_output = 3.0
        frequency = 100000
        
        suggestions = suggest_mosfets(
            voltage_input=voltage_input,
            voltage_output=voltage_output,
            current_output=current_output,
            frequency=frequency,
            use_web_search=True
        )
        
        print(f"   ✅ Got {len(suggestions)} MOSFET suggestions")
        
        # Test that we can access component attributes
        for i, suggestion in enumerate(suggestions[:2]):  # Check first 2
            comp = suggestion.component
            print(f"   📦 Component {i+1}: {getattr(comp, 'name', 'No name')} by {getattr(comp, 'manufacturer', 'Unknown')}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ MOSFET test failed: {e}")
        return False

def test_capacitor_suggestions_web():
    """Test capacitor suggestions with web search"""
    print("🔹 Testing Capacitor suggestions with web search...")
    try:
        suggestions = suggest_capacitors(
            voltage_input=24.0,
            voltage_output=5.0,
            current_output=3.0,
            frequency=100000,
            use_web_search=True
        )
        
        print(f"   ✅ Got {len(suggestions)} capacitor suggestions")
        
        # Test that we can access component attributes
        for i, suggestion in enumerate(suggestions[:2]):  # Check first 2
            comp = suggestion.component
            print(f"   📦 Component {i+1}: {getattr(comp, 'name', 'No name')} by {getattr(comp, 'manufacturer', 'Unknown')}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Capacitor test failed: {e}")
        return False

def main():
    """Run simple integration tests"""
    print("🧪 Simple Web Component Integration Test")
    print("=" * 50)
    
    # Test individual components
    mosfet_ok = test_mosfet_suggestions_web()
    capacitor_ok = test_capacitor_suggestions_web()
    
    print("\n" + "=" * 50)
    print("📋 RESULTS:")
    print(f"MOSFETs: {'✅ PASS' if mosfet_ok else '❌ FAIL'}")
    print(f"Capacitors: {'✅ PASS' if capacitor_ok else '❌ FAIL'}")
    
    if mosfet_ok and capacitor_ok:
        print("🎉 Web component integration working!")
    else:
        print("⚠️  Some issues remain")

if __name__ == "__main__":
    main()
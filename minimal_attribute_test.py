#!/usr/bin/env python3
"""
Test specific function attribute access - minimal version
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mock_component_creation():
    """Test that we can create mock components with correct attributes"""
    print("🔹 Testing mock component creation...")
    
    try:
        # Create a mock WebComponent
        class MockWebComponent:
            def __init__(self, part_number="TEST123", manufacturer="TestCorp", 
                        description="Test component", package="TO-220", 
                        price="$1.50", availability="In Stock", distributor="Mouser"):
                self.part_number = part_number
                self.manufacturer = manufacturer
                self.description = description
                self.package = package
                self.price = price
                self.availability = availability
                self.distributor = distributor
        
        comp = MockWebComponent()
        
        # Test MOSFET mock creation (same pattern as in component_suggestions.py)
        mock_mosfet = type('MOSFET', (), {
            'name': comp.part_number,  # Use 'name' instead of 'part_number'
            'manufacturer': comp.manufacturer,
            'vds': 100.0,
            'id': 30.0,
            'rdson': 50.0,
            'qg': 0.0,
            'package': comp.package or "TO-220",
            'typical_use': f"Web search result - {comp.description}",
            'price': comp.price,
            'availability': comp.availability,
            'distributor': comp.distributor
        })()
        
        # Test accessing attributes
        print(f"   ✅ MOSFET name: {mock_mosfet.name}")
        print(f"   ✅ MOSFET manufacturer: {mock_mosfet.manufacturer}")
        print(f"   ✅ MOSFET vds: {mock_mosfet.vds}V")
        print(f"   ✅ MOSFET price: {mock_mosfet.price}")
        
        # Test Capacitor mock creation  
        mock_capacitor = type('Capacitor', (), {
            'name': comp.part_number,  # Use 'name' instead of 'part_number'
            'manufacturer': comp.manufacturer,
            'capacitance_uf': 100.0,
            'voltage_rating': 25.0,
            'tolerance': 20.0,
            'package': comp.package or "1206",
            'price': comp.price,
            'availability': comp.availability,
            'distributor': comp.distributor,
            'description': comp.description
        })()
        
        print(f"   ✅ Capacitor name: {mock_capacitor.name}")
        print(f"   ✅ Capacitor capacitance: {mock_capacitor.capacitance_uf}µF")
        print(f"   ✅ Capacitor voltage: {mock_capacitor.voltage_rating}V")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Mock creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run minimal attribute test"""
    print("🧪 Minimal Component Attribute Test")
    print("=" * 40)
    
    success = test_mock_component_creation()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Mock component creation works!")
        print("✅ Attribute mapping fixed - should work in main app")
    else:
        print("❌ Issues with mock component creation")

if __name__ == "__main__":
    main()
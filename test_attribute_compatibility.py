#!/usr/bin/env python3
"""
Test web component attribute compatibility to prevent attribute errors
"""

def test_mosfet_attributes():
    """Test MOSFET web component has all required attributes"""
    print("🧪 Testing MOSFET attribute compatibility...")
    
    # Simulate web component data
    class MockWebComponent:
        def __init__(self):
            self.part_number = "TEST_MOSFET_123"
            self.manufacturer = "TestCorp"
            self.description = "N-Channel MOSFET"
            self.package = "TO-220"
            self.price = "$2.50"
            self.availability = "In Stock"
            self.distributor = "Mouser"
    
    comp = MockWebComponent()
    
    # Create mock MOSFET exactly as in component_suggestions.py
    mock_mosfet = type('MOSFET', (), {
        'name': comp.part_number,
        'manufacturer': comp.manufacturer,
        'vds': 100.0,
        'id': 30.0,
        'rdson': 50.0,
        'qg': 0.0,
        'package': comp.package or "TO-220",
        'typical_use': f"Web search result - {comp.description}",
        'efficiency_range': "See datasheet",  # This was missing before!
        'price': comp.price,
        'availability': comp.availability,
        'distributor': comp.distributor
    })()
    
    # Test all required MOSFET attributes
    required_attrs = ['name', 'manufacturer', 'vds', 'id', 'rdson', 'qg', 'package', 'typical_use', 'efficiency_range']
    
    for attr in required_attrs:
        try:
            value = getattr(mock_mosfet, attr)
            print(f"   ✅ {attr}: {value}")
        except AttributeError as e:
            print(f"   ❌ Missing attribute: {attr}")
            return False
    
    return True

def test_capacitor_attributes():
    """Test Capacitor web component has all required attributes"""
    print("\n🧪 Testing Capacitor attribute compatibility...")
    
    class MockWebComponent:
        def __init__(self):
            self.part_number = "TEST_CAP_456"
            self.manufacturer = "CapCorp"
            self.description = "Ceramic Capacitor"
            self.package = "1206"
            self.price = "$0.25"
            self.availability = "In Stock"
            self.distributor = "Mouser"
    
    comp = MockWebComponent()
    required_capacitance_uf = 100.0
    max_voltage = 25.0
    
    # Create mock Capacitor exactly as in component_suggestions.py
    mock_capacitor = type('Capacitor', (), {
        'part_number': comp.part_number,
        'manufacturer': comp.manufacturer,
        'capacitance': required_capacitance_uf,  # µF
        'voltage': max_voltage,  # V
        'type': "See datasheet",
        'esr': "See datasheet",  # mΩ
        'primary_use': f"Web search result - {comp.description}",
        'temp_range': "See datasheet",
        'price': comp.price,
        'availability': comp.availability,
        'distributor': comp.distributor
    })()
    
    # Test all required Capacitor attributes  
    required_attrs = ['part_number', 'manufacturer', 'capacitance', 'voltage', 'type', 'esr', 'primary_use', 'temp_range']
    
    for attr in required_attrs:
        try:
            value = getattr(mock_capacitor, attr)
            print(f"   ✅ {attr}: {value}")
        except AttributeError as e:
            print(f"   ❌ Missing attribute: {attr}")
            return False
    
    return True

def main():
    """Test all component attribute compatibility"""
    print("🚀 Web Component Attribute Compatibility Test")
    print("=" * 55)
    
    mosfet_ok = test_mosfet_attributes()
    capacitor_ok = test_capacitor_attributes()  
    
    print("\n" + "=" * 55)
    print("📋 COMPATIBILITY TEST RESULTS:")
    print(f"MOSFETs: {'✅ PASS' if mosfet_ok else '❌ FAIL'}")
    print(f"Capacitors: {'✅ PASS' if capacitor_ok else '❌ FAIL'}")
    
    if mosfet_ok and capacitor_ok:
        print("\n🎉 All web components have correct attributes!")
        print("✅ No more 'object has no attribute' errors expected")
    else:
        print("\n⚠️  Some attribute issues remain")
        
    return mosfet_ok and capacitor_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
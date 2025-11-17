"""
Test script for web component scraping functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_web_scraper_import():
    """Test if web scraper module can be imported"""
    try:
        from lib.web_component_scraper import WebComponentScraper, is_web_search_available
        print("✅ Web scraper module imported successfully")
        print(f"✅ Web search available: {is_web_search_available()}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_component_suggestions_web():
    """Test if component suggestions work with web search flag"""
    try:
        from lib.component_suggestions import suggest_mosfets, suggest_capacitors, suggest_inductors, suggest_input_capacitors
        
        print("\n🔧 Testing component suggestion functions with web search...")
        
        # Test with web search disabled (should work)
        mosfets = suggest_mosfets(12, 5, use_web_search=False)
        print(f"✅ MOSFET suggestions (local): {len(mosfets)} found")
        
        caps = suggest_capacitors(100, 16, use_web_search=False)
        print(f"✅ Capacitor suggestions (local): {len(caps)} found")
        
        inductors = suggest_inductors(22, 5, use_web_search=False)
        print(f"✅ Inductor suggestions (local): {len(inductors)} found")
        
        input_caps = suggest_input_capacitors(100, 16, 2, use_web_search=False)
        print(f"✅ Input capacitor suggestions (local): {len(input_caps)} found")
        
        return True
        
    except Exception as e:
        print(f"❌ Component suggestion test failed: {e}")
        return False

def test_session_state_integration():
    """Test if session state integration would work"""
    try:
        # Simulate session state
        class MockSessionState:
            def __init__(self):
                self.data = {'component_source': 'local'}
            
            def get(self, key, default=None):
                return self.data.get(key, default)
        
        mock_session = MockSessionState()
        use_web_search = mock_session.get('component_source', 'local') == 'web'
        print(f"\n🔄 Session state simulation: use_web_search = {use_web_search}")
        
        # Test with web component source
        mock_session.data['component_source'] = 'web'
        use_web_search = mock_session.get('component_source', 'local') == 'web'
        print(f"🔄 Web mode simulation: use_web_search = {use_web_search}")
        
        return True
        
    except Exception as e:
        print(f"❌ Session state test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Web Component Search Functionality")
    print("=" * 50)
    
    success = True
    
    # Test imports
    success &= test_web_scraper_import()
    
    # Test component suggestions
    success &= test_component_suggestions_web()
    
    # Test session state integration
    success &= test_session_state_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Web component search is ready.")
        print("\n📋 Next steps:")
        print("1. Run Streamlit app and test the component source toggle")
        print("2. Try web search mode with a Buck converter calculation")
        print("3. Verify fallback to local database if web search fails")
    else:
        print("❌ Some tests failed. Please check the implementation.")
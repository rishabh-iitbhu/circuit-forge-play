#!/usr/bin/env python3
"""
Test the improved web search functionality
"""

from lib.web_component_scraper import WebComponentScraper
import time

def test_timeout_functionality():
    """Test that timeout works properly"""
    print('🧪 Testing timeout functionality...')
    
    scraper = WebComponentScraper()
    start_time = time.time()

    # This should timeout quickly
    components = scraper._search_with_timeout(
        lambda: scraper.search_mouser('test', 'mosfet'), 
        2.0  # 2 second timeout
    )

    elapsed = time.time() - start_time
    print(f'⏱️  Search completed in {elapsed:.2f} seconds')
    print(f'📦 Found {len(components)} components')
    
    if elapsed <= 3.0:  # Should be close to 2 seconds
        print('✅ Timeout mechanism working!')
        return True
    else:
        print('❌ Timeout may not be working properly')
        return False

def test_fallback_components():
    """Test fallback component generation"""
    print('\n🧪 Testing fallback components...')
    
    scraper = WebComponentScraper()
    mosfet_comps = scraper._get_mouser_fallback_components('N-Channel MOSFET', 'mosfet')
    
    print(f'📦 Generated {len(mosfet_comps)} fallback MOSFETs')
    if mosfet_comps:
        print(f'   Sample: {mosfet_comps[0].part_number} by {mosfet_comps[0].manufacturer}')
        print('✅ Fallback components working!')
        return True
    
    print('❌ Fallback components not working')
    return False

def main():
    """Run all tests"""
    print("🚀 Testing Enhanced Web Search Functionality")
    print("=" * 50)
    
    timeout_ok = test_timeout_functionality()
    fallback_ok = test_fallback_components()
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS:")
    print(f"Timeout Mechanism: {'✅ PASS' if timeout_ok else '❌ FAIL'}")
    print(f"Fallback Components: {'✅ PASS' if fallback_ok else '❌ FAIL'}")
    
    if timeout_ok and fallback_ok:
        print("\n🎉 All core functionality working!")
        print("💡 Ready to test in Streamlit app")
    else:
        print("\n⚠️  Some issues detected")

if __name__ == "__main__":
    main()
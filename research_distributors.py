"""
Deep research script for Mouser and Digikey search mechanisms
This script will analyze their actual HTML structure and search patterns
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import quote_plus

def research_mouser_structure():
    """Research Mouser.com search structure"""
    print("🔍 Researching Mouser.com structure...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # Test different Mouser search approaches
    search_urls = [
        "https://www.mouser.com/c/semiconductors/discrete-semiconductors/transistors/mosfets-single/?q=MOSFET",
        "https://www.mouser.com/c/?q=MOSFET",
        "https://www.mouser.com/ProductDetail/?qs=%252B6g0mu59x7L8%252Bgjcsg0bfg%253D%253D",  # Sample product
        "https://www.mouser.com/c/semiconductors/discrete-semiconductors/transistors/mosfets-single/"
    ]
    
    for i, url in enumerate(search_urls):
        try:
            print(f"\n📍 Testing Mouser URL {i+1}: {url}")
            response = session.get(url, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for common product listing patterns
                product_patterns = [
                    'div[class*="product"]',
                    'tr[class*="product"]', 
                    'div[class*="search-result"]',
                    'div[class*="part-"]',
                    '.SearchResultsRowData',
                    '.grid-item',
                    '[data-testid*="product"]'
                ]
                
                for pattern in product_patterns:
                    elements = soup.select(pattern)
                    if elements:
                        print(f"   ✅ Found {len(elements)} elements with pattern: {pattern}")
                        
                        # Analyze first element structure
                        if len(elements) > 0:
                            first_elem = elements[0]
                            print(f"      Sample element classes: {first_elem.get('class', [])}")
                            print(f"      Sample element text (first 100 chars): {first_elem.get_text()[:100]}")
                
                # Look for specific data elements
                part_numbers = soup.find_all(text=lambda t: t and ('IRF' in t or 'BSS' in t or 'FQP' in t))[:3]
                if part_numbers:
                    print(f"   📝 Sample part numbers found: {part_numbers}")
                
                # Look for price patterns
                price_elements = soup.find_all(text=lambda t: t and '$' in str(t))[:3]
                if price_elements:
                    print(f"   💰 Sample prices found: {price_elements}")
            
            time.sleep(2)  # Be respectful
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def research_digikey_structure():
    """Research Digikey.com search structure"""
    print("\n🔍 Researching Digikey.com structure...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    })
    
    # Test different Digikey approaches
    search_urls = [
        "https://www.digikey.com/en/products/filter/transistors-fets-mosfets-single/278?s=N4IgjCBcoLQBxVAYygMwIYBsDOBTANCAPZQDaIALAAwg4CcADABwgC%2BhCQA",  # Category page
        "https://www.digikey.com/en/products/filter/transistors-fets-mosfets-single/278",
        "https://www.digikey.com/en/products/detail/infineon-technologies/IRLB8721PBF/2127443"  # Sample product
    ]
    
    for i, url in enumerate(search_urls):
        try:
            print(f"\n📍 Testing Digikey URL {i+1}: {url}")
            response = session.get(url, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for common Digikey patterns
                product_patterns = [
                    'tr[data-testid="row"]',
                    'div[data-testid*="product"]',
                    '.product-table-row',
                    '.search-results-content',
                    '[data-testid="data-table-row"]',
                    'tbody tr'
                ]
                
                for pattern in product_patterns:
                    elements = soup.select(pattern)
                    if elements:
                        print(f"   ✅ Found {len(elements)} elements with pattern: {pattern}")
                        
                        if len(elements) > 0:
                            first_elem = elements[0]
                            print(f"      Sample element: {first_elem.name} with classes: {first_elem.get('class', [])}")
                            cells = first_elem.find_all(['td', 'div'])[:5]
                            if cells:
                                print(f"      Sample cell contents: {[cell.get_text().strip()[:50] for cell in cells]}")
                
                # Look for JSON data (common in modern sites)
                scripts = soup.find_all('script', type='application/json')
                if scripts:
                    print(f"   📄 Found {len(scripts)} JSON scripts")
                
            time.sleep(3)  # More conservative for Digikey
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_simple_search():
    """Test a very basic search to see what we get"""
    print("\n🧪 Testing simple search approaches...")
    
    # Test Mouser with a known part
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Try Mouser API-like endpoint
        mouser_test_url = "https://www.mouser.com/api/search/keyword?keyword=IRLB8721"
        print(f"🔍 Testing Mouser API: {mouser_test_url}")
        
        response = session.get(mouser_test_url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON response received! Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            except:
                print(f"   📄 Non-JSON response, length: {len(response.text)}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Error testing Mouser API: {e}")

if __name__ == "__main__":
    print("🔬 Deep Research: Mouser and Digikey Search Mechanisms")
    print("=" * 60)
    
    # Research both sites
    research_mouser_structure()
    research_digikey_structure()
    test_simple_search()
    
    print("\n" + "=" * 60)
    print("🎯 Research Complete! Check output above for working patterns.")
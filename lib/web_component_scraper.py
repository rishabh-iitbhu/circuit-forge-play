"""
Web Component Scraper for Mouser and Digikey
Provides functionality to search for electronic components from major distributors
"""

import time
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import streamlit as st

# Web scraping imports (with fallback)
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False

@dataclass
class WebComponent:
    """Represents a component found via web search"""
    part_number: str
    manufacturer: str
    description: str
    price: str
    availability: str
    datasheet_url: Optional[str] = None
    distributor: str = ""
    package: Optional[str] = None
    specifications: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}

class WebComponentScraper:
    """Main scraper class for component distributors"""
    
    def __init__(self):
        self.session = requests.Session() if WEB_SCRAPING_AVAILABLE else None
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests
        
        # Set user agent to avoid blocking
        if self.session:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def _rate_limit(self):
        """Ensure we don't make requests too quickly"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def search_mouser(self, search_term: str, component_type: str) -> List[WebComponent]:
        """
        Search Mouser.com for components
        
        Args:
            search_term: Component search term (e.g., "MOSFET N-Channel 100V")
            component_type: Type of component ("mosfet", "capacitor", "inductor")
        
        Returns:
            List of WebComponent objects
        """
        if not WEB_SCRAPING_AVAILABLE:
            return []
        
        try:
            self._rate_limit()
            
            # Mouser search URL
            search_url = f"https://www.mouser.com/c/?q={search_term.replace(' ', '%20')}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            components = []
            
            # Find component results (this is a simplified parser - may need adjustment)
            product_divs = soup.find_all('div', class_='SearchResultsRowData')[:5]  # Top 5
            
            for div in product_divs:
                try:
                    # Extract basic information
                    part_number_elem = div.find('div', class_='MouserPartNumber')
                    manufacturer_elem = div.find('div', class_='ManufacturerName')
                    description_elem = div.find('div', class_='PartDescription')
                    price_elem = div.find('div', class_='PriceBreaks')
                    availability_elem = div.find('div', class_='AvailabilityCell')
                    
                    if part_number_elem and description_elem:
                        component = WebComponent(
                            part_number=part_number_elem.get_text(strip=True),
                            manufacturer=manufacturer_elem.get_text(strip=True) if manufacturer_elem else "Unknown",
                            description=description_elem.get_text(strip=True),
                            price=price_elem.get_text(strip=True) if price_elem else "Contact for pricing",
                            availability=availability_elem.get_text(strip=True) if availability_elem else "Check availability",
                            distributor="Mouser"
                        )
                        components.append(component)
                        
                except Exception as e:
                    st.warning(f"Error parsing Mouser component: {e}")
                    continue
            
            return components
            
        except Exception as e:
            st.error(f"Error searching Mouser: {e}")
            return []
    
    def search_digikey(self, search_term: str, component_type: str) -> List[WebComponent]:
        """
        Search Digikey.com for components
        
        Args:
            search_term: Component search term
            component_type: Type of component
        
        Returns:
            List of WebComponent objects
        """
        if not WEB_SCRAPING_AVAILABLE:
            return []
        
        try:
            self._rate_limit()
            
            # Digikey search URL
            search_url = f"https://www.digikey.com/en/products/filter/{component_type}?keywords={search_term.replace(' ', '%20')}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            components = []
            
            # Find component results (simplified parser)
            product_rows = soup.find_all('tr', {'data-testid': 'row'})[:5]  # Top 5
            
            for row in product_rows:
                try:
                    # Extract information from table cells
                    cells = row.find_all('td')
                    
                    if len(cells) >= 4:
                        part_number = cells[1].get_text(strip=True) if len(cells) > 1 else "Unknown"
                        description = cells[2].get_text(strip=True) if len(cells) > 2 else "No description"
                        manufacturer = cells[0].get_text(strip=True) if len(cells) > 0 else "Unknown"
                        price = cells[3].get_text(strip=True) if len(cells) > 3 else "Contact for pricing"
                        availability = cells[4].get_text(strip=True) if len(cells) > 4 else "Check availability"
                        
                        component = WebComponent(
                            part_number=part_number,
                            manufacturer=manufacturer,
                            description=description,
                            price=price,
                            availability=availability,
                            distributor="Digikey"
                        )
                        components.append(component)
                        
                except Exception as e:
                    st.warning(f"Error parsing Digikey component: {e}")
                    continue
            
            return components
            
        except Exception as e:
            st.error(f"Error searching Digikey: {e}")
            return []
    
    def search_components(self, search_term: str, component_type: str) -> Dict[str, List[WebComponent]]:
        """
        Search both Mouser and Digikey for components
        
        Args:
            search_term: Component search term
            component_type: Type of component
        
        Returns:
            Dictionary with distributor names as keys and component lists as values
        """
        if not WEB_SCRAPING_AVAILABLE:
            st.error("Web scraping libraries not available. Please install requests and beautifulsoup4.")
            return {}
        
        results = {}
        
        # Search Mouser
        with st.spinner("Searching Mouser.com..."):
            mouser_results = self.search_mouser(search_term, component_type)
            if mouser_results:
                results["Mouser"] = mouser_results
        
        # Search Digikey  
        with st.spinner("Searching Digikey.com..."):
            digikey_results = self.search_digikey(search_term, component_type)
            if digikey_results:
                results["Digikey"] = digikey_results
        
        return results

def create_component_search_terms(circuit_params: Dict[str, Any]) -> Dict[str, str]:
    """
    Create optimized search terms for each component type based on circuit parameters
    
    Args:
        circuit_params: Dictionary containing circuit parameters (voltage, current, frequency, etc.)
    
    Returns:
        Dictionary with component types as keys and search terms as values
    """
    vin = circuit_params.get('vin', 12)
    vout = circuit_params.get('vout', 5)
    iout = circuit_params.get('iout', 2)
    freq = circuit_params.get('frequency', 100000)
    
    search_terms = {}
    
    # MOSFET search term
    # Calculate voltage rating (add safety margin)
    mosfet_voltage = int(vin * 1.5)  # 50% safety margin
    mosfet_current = int(iout * 2)   # 100% safety margin for peak current
    search_terms['mosfet'] = f"MOSFET N-Channel {mosfet_voltage}V {mosfet_current}A TO-220"
    
    # Input capacitor search term
    input_cap_voltage = int(vin * 1.2)  # 20% safety margin
    search_terms['input_capacitor'] = f"Electrolytic Capacitor {input_cap_voltage}V 100uF Low ESR"
    
    # Output capacitor search term
    output_cap_voltage = int(vout * 1.5)  # 50% safety margin
    search_terms['output_capacitor'] = f"Ceramic Capacitor {output_cap_voltage}V 10uF X7R"
    
    # Inductor search term
    # Estimate inductance based on switching frequency
    estimated_inductance = int((vin - vout) / (0.3 * iout * freq) * 1e6)  # Convert to uH
    search_terms['inductor'] = f"Power Inductor {estimated_inductance}uH {int(iout * 1.3)}A Shielded"
    
    return search_terms

def search_web_components(circuit_params: Dict[str, Any], component_types: List[str] = None) -> Dict[str, Dict[str, List[WebComponent]]]:
    """
    Search for all required components based on circuit parameters
    
    Args:
        circuit_params: Circuit design parameters
        component_types: List of component types to search for (default: all)
    
    Returns:
        Nested dictionary: component_type -> distributor -> [components]
    """
    if component_types is None:
        component_types = ['mosfet', 'input_capacitor', 'output_capacitor', 'inductor']
    
    scraper = WebComponentScraper()
    search_terms = create_component_search_terms(circuit_params)
    
    results = {}
    
    for comp_type in component_types:
        if comp_type in search_terms:
            st.write(f"🔍 Searching for {comp_type.replace('_', ' ').title()}...")
            search_term = search_terms[comp_type]
            results[comp_type] = scraper.search_components(search_term, comp_type)
    
    return results

# Utility functions for integration with existing code

def format_web_components_for_display(web_results: Dict[str, Dict[str, List[WebComponent]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Convert web search results to format compatible with existing display functions
    
    Args:
        web_results: Results from search_web_components()
    
    Returns:
        Dictionary formatted for Streamlit display
    """
    formatted = {}
    
    for comp_type, distributors in web_results.items():
        formatted[comp_type] = []
        
        for distributor, components in distributors.items():
            for comp in components:
                formatted_comp = {
                    'Part Number': comp.part_number,
                    'Manufacturer': comp.manufacturer,
                    'Description': comp.description,
                    'Price': comp.price,
                    'Availability': comp.availability,
                    'Distributor': comp.distributor,
                    'Package': comp.package or 'N/A'
                }
                
                # Add specifications if available
                if comp.specifications:
                    formatted_comp.update(comp.specifications)
                
                formatted[comp_type].append(formatted_comp)
    
    return formatted

def is_web_search_available() -> bool:
    """Check if web searching capabilities are available"""
    return WEB_SCRAPING_AVAILABLE
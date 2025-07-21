import trafilatura
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def scrape_single_url(url):
    """
    Scrape a single URL and return the text content
    """
    try:
        # Add a small delay to be respectful to servers
        time.sleep(0.5)
        
        # Fetch the URL
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            # Extract text content
            text = trafilatura.extract(downloaded)
            if text:
                return {
                    'url': url,
                    'content': text[:5000],  # Limit content length
                    'success': True
                }
        
        return {
            'url': url,
            'content': '',
            'success': False,
            'error': 'Failed to extract content'
        }
        
    except Exception as e:
        return {
            'url': url,
            'content': '',
            'success': False,
            'error': str(e)
        }

def scrape_urls(urls, max_workers=5):
    """
    Scrape multiple URLs concurrently
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scraping tasks
        future_to_url = {executor.submit(scrape_single_url, url): url for url in urls}
        
        # Process completed tasks
        for future in as_completed(future_to_url):
            result = future.result()
            if result['success'] and result['content']:
                results.append(result)
    
    return results

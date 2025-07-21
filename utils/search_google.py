import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def search_google(query, num_results=10, time_filter=None, enhanced_filtering=True):
    """
    Search Google using the Custom Search API with enhanced filtering
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_CX")
    
    if not api_key or not search_engine_id:
        raise ValueError("Google API key or Search Engine ID not configured")
    
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Enhanced query with time filter and relevance boosting
        enhanced_query = query
        if time_filter and enhanced_filtering:
            enhanced_query = f"{query} {time_filter}"
        
        # Search parameters with time restrictions
        search_params = {
            'q': enhanced_query,
            'cx': search_engine_id,
            'num': num_results
        }
        
        # Add Google's date restriction parameter for more effective time filtering
        if time_filter and 'after:' in time_filter:
            # Convert after:YYYY-MM-DD to Google's dateRestrict format
            date_part = time_filter.replace('after:', '')
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                current_date = datetime.now()
                days_diff = (current_date - date_obj).days
                search_params['dateRestrict'] = f'd{days_diff}'  # Last N days
            except:
                pass  # Fall back to query-based filtering
        
        result = service.cse().list(**search_params).execute()
        
        search_results = []
        
        if 'items' in result:
            for item in result['items']:
                search_results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'displayLink': item.get('displayLink', '')
                })
        
        return search_results
        
    except HttpError as e:
        print(f"Google Search API error: {e}")
        return []
    except Exception as e:
        print(f"Error searching Google: {e}")
        return []

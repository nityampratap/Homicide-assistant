import subprocess
import webbrowser
import os
import urllib.parse

def open_any_website(url):
    """Dynamically opens any web URL passed by the AI."""
    print(f"[OS Executing]: Navigating to web portal -> {url}")
    clean_url = str(url).strip()
    if not clean_url.startswith("http"):
        clean_url = f"https://{clean_url}"
    webbrowser.open(clean_url)
    return f"Navigating to website now."

def search_web_query(platform, query):
    """Dynamically formats and runs search queries directly inside Google or YouTube."""
    # Safely URL-encode the string (e.g. 'lofi music' becomes 'lofi%20music')
    encoded_query = urllib.parse.quote(query.strip())
    
    if "youtube" in platform.lower():
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        print(f"[OS Executing]: Running YouTube search query -> {query}")
        webbrowser.open(search_url)
        return f"Searching for {query} on YouTube."
    else:
        search_url = f"https://www.google.com/search?q={encoded_query}"
        print(f"[OS Executing]: Running Google search query -> {query}")
        webbrowser.open(search_url)
        return f"Searching Google for {query}."

def launch_any_app(app_name):
    """Dynamically attempts to launch any system application by name using Windows shell hooks."""
    print(f"[OS Executing]: Initializing local system hook for -> {app_name}")
    clean_app = str(app_name).strip().lower()
    
    try:
        subprocess.Popen(f"start {clean_app}", shell=True)
        return f"Initializing {clean_app} deployment protocols."
    except Exception:
        return f"Unable to map execution vector for {clean_app}."
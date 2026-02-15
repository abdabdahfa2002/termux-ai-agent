import subprocess
import os
import requests
from bs4 import BeautifulSoup

def execute_shell(command: str):
    """Executes a shell command in the Termux environment and returns the output.
    
    Args:
        command: The shell command to run.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nExit Code: {result.returncode}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def read_file(path: str):
    """Reads the content of a file from the filesystem.
    
    Args:
        path: The absolute or relative path to the file.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path: str, content: str):
    """Creates a new file or overwrites an existing one with the provided content.
    
    Args:
        path: The path where the file should be saved.
        content: The text content to write into the file.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully saved file to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def search_web(query: str):
    """Searches the web for the given query and returns a summary of the results.
    
    Args:
        query: The search terms to look up.
    """
    try:
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract meaningful text
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:2000]
    except Exception as e:
        return f"Search error: {str(e)}"

def get_termux_info():
    """Retrieves device information like battery status and Wi-Fi details using Termux API."""
    try:
        battery = subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True).stdout
        wifi = subprocess.run("termux-wifi-connectioninfo", shell=True, capture_output=True, text=True).stdout
        return f"Battery: {battery}\nWiFi: {wifi}"
    except Exception as e:
        return f"Error getting device info: {str(e)}"

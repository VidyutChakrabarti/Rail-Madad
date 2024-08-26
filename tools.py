from langchain.tools import tool 
from datetime import date


@tool("Get current date")
def getCurrentDate():
    """used to fetch the current date in a formatted manner."""
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    return d




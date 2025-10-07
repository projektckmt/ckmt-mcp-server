"""Configuration for the MCP server."""
import os
from dotenv import load_dotenv

load_dotenv()

# API configuration
API_BASE_URL = "https://api.ckmt.io"
API_KEY = os.getenv("API_KEY", "test-api-key-12345")

# Server configuration
MCP_SERVER_NAME = "ckmt-search"
MCP_SERVER_VERSION = "1.0.0"

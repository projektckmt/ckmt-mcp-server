# CKMT Search MCP Server

FastMCP server that exposes the CKMT search endpoints as MCP tools for use with Claude Desktop and other MCP clients.

## Features

This MCP server provides 7 tools for searching and analyzing network security data:

1. **search_host** - Get all data for a specific IP address
2. **search_hosts** - Search hosts using various filters (port, service, country, etc.)
3. **search_facets** - Get aggregated facets/statistics for search results
4. **count_hosts** - Count hosts matching search filters
5. **get_ports** - Get list of ports for a query
6. **get_services** - Get all detected services
7. **get_stats** - Get overall statistics about indexed data

## Installation

1. Navigate to the MCP server directory:
```bash
cd ckmt-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the `ckmt-mcp-server` directory with your API key:
```bash
API_KEY=your-api-key-here
```

**Important**: Replace `your-api-key-here` with your actual CKMT API key. You can use `test-api-key-12345` for testing purposes.

## Usage

### Running the Server Standalone

```bash
python server.py
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop MCP settings file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ckmt-search": {
      "command": "python",
      "args": ["/path/to/ckmt-mcp-server/server.py"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Important**: Replace `your-api-key-here` with your actual CKMT API key.

Replace `/path/to/ckmt-mcp-server` with the actual path to your project.

### Using with Other MCP Clients

The server can be used with any MCP-compatible client. Configure the client to run:

```bash
python /path/to/ckmt-mcp-server/server.py
```

## Available Tools

### search_host

Get all information for a specific IP address.

**Parameters:**
- `ip` (string, required): IP address to search for

**Example:**
```python
search_host(ip="8.8.8.8")
```

### search_hosts

Search for hosts using various filters.

**Parameters:**
- `query` (string, optional): Search query (IP, service, product, etc.)
- `port` (integer, optional): Filter by port number
- `service` (string, optional): Filter by service name
- `product` (string, optional): Filter by product name
- `version` (string, optional): Filter by version
- `country` (string, optional): Filter by country code
- `asn` (string, optional): Filter by ASN
- `os` (string, optional): Filter by operating system
- `vuln` (string, optional): Filter by vulnerability/CVE
- `http_title` (string, optional): Filter by HTTP title
- `http_status` (integer, optional): Filter by HTTP status code
- `technology` (string, optional): Filter by detected technology
- `page` (integer, optional): Page number (default: 1)
- `size` (integer, optional): Results per page (default: 10, max: 100)

**Example:**
```python
search_hosts(query="nginx", port=443, country="US", page=1, size=10)
```

### search_facets

Get aggregated facets for search results.

**Parameters:**
- `query` (string, optional): Search query to filter results
- `facets` (string, optional): Comma-separated facets (default: "country,port,service,technology")

Available facets: country, port, service, technology, asn, os, vulnerability

**Example:**
```python
search_facets(query="apache", facets="country,port,service")
```

### count_hosts

Count hosts matching search filters.

**Parameters:**
- `query` (string, optional): Search query
- `port` (string, optional): Filter by port
- `country` (string, optional): Filter by country code

**Example:**
```python
count_hosts(query="ssh", port="22", country="US")
```

### get_ports

Get a list of port numbers used by hosts matching the query.

**Parameters:**
- `query` (string, optional): Search query
- `size` (integer, optional): Number of results (default: 100, max: 1000)

**Example:**
```python
get_ports(query="192.168", size=50)
```

### get_services

Get a list of all detected services.

**Parameters:** None

**Example:**
```python
get_services()
```

### get_stats

Get overall statistics about the indexed data.

**Parameters:** None

**Example:**
```python
get_stats()
```

## Configuration

The server can be configured via environment variables:

- `API_KEY`: Your CKMT API key (default: `test-api-key-12345`)

## Requirements

- Python 3.8+
- CKMT API running and accessible
- FastMCP 0.2.0+
- httpx 0.24.0+

## Notes

- The server makes HTTP requests to the CKMT API using the provided API key
- API authentication is handled via Bearer token in the Authorization header
- All errors are caught and returned in the response with an "error" field
- The server acts as a proxy between MCP clients and the CKMT API
- Each tool directly maps to a CKMT API endpoint

## Troubleshooting

### Connection Issues

If you can't connect to the API:
1. Verify the API is running: `curl https://api.ckmt.io/v1/health/`
2. Ensure your API key is valid and active
3. Test API authentication: `curl -H "Authorization: Bearer YOUR_API_KEY" https://api.ckmt.io/v1/search/stats`

### Tool Not Found in Claude

1. Restart Claude Desktop after configuration changes
2. Check the MCP settings file syntax is valid JSON
3. Verify the path to `server.py` is correct and absolute
4. Check Claude Desktop logs for MCP connection errors

## License

MIT License - see [LICENSE](LICENSE) file for details.


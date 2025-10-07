"""FastMCP server for CKMT search endpoints."""
from typing import Optional
import httpx
from fastmcp import FastMCP
from config import (
    API_BASE_URL,
    API_KEY,
    MCP_SERVER_NAME,
    MCP_SERVER_VERSION,
)

# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME, version=MCP_SERVER_VERSION)


async def make_api_request(endpoint: str, params: dict = None) -> dict:
    """
    Make an authenticated request to the CKMT API.

    Args:
        endpoint: API endpoint path (e.g., "/v1/search/host/1.1.1.1")
        params: Query parameters

    Returns:
        API response as dict
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(
                f"{API_BASE_URL}{endpoint}",
                headers=headers,
                params=params or {}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": "Not found"}
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def search_host(ip: str) -> dict:
    """
    Get all available information for a specific IP address.

    Args:
        ip: IP address to search for

    Returns:
        Host information including ports, services, vulnerabilities, and HTTP endpoints
    """
    return await make_api_request(f"/v1/search/host/{ip}")


@mcp.tool()
async def search_hosts(
    query: Optional[str] = None,
    port: Optional[int] = None,
    service: Optional[str] = None,
    product: Optional[str] = None,
    version: Optional[str] = None,
    country: Optional[str] = None,
    asn: Optional[str] = None,
    os: Optional[str] = None,
    vuln: Optional[str] = None,
    http_title: Optional[str] = None,
    http_status: Optional[int] = None,
    technology: Optional[str] = None,
    page: int = 1,
    size: int = 10,
) -> dict:
    """
    Search for hosts using various filters.

    Args:
        query: Search query (IP, service, product, etc.)
        port: Filter by port number
        service: Filter by service name
        product: Filter by product name
        version: Filter by version
        country: Filter by country code
        asn: Filter by ASN
        os: Filter by operating system
        vuln: Filter by vulnerability/CVE
        http_title: Filter by HTTP title
        http_status: Filter by HTTP status code
        technology: Filter by detected technology
        page: Page number (default: 1)
        size: Results per page (default: 10, max: 100)

    Returns:
        Search results with total count and matches
    """
    params = {}

    if query is not None:
        params["query"] = query
    if port is not None:
        params["port"] = port
    if service is not None:
        params["service"] = service
    if product is not None:
        params["product"] = product
    if version is not None:
        params["version"] = version
    if country is not None:
        params["country"] = country
    if asn is not None:
        params["asn"] = asn
    if os is not None:
        params["os"] = os
    if vuln is not None:
        params["vuln"] = vuln
    if http_title is not None:
        params["http_title"] = http_title
    if http_status is not None:
        params["http_status"] = http_status
    if technology is not None:
        params["technology"] = technology

    params["page"] = page
    params["size"] = size

    return await make_api_request("/v1/search", params)


@mcp.tool()
async def search_facets(
    query: Optional[str] = None,
    facets: str = "country,port,service,technology"
) -> dict:
    """
    Get aggregated facets for search results.

    Args:
        query: Search query to filter results
        facets: Comma-separated list of facets to return
                (options: country, port, service, technology, asn, os, vulnerability)

    Returns:
        Aggregated facets with counts
    """
    params = {"facets": facets}
    if query is not None:
        params["query"] = query

    return await make_api_request("/v1/search/facets", params)


@mcp.tool()
async def count_hosts(
    query: Optional[str] = None,
    port: Optional[str] = None,
    country: Optional[str] = None
) -> dict:
    """
    Count the number of hosts matching the search filters.

    Args:
        query: Search query
        port: Filter by port
        country: Filter by country code

    Returns:
        Count of matching hosts
    """
    params = {}
    if query is not None:
        params["query"] = query
    if port is not None:
        params["port"] = port
    if country is not None:
        params["country"] = country

    return await make_api_request("/v1/search/count", params)


@mcp.tool()
async def get_ports(
    query: Optional[str] = None,
    size: int = 100
) -> dict:
    """
    Get a list of port numbers that have been used by hosts matching the query.

    Args:
        query: Search query
        size: Number of results (default: 100, max: 1000)

    Returns:
        List of ports sorted numerically
    """
    params = {"size": size}
    if query is not None:
        params["query"] = query

    result = await make_api_request("/v1/search/ports", params)

    # The API returns {"ports": [...]} but we want {"ports": [...]} format
    # If the API returns {"data": [...]}, rename it to {"ports": [...]}
    if "data" in result and "ports" not in result:
        result["ports"] = result.pop("data")

    return result


@mcp.tool()
async def get_services() -> dict:
    """
    Get a list of all services that have been detected.

    Returns:
        List of service names
    """
    return await make_api_request("/v1/search/services")


@mcp.tool()
async def get_stats() -> dict:
    """
    Get overall statistics about the indexed data.

    Returns:
        Statistics including total hosts, ports, vulnerabilities, etc.
    """
    return await make_api_request("/v1/search/stats")


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

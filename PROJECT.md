# RCP API Client Project

## Overview
This project provides a Python client for interacting with the RCP (Revenue Cycle Platform) API at drill.gghc.com. It includes functionality to fetch payment requests, update payment request statuses, and retrieve year-to-date payment data.

## Project Structure
```
RCPMCP/
├── rcp_api_python.py      # Main Python API client
├── mcp_server.py          # MCP server for Claude Desktop integration
├── RCP_api_example.sh     # Shell script examples (bash/curl)
├── rcp_api_example.py     # Empty Python file (placeholder)
├── requirements.txt       # Python dependencies
├── venv/                  # Virtual environment directory
├── .gitignore            # Git ignore rules
├── PROJECT.md            # This file
└── TODO.md               # Project tasks and improvements
```

## Technology Stack
- **Language**: Python 3.x
- **HTTP Library**: requests 2.31.0
- **MCP Integration**: mcp >=1.0.0 (Model Context Protocol)
- **Additional Libraries**: urllib3 (for SSL warning suppression)
- **Environment**: Virtual environment (venv)

## Features
The API client provides three main functions:

1. **get_payment_requests()** - Fetches payment requests for a specific employee and period
2. **update_payment_request()** - Updates payment request approval/rejection status
3. **get_payments_ytd()** - Retrieves year-to-date payment data

## MCP Server Integration
The project includes an MCP (Model Context Protocol) server that allows Claude Desktop to directly interact with the RCP API. The MCP server provides:

- **Direct API Access**: Claude Desktop can call RCP API endpoints through MCP tools
- **Real-time Data**: Get live payment data without manual script execution
- **Interactive Workflows**: Enable conversational interactions with the RCP system
- **Secure Integration**: Maintains existing authentication and SSL handling

## Setup and Installation

### Prerequisites
- Python 3.x installed on your system
- Access to the drill.gghc.com API endpoints
- Valid session cookies for authentication

### Installation Steps
1. Clone or download the project files
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
The script uses hardcoded session cookies and headers in the following constants:
- `SESSION_COOKIES` - Authentication cookies for API access
- `COMMON_HEADERS` - Standard HTTP headers for requests

**Note**: Update these values with your actual session data before running.

## How to Run

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run the main script
python rcp_api_python.py
```

### Individual Function Usage
```python
from rcp_api_python import get_payment_requests, update_payment_request, get_payments_ytd

# Fetch payment requests
payment_data = get_payment_requests(emp_id=154, period_id=202506)

# Update a payment request
update_result = update_payment_request(
    emp_id=154, 
    request_id=85360, 
    split=0.1, 
    producer_approved=True
)

# Get YTD payments
ytd_data = get_payments_ytd(emp_id=154, period_id=202506)
```

## Output Files
The script generates JSON files for each API call:
- `payment_requests.json` - Payment requests data
- `approval_json.json` - Update operation results
- `payments_ytd.json` - Year-to-date payments data

## SSL Configuration
The project includes SSL verification bypass (`verify=False`) to handle certificate issues with the target domain. This is configured in the requests calls and SSL warnings are suppressed using urllib3.

## Error Handling
- All API calls include try-catch blocks for request exceptions
- HTTP status codes are checked using `response.raise_for_status()`
- Error messages are printed to console for debugging

## Security Considerations
- SSL verification is disabled (`verify=False`) - use with caution
- Session cookies are hardcoded - consider environment variables for production
- API endpoints use HTTPS but certificate verification is bypassed

## Testing
Currently, the project runs all three API endpoints sequentially when executed directly:
```bash
python rcp_api_python.py
```

To test individual functions, import them into a Python REPL or create separate test scripts.

## MCP Server Usage

### Running the MCP Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start the MCP server
python mcp_server.py
```

### Claude Desktop Configuration
Add the following to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "rcp-api-server": {
      "command": "python",
      "args": ["/Users/acd/RCPMCP/mcp_server.py"],
      "cwd": "/Users/acd/RCPMCP",
      "env": {
        "PYTHONPATH": "/Users/acd/RCPMCP/venv/lib/python3.12/site-packages"
      }
    }
  }
}
```

### Available MCP Tools
- **get_payment_requests**: Fetch payment requests for an employee/period
- **update_payment_request**: Update payment request approval status
- **get_payments_ytd**: Get year-to-date payment data

## Dependencies
- `requests==2.31.0` - HTTP library for API calls
- `mcp>=1.0.0` - Model Context Protocol for Claude Desktop integration
- `urllib3` - For SSL warning suppression (included with requests)

## Shell Script Alternative
The project also includes `RCP_api_example.sh` which provides the same functionality using curl commands. This can be useful for testing or integration with shell-based workflows.
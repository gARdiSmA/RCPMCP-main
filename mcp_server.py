#!/usr/bin/env python3
"""
MCP Server for RCP API Integration

This MCP server provides tools for Claude Desktop to interact with the RCP API,
allowing direct access to payment requests, payment updates, and YTD data.
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional, List
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session cookies - these should be updated with current session data
SESSION_COOKIES = {
    'ui-tabs-1': '0',
    '_ga_6JKEKWMK4R': 'GS2.1.s1747836433$o2$g1$t1747836555$j0$l0$h0',
    '_ga': 'GA1.2.1531443272.1674668566',
    'adAuthCookie': '291F1A7F9CD4E302C8D20DE775A64E86F67023F895855BDA141580349C32F146ADA0C78E0975B123EB5F06B199D85C79AA05ED548604783C3642AB336895A3ACEFD20D083EBFAE11EF71A49523D4FB8D01DB1C4026AAA36DD05CA62424CE500F6A30218D8F107B52FA1A71E082F96AF376A0B29C',
    'ASP.NET_SessionId': 'wttc4zpfc1tzquomalb2zuon',
    'AWSALB': 'VrEekVZIeFU1pnmxxs4X8u0b5oJKqmMYLKvw+DFxh4WuXmDeUfly70HJ/6xrKYNqGH1SU70n8/FPHxsmXDOMmYa8gcBVbVOKTqUO++LHGGKAUXK7c67mXoC8XHbe',
    'AWSALBCORS': 'VrEekVZIeFU1pnmxxs4X8u0b5oJKqmMYLKvw+DFxh4WuXmDeUfly70HJ/6xrKYNqGH1SU70n8/FPHxsmXDOMmYa8gcBVbVOKTqUO++LHGGKAUXK7c67mXoC8XHbe'
}

# Common headers
COMMON_HEADERS = {}
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://drill.gghc.com/rcp.html',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

# Create MCP server instance
server = Server("rcp-api-server")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools for the MCP server."""
    return [
        types.Tool(
            name="get_payment_requests",
            description="Fetch payment requests for a specific employee and period",
            inputSchema={
                "type": "object",
                "properties": {
                    "emp_id": {
                        "type": "integer",
                        "description": "Employee ID",
                        "default": 73
                    },
                    "period_id": {
                        "type": "integer", 
                        "description": "Period ID (format: YYYYMM)",
                        "default": 202506
                    }
                },
                "required": ["emp_id", "period_id"]
            }
        ),
        types.Tool(
            name="update_payment_request",
            description="Update a payment request with approval/rejection status",
            inputSchema={
                "type": "object",
                "properties": {
                    "emp_id": {
                        "type": "integer",
                        "description": "Employee ID",
                        "default": 73
                    },
                    "request_id": {
                        "type": "integer",
                        "description": "Payment request ID"
                    },
                    "split": {
                        "type": "number",
                        "description": "Split percentage (0.0 to 1.0)",
                        "default": 0.1
                    },
                    "producer_approved": {
                        "type": "boolean",
                        "description": "Producer approval status",
                        "default": True
                    },
                    "producer_rejected": {
                        "type": "boolean",
                        "description": "Producer rejection status",
                        "default": False
                    }
                },
                "required": ["emp_id", "request_id"]
            }
        ),
        types.Tool(
            name="get_payments_ytd",
            description="Fetch year-to-date payments for a specific employee and period",
            inputSchema={
                "type": "object",
                "properties": {
                    "emp_id": {
                        "type": "integer",
                        "description": "Employee ID",
                        "default": 73
                    },
                    "period_id": {
                        "type": "integer",
                        "description": "Period ID (format: YYYYMM)",
                        "default": 202506
                    }
                },
                "required": ["emp_id", "period_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls from Claude Desktop."""
    
    if name == "get_payment_requests":
        emp_id = arguments.get("emp_id", 73)
        period_id = arguments.get("period_id", 202506)
        
        try:
            url = 'https://drill.gghc.com/extras/api/rcp/get-payment-requests.aspx'
            params = {
                'emp_id': emp_id,
                'period_id': period_id
            }
            
            response = requests.get(
                url,
                params=params,
                headers=COMMON_HEADERS,
                cookies=SESSION_COOKIES,
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            return [types.TextContent(
                type="text",
                text=f"Payment requests for employee {emp_id}, period {period_id}:\n{json.dumps(data, indent=2)}"
            )]
            
        except Exception as e:
            logger.error(f"Error fetching payment requests: {e}")
            return [types.TextContent(
                type="text",
                text=f"Error fetching payment requests: {str(e)}"
            )]
    
    elif name == "update_payment_request":
        emp_id = arguments.get("emp_id", 73)
        request_id = arguments["request_id"]
        split = arguments.get("split", 0.1)
        producer_approved = arguments.get("producer_approved", True)
        producer_rejected = arguments.get("producer_rejected", False)
        
        try:
            url = 'https://drill.gghc.com/extras/api/rcp/update-payment-request.aspx'
            params = {
                'emp_id': emp_id,
                'id': request_id,
                'split': split,
                'producerApproved_fl': str(producer_approved).lower(),
                'producerRejected_fl': str(producer_rejected).lower()
            }
            
            post_headers = COMMON_HEADERS.copy()
            post_headers.update({
                'content-length': '0',
                'origin': 'https://drill.gghc.com'
            })
            
            response = requests.post(
                url,
                params=params,
                headers=post_headers,
                cookies=SESSION_COOKIES,
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            return [types.TextContent(
                type="text",
                text=f"Payment request {request_id} updated successfully:\n{json.dumps(data, indent=2)}"
            )]
            
        except Exception as e:
            logger.error(f"Error updating payment request: {e}")
            return [types.TextContent(
                type="text",
                text=f"Error updating payment request: {str(e)}"
            )]
    
    elif name == "get_payments_ytd":
        emp_id = arguments.get("emp_id", 73)
        period_id = arguments.get("period_id", 202506)
        
        try:
            url = 'https://drill.gghc.com/extras/api/rcp/get-payments-ytd.aspx'
            params = {
                'emp_id': emp_id,
                'period_id': period_id
            }
            
            response = requests.get(
                url,
                params=params,
                headers=COMMON_HEADERS,
                cookies=SESSION_COOKIES,
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            return [types.TextContent(
                type="text",
                text=f"YTD payments for employee {emp_id}, period {period_id}:\n{json.dumps(data, indent=2)}"
            )]
            
        except Exception as e:
            logger.error(f"Error fetching YTD payments: {e}")
            return [types.TextContent(
                type="text",
                text=f"Error fetching YTD payments: {str(e)}"
            )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="rcp-api-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
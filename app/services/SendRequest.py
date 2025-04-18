import aiohttp

class RequestClient:
    def __init__(self, base_url: str):
        """Initialize with base URL"""
        self.base_url = base_url

    async def send_request(self, endpoint: str, data: dict):
        """Send POST request asynchronously"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"} 
        
        async with aiohttp.ClientSession() as session:
            try:
                # Send POST request
                async with session.post(url, json=data, headers=headers) as response:
                    response.raise_for_status()  
                    return await response.json()  

            except aiohttp.ClientResponseError as http_error:
                """Handle HTTP errors (non-2xx status)"""
                return {"error": f"HTTP Error occurred: {http_error.status}"}
            except aiohttp.ClientError as req_error:
                """Handle network or request issues"""
                return {"error": f"Request Error occurred: {str(req_error)}"}
            except Exception as e:
                """Handle unexpected errors"""
                return {"error": f"An error occurred: {str(e)}"}


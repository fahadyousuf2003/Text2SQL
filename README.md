## How to Run the Project

## Prerequisites
- Ensure Python is installed on your system.
- Run Command Prompt as Administrator to avoid permission issues.

## Steps to Run

1. **Start the Endpoint**  
   Run the following command to start the `endpoint.py` file:  
   ```bash
   python endpoint.py

2. **Send a POST Request**   
   Use the curl command to send a POST request to the endpoint. Run the following command:
   ```bash
   curl.exe -X POST http://127.0.0.1:5000/ask -H "Content-Type: application/json" -d "{\"question\": \"Count the number of employees\"}"
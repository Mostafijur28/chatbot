from fastapi import FastAPI, Request

app = FastAPI()

# Define the endpoint to receive webhook events
@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    # Process the payload here
    print(payload)
    return {"status": "Received"}

@app.get("/")
async def homepage():
    return {"Message": "Hello"}

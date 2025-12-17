from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.trip import router as trips_router
from routes.client import router as clients_router
from routes.booking import router as bookings_router
from routes.message import router as messages_router
from routes.messnger_webhooks import router as messages_webhooks_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)

app.include_router(trips_router)
app.include_router(clients_router)
app.include_router(bookings_router)
app.include_router(messages_router)
app.include_router(messages_webhooks_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

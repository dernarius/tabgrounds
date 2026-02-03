from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List
from tabgrounds.game import game_manager
from tabgrounds.schemas import AdvanceResult

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tabgrounds")

app = FastAPI(title="Tabgrounds Backend")

# Allow CORS for potential frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        # Iterate over a copy to avoid modification issues during iteration if disconnect happens
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                # Potentially remove bad connection?
                # For now let disconnect handle it


manager = ConnectionManager()


@app.get("/")
async def read_root():
    """Health check and status endpoint."""
    return {"status": "ok", "game_status": await game_manager.get_status()}


@app.post("/advance", response_model=AdvanceResult)
async def advance_game():
    """Attempts to advance the game to the next stage."""
    result = await game_manager.advance_challenge()

    if result.new_state:
        # Broadcast update to all connected clients
        # Use model_dump_json() or dict for websocket broadcasting
        await manager.broadcast(
            {"type": "GAME_UPDATE", "payload": result.new_state.model_dump()}
        )

    return result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time game state updates."""
    await manager.connect(websocket)
    try:
        # Send initial state
        status = await game_manager.get_status()
        await websocket.send_json(
            {"type": "INITIAL_STATE", "payload": status.model_dump()}
        )
        while True:
            # Keep connection alive, listen for messages (optional client actions)
            data = await websocket.receive_text()
            logger.info(f"Received message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

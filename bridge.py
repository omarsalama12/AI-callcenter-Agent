"""
PersonaPlex WebSocket Bridge
Connects the voice layer to the orchestration layer.
"""
import json
import logging
import websockets

logger = logging.getLogger(__name__)

class PersonaPlexBridge:
    def __init__(self, persona_url="wss://localhost:8998/api/ws"):
        self.persona_url = persona_url
        self.orchestrator_callback = None

    async def connect(self, client_id, persona_prompt, voice="NATM1"):
        async with websockets.connect(self.persona_url) as ws:
            await ws.send(json.dumps({
                "type": "init",
                "role_prompt": persona_prompt,
                "voice": voice,
                "client_id": client_id
            }))
            async for raw in ws:
                data = json.loads(raw)
                if data["type"] == "transcript" and self.orchestrator_callback:
                    if not data.get("is_partial", False):
                        response = await self.orchestrator_callback(
                            client_id=client_id, user_text=data["text"])
                        await ws.send(json.dumps({"type": "response", "text": response}))
                elif data["type"] == "partial_transcript" and self.orchestrator_callback:
                    await self.orchestrator_callback(
                        client_id=client_id, user_text=data["text"], is_partial=True)

    async def stream_response(self, ws, sentences):
        for i, sentence in enumerate(sentences):
            await ws.send(json.dumps({
                "type": "stream_text",
                "text": sentence,
                "is_final": i == len(sentences) - 1
            }))

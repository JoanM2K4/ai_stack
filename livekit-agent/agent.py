import os
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io, mcp
from livekit.plugins import noise_cancellation,google
from prompts import SESSION_INSTRUCTION, AGENT_INSTRUCTION

load_dotenv(".env")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION)

server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(

    #Eleccion de modelo de google
    llm=google.realtime.RealtimeModel(
            ##Seccion en donde se elige la voz del modelo de google e instrucciones que debe tener EVI(la IA)
            voice="Sulafat",
            temperature=0.8,
            instructions=AGENT_INSTRUCTION,
            name="call-center",
            identity="call-center"
        ),
    mcp_servers=[
        mcp.MCPServerHTTP(
            url=os.environ["N8N_MCP_URL"],
            headers={
                "Authorization": f"Bearer {os.environ['N8N_MCP_TOKEN']}"
            }
        )
    ]
    )
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP else noise_cancellation.BVC()
            ),
        ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
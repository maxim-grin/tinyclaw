import asyncio
import logging
import os
from dotenv import load_dotenv

from memory_store import Memory
from session_manager import SessionManager
from skill_loader import SkillLoader
from agent_runtime import AgentRuntime
from telegram_channel import TelegramChannel
from model_providers import create_provider_from_env

# Load environment variables
load_dotenv()

def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

async def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("TinyClaw starting up...")

    # Create the Memory store
    memory = Memory()

    # Create the Session manager 
    sessions = SessionManager()

    # Load all Skills
    skills = SkillLoader()
    skills.load_from_directory(os.path.join(os.path.dirname(__file__), "skills"))

    # Create the configured model provider and agent runtime
    provider = create_provider_from_env()
    logger.info("Using model: %s", provider.display_name)
    agent = AgentRuntime(
        provider = provider,
        skills = skills,
        memory = memory,
    )

    # Create the Telegram channel and connect it to the LLM agent and sessions
    telegram = TelegramChannel(
        token = os.getenv("TELEGRAM_BOT_TOKEN"),
        agent = agent,
        sessions = sessions,
    )

    logger.info("TinyClaw is running on Telegram")
    logger.info("Go Claw!!!🦞")

    # Start the Telegram bot 
    await telegram.start()

def cli():
    asyncio.run(main())

if __name__ == "__main__":
    cli()

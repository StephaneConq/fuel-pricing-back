from dotenv import load_dotenv

ENV = "local"

load_dotenv(dotenv_path=f".env.{ENV}")

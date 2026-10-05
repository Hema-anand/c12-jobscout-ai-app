import os

os.environ["DATABASE_URL"] = "sqlite:///./data/test_jobscout.db"
os.environ["LLM_PROVIDER"] = "mock"
os.environ["MESSAGING_ENABLED"] = "false"

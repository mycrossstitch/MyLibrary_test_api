import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv(
    "API_HOST", "http://127.0.0.1:8000"
)  # if os.environ["STAGE"] == "qa" else ""


# Если используется API_TOKEN
# @pytest.fixture(autouse=True, scope="session")
def init_environment():
    response = requests.post(
        url=f"{HOST}/setup",
        headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
    )

    assert response.status_code == 205

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient


from app.presentation.api.v1.main import app as fastapi_app



@pytest.mark.usefixtures(
    "override_get_db"
)
def test_lifespan_startup_calls_init_db(mocker):
    """
    Verify that the init_db function is called during application startup
    when the TestClient is initialized.
    """

    mock_init_db = mocker.patch("app.presentation.api.v1.lifespan.init_db")
    mock_session_local = MagicMock()
    mock_session_instance = MagicMock()
    mock_session_instance.close = MagicMock()
    mock_session_local.return_value = mock_session_instance
    mocker.patch(
        "app.presentation.api.v1.lifespan.SessionLocal", return_value=mock_session_local
    )

    try:
        with TestClient(fastapi_app) as client:
            mock_init_db.assert_called_once()

    finally:
        pass

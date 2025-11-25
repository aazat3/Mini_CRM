import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.usefixtures("async_client")
@pytest.mark.asyncio
class TestFastAPI():
   source_id: int 

   async def test_create_operator(self, async_client: AsyncClient):
      resp = await async_client.post("/operators/", json={"name": "Operator1", "leads_limit": 5, "is_active": True})
      assert resp.status_code == 201
      data = resp.json()
      assert data["name"] == "Operator1"
      assert data["leads_limit"] == 5
      assert data["is_active"] is True

   async def test_create_source(self, async_client: AsyncClient):
      resp = await async_client.post("/sources/", json={"name": "BotA"})
      assert resp.status_code == 200
      data = resp.json()
      assert data["name"] == "BotA"
      TestFastAPI.source_id = data["id"]

   async def test_set_operator_weight(self, async_client: AsyncClient):
      resp = await async_client.post(f"/sources/{TestFastAPI.source_id}/weights",
                           json={"operator_id": 1, "source_id": TestFastAPI.source_id, "weight": 10})
      assert resp.status_code == 200
      assert resp.json()["weight"] == 10

   async def test_create_contact_with_operator(self, async_client: AsyncClient):
      resp = await async_client.post("/contacts/", json={
            "external_lead_id": "123",
            "source_id": TestFastAPI.source_id,
            "message": "Test message"
      })
      assert resp.status_code == 200
      data = resp.json()
      assert data["external_lead_id"] is not None
      assert data["operator_id"] is not None
      assert data["message"] == "Test message"

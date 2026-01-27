from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_chat_success(client: AsyncClient):
    data = {"title": "My Test Chat"}
    
    response = await client.post("/chats/", json=data)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["title"] == "My Test Chat"
    assert "id" in json_data


@pytest.mark.asyncio
async def test_create_chat_fail(client: AsyncClient):
    data = {"title": ""}
    
    response = await client.post("/chats/", json=data)
    assert response.status_code == 422
    
    json_data = response.json()
    assert json_data["detail"][0]["msg"] == "String should have at least 1 character"


@pytest.mark.asyncio
async def test_send_message_success(client: AsyncClient):
    data_chat = {"title": "My Test Chat"}
    response_chat = await client.post("/chats/", json=data_chat)
    chat_data = response_chat.json()
    chat_id = chat_data["id"]

    data = {"text": "Hello World"}
    response = await client.post(f"/chats/{chat_id}/messages/", json=data)
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["text"] == "Hello World"


@pytest.mark.asyncio
async def test_send_message_fail(client: AsyncClient):
    response = await client.post("/chats/1/messages/", json={"text": ""})
    
    assert response.status_code == 422
    json_data = response.json()
    assert json_data["detail"][0]["msg"] == "String should have at least 1 character"


@pytest.mark.asyncio
async def test_get_messages_from_chat_success(client: AsyncClient):
    data_chat = {"title": "My Test Chat"}
    response_chat = await client.post("/chats/", json=data_chat)
    chat_data = response_chat.json()
    chat_id = chat_data["id"]

    for i in range(5):
        data = {"text": f"Hello World {i+1}!"}
        response = await client.post(f"/chats/{chat_id}/messages/", json=data)
    
    response = await client.get(f"/chats/{chat_id}")
    assert response.status_code == 200

    json_data = response.json()
    assert len(json_data["messages"]) == 5
    assert json_data["messages"][0]["text"] == "Hello World 1!"


@pytest.mark.asyncio
async def test_delete_chat_success(client: AsyncClient):
    data_chat = {"title": "My Test Chat"}
    response_chat = await client.post("/chats/", json=data_chat)
    chat_id = response_chat.json()["id"]

    response = await client.delete(f"/chats/{chat_id}")
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["success"] == True


@pytest.mark.asyncio
async def test_delete_nonexistent_chat(client: AsyncClient):
    response = await client.delete("/chats/99999")
    assert response.status_code == 500

    json_data = response.json()
    assert json_data["detail"] == "404: Chat not found"


@pytest.mark.asyncio
async def test_get_messages_from_chat_fail(client: AsyncClient):
    response = await client.get(f"/chats/99999")
    assert response.status_code == 500

    json_data = response.json()
    assert json_data["detail"] == "404: Chat not found"

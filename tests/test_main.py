"""
Test suite for the /players/ API endpoints.

Covers:
- GET    /health/
- GET    /players/
- GET    /players/{player_id}
- GET    /players/squadnumber/{squad_number}
- POST   /players/
- PUT    /players/squadnumber/{squad_number}
- DELETE /players/squadnumber/{squad_number}

Validates:
- Status codes, response bodies, headers (e.g., X-Cache)
- Handling of existing, nonexistent, and malformed requests
- Conflict and edge case behaviors
"""

from uuid import UUID

from tests.player_fake import (
    existing_player,
    nonexistent_player,
    unknown_player,
)

PATH = "/players/"


def _is_valid_uuid(value: str) -> bool:
    """Return True if value is a well-formed UUID string, False otherwise."""
    try:
        UUID(value)
        return True
    except ValueError:
        return False


# GET /health/ -----------------------------------------------------------------


def test_request_get_health_response_status_ok(client):
    """GET /health/ returns 200 OK"""
    # Act
    response = client.get("/health/")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# GET /players/ ----------------------------------------------------------------


def test_request_get_players_response_header_cache_miss(client):
    """GET /players/ initial request returns X-Cache: MISS"""
    # Act
    response = client.get(PATH)
    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "MISS"


def test_request_get_players_response_header_cache_hit(client):
    """GET /players/ subsequent request returns X-Cache: HIT"""
    # Act
    client.get(PATH)  # initial
    response = client.get(PATH)  # subsequent (cached)
    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "HIT"


def test_request_get_players_response_status_ok(client):
    """GET /players/ returns 200 OK"""
    # Act
    response = client.get(PATH)
    # Assert
    assert response.status_code == 200


def test_request_get_players_response_body_each_player_has_uuid(client):
    """GET /players/ returns players each containing a UUID id field"""
    # Act
    response = client.get(PATH)
    # Assert
    players = response.json()
    assert all(
        _is_valid_uuid(player["id"]) for player in players
    )  # UUID v5 (migration-seeded)


# GET /players/{player_id} -----------------------------------------------------


def test_request_get_player_id_unknown_response_status_not_found(client):
    """GET /players/{player_id} with unknown UUID returns 404 Not Found"""
    # Arrange
    player_id = unknown_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 404


def test_request_get_player_id_existing_response_status_ok(client):
    """GET /players/{player_id} with existing ID returns 200 OK"""
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 200


def test_request_get_player_id_existing_response_body_player_match(client):
    """GET /players/{player_id} with existing ID returns matching player"""
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    player = response.json()
    assert player["id"] == str(player_id)


# GET /players/squadnumber/{squad_number} --------------------------------------


def test_request_get_player_squadnumber_nonexistent_response_status_not_found(client):
    """GET /players/squadnumber/{squad_number} with nonexistent number returns 404 Not Found"""
    # Arrange
    squad_number = nonexistent_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 404


def test_request_get_player_squadnumber_existing_response_status_ok(client):
    """GET /players/squadnumber/{squad_number} with existing number returns 200 OK"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 200


def test_request_get_player_squadnumber_existing_response_body_player_match(client):
    """GET /players/squadnumber/{squad_number} with existing number returns matching player"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    player = response.json()
    assert player["squadNumber"] == squad_number


# POST /players/ ---------------------------------------------------------------


def test_request_post_player_body_empty_response_status_unprocessable(client):
    """POST /players/ with empty body returns 422 Unprocessable Entity"""
    # Act
    response = client.post(PATH, json={})
    # Assert
    assert response.status_code == 422


def test_request_post_player_body_existing_response_status_conflict(client):
    """POST /players/ with existing player returns 409 Conflict"""
    # Arrange
    player = existing_player()
    # Act
    response = client.post(PATH, json=player.__dict__)
    # Assert
    assert response.status_code == 409


def test_request_post_player_body_existing_response_body_detail(client):
    """POST /players/ with existing player returns 409 with detail message"""
    # Arrange
    player = existing_player()
    # Act
    response = client.post(PATH, json=player.__dict__)
    # Assert
    assert (
        response.json()["detail"] == "A Player with this squad number already exists."
    )


def test_request_post_player_body_nonexistent_response_status_created(client):
    """POST /players/ with nonexistent player returns 201 Created with a valid UUID"""
    # Arrange
    player = nonexistent_player()
    try:
        # Act
        response = client.post(PATH, json=player.__dict__)
        # Assert
        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert UUID(body["id"]).version == 4  # UUID v4 (API-created)
    finally:
        # Teardown — remove the created player
        client.delete(PATH + "squadnumber/" + str(player.squad_number))


# PUT /players/squadnumber/{squad_number} --------------------------------------


def test_request_put_player_squadnumber_existing_body_empty_response_status_unprocessable(
    client,
):
    """PUT /players/squadnumber/{squad_number} with empty body returns 422 Unprocessable Entity"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.put(PATH + "squadnumber/" + str(squad_number), json={})
    # Assert
    assert response.status_code == 422


def test_request_put_player_squadnumber_unknown_response_status_not_found(client):
    """PUT /players/squadnumber/{squad_number} with unknown number returns 404 Not Found"""
    # Arrange
    squad_number = unknown_player().squad_number
    player = unknown_player()
    # Act
    response = client.put(
        PATH + "squadnumber/" + str(squad_number), json=player.__dict__
    )
    # Assert
    assert response.status_code == 404


def test_request_put_player_squadnumber_existing_response_status_no_content(client):
    """PUT /players/squadnumber/{squad_number} with existing number returns 204 No Content"""
    # Arrange
    squad_number = existing_player().squad_number
    player = existing_player()
    player.first_name = "Emiliano"
    player.middle_name = None
    try:
        # Act
        response = client.put(
            PATH + "squadnumber/" + str(squad_number), json=player.__dict__
        )
        # Assert
        assert response.status_code == 204
    finally:
        # Teardown — restore Damián Martínez to its seeded state
        seed = existing_player()
        client.put(PATH + "squadnumber/" + str(seed.squad_number), json=seed.__dict__)


def test_request_put_player_squadnumber_mismatch_response_status_bad_request(client):
    """PUT /players/squadnumber/{squad_number} with mismatched squad number in body returns 400 Bad Request"""
    # Arrange
    squad_number = existing_player().squad_number
    player = existing_player()
    player.squad_number = unknown_player().squad_number
    # Act
    response = client.put(
        PATH + "squadnumber/" + str(squad_number), json=player.__dict__
    )
    # Assert
    assert response.status_code == 400


# DELETE /players/squadnumber/{squad_number} -----------------------------------


def test_request_delete_player_squadnumber_unknown_response_status_not_found(client):
    """DELETE /players/squadnumber/{squad_number} with unknown number returns 404 Not Found"""
    # Arrange
    squad_number = unknown_player().squad_number
    # Act
    response = client.delete(PATH + "squadnumber/" + str(squad_number))
    # Assert
    assert response.status_code == 404


def test_request_delete_player_squadnumber_existing_response_status_no_content(
    client, nonexistent_player_in_db
):
    """DELETE /players/squadnumber/{squad_number} with existing number returns 204 No Content"""
    # Arrange
    player = nonexistent_player_in_db
    # Act
    response = client.delete(PATH + "squadnumber/" + str(player.squad_number))
    # Assert
    assert response.status_code == 204


def test_request_post_player_body_nonexistent_response_header_location(client):
    """POST /players/ with nonexistent player returns 201 with Location header"""
    # Arrange
    player = nonexistent_player()
    try:
        # Act
        response = client.post(PATH, json=player.__dict__)
        # Assert
        assert response.status_code == 201
        assert "Location" in response.headers
        assert (
            response.headers["Location"]
            == f"/players/squadnumber/{player.squad_number}"
        )
    finally:
        client.delete(PATH + "squadnumber/" + str(player.squad_number))


# GET /players/?page=&size= -----------------------------------------------------


def test_request_get_players_ac1_response_ten_players(client):
    # Arrange
    params = {"page": 1, "size": 10}
    # Act
    response = client.get(PATH, params=params)
    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_request_get_players_ac2_response_complete_order(client):
    # Arrange
    complete = client.get(PATH).json()
    # Act
    pages = [client.get(PATH, params={"page": p, "size": 10}) for p in (1, 2, 3)]
    combined = [player for response in pages for player in response.json()]
    # Assert
    assert all(response.status_code == 200 for response in pages)
    assert combined == complete
    assert len({player["id"] for player in combined}) == 26


def test_request_get_players_ac3_response_last_and_empty_pages(client):
    # Arrange
    complete = client.get(PATH).json()
    # Act
    last = client.get(PATH, params={"page": 3, "size": 10})
    beyond = client.get(PATH, params={"page": 4, "size": 10})
    # Assert
    assert last.status_code == beyond.status_code == 200
    assert len(last.json()) == 6
    assert last.json() == complete[20:]
    assert beyond.json() == []


def test_request_get_players_ac4_response_default_parameters(client):
    # Arrange
    complete = client.get(PATH).json()
    # Act
    page_only = client.get(PATH, params={"page": 2})
    size_only = client.get(PATH, params={"size": 10})
    # Assert
    assert page_only.status_code == size_only.status_code == 200
    assert page_only.json() == complete[20:26]
    assert size_only.json() == complete[:10]


def test_request_get_players_ac5_response_unprocessable(client):
    # Arrange
    invalid = ["size=0", "size=101", "size=abc", "page=0", "page=-1"]
    # Act
    responses = [client.get(PATH + "?" + query) for query in invalid]
    # Assert
    assert all(response.status_code == 422 for response in responses)


def test_request_get_players_ac6_response_isolated_cache(client):
    # Arrange
    from routes.player_route import CACHE_KEY, simple_memory_cache

    client.portal.call(simple_memory_cache.clear, CACHE_KEY)
    complete = client.get(PATH).json()
    # Act
    first = client.get(PATH, params={"page": 1, "size": 10})
    second = client.get(PATH, params={"page": 2, "size": 10})
    first_hit = client.get(PATH, params={"page": 1, "size": 10})
    second_hit = client.get(PATH, params={"page": 2, "size": 10})
    full = client.get(PATH)
    # Assert
    assert first.status_code == second.status_code == full.status_code == 200
    assert first.json() == complete[:10]
    assert second.json() == complete[10:20]
    assert {p["id"] for p in first.json()}.isdisjoint(p["id"] for p in second.json())
    assert first.headers["X-Cache"] == second.headers["X-Cache"] == "MISS"
    assert first_hit.headers["X-Cache"] == second_hit.headers["X-Cache"] == "HIT"
    assert first_hit.json() == first.json()
    assert second_hit.json() == second.json()
    assert len(full.json()) == 26
    assert full.json() == complete


def test_request_get_players_ac7_response_unchanged_full_list(client):
    # Arrange
    from routes.player_route import CACHE_KEY, simple_memory_cache

    client.portal.call(simple_memory_cache.clear, CACHE_KEY)
    # Act
    miss = client.get(PATH)
    hit = client.get(PATH)
    # Assert
    assert miss.status_code == hit.status_code == 200
    assert len(miss.json()) == 26
    assert miss.json() == hit.json()
    assert miss.headers["X-Cache"] == "MISS"
    assert hit.headers["X-Cache"] == "HIT"


def test_request_get_players_ac8_response_page_cache_cleared_after_write(client):
    # Arrange
    player = nonexistent_player()
    params = {"page": 2, "size": 20}
    try:
        before = client.get(PATH, params=params)
        assert before.status_code == 200
        assert len(before.json()) == 6
        # Act
        created = client.post(PATH, json=player.__dict__)
        after = client.get(PATH, params=params)
        # Assert
        assert created.status_code == 201
        assert after.status_code == 200
        assert len(after.json()) == 7
        assert created.json() in after.json()
        assert after.headers["X-Cache"] == "MISS"
    finally:
        client.delete(PATH + "squadnumber/" + str(player.squad_number))


# GET /players/count -----------------------------------------------------------


def test_request_get_players_count_seeded_response_count(client):
    # Arrange
    expected = {"count": 26}
    # Act
    response = client.get(PATH + "count")
    # Assert
    assert response.status_code == 200
    assert response.json() == expected


def test_request_get_players_count_writes_response_updated_count(client):
    # Arrange
    player = nonexistent_player()
    before = client.get(PATH + "count")
    try:
        assert client.post(PATH, json=player.__dict__).status_code == 201
        # Act
        after_create = client.get(PATH + "count")
        deleted = client.delete(PATH + "squadnumber/" + str(player.squad_number))
        after_delete = client.get(PATH + "count")
        # Assert
        assert before.status_code == after_create.status_code == 200
        assert after_delete.status_code == 200
        assert before.json() == after_delete.json() == {"count": 26}
        assert after_create.json() == {"count": 27}
        assert deleted.status_code == 204
    finally:
        client.delete(PATH + "squadnumber/" + str(player.squad_number))


def test_request_get_players_count_empty_response_zero(client):
    # Arrange
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    from databases.player_database import Base, generate_async_session
    from main import app

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async def create_tables():
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def empty_session():
        async with AsyncSession(engine) as session:
            yield session

    client.portal.call(create_tables)
    app.dependency_overrides[generate_async_session] = empty_session
    try:
        # Act
        response = client.get(PATH + "count")
        # Assert
        assert response.status_code == 200
        assert response.json() == {"count": 0}
    finally:
        app.dependency_overrides.pop(generate_async_session)
        client.portal.call(engine.dispose)

from fastapi.testclient import TestClient

from app.server.app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_read_all_shops():
    with client:
        response = client.get("/shops")
        assert response.status_code == 200


def test_read_shop_by_id():
    with client:
        all_shops = client.get("/shops")
        sample_shop = all_shops.json()[0]
        sample_shop_id = sample_shop["_id"]
        found_shop_resp = client.get(f"/shops/{sample_shop_id}")
        assert found_shop_resp.status_code == 200
        assert found_shop_resp.json() == sample_shop


def test_read_shops_by_distance():
    with client:
        response = client.post(
            "/shops/by_distance",
            json={
                "lat": 50.086776271666096,
                "lng": 19.915122985839847,
                "radius": 1000,
            },
        )
        assert response.status_code == 200
        assert len(response.json()) > 0


def test_read_shops_by_number():
    with client:
        response = client.post(
            "/shops/by_number",
            json={
                "lat": 50.086776271666096,
                "lng": 19.915122985839847,
                "n_closest": 5,
            },
        )
        assert response.status_code == 200
        assert len(response.json()) <= 5

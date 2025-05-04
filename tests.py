import pytest 
from fastapi.testclient import TestClient
from main import app


#integration test
client = TestClient(app)
def test_post_and_delete_swift_code():
    new_code = {
        "address": "123 Test St",
        "townName": "TESTVILLE",
        "bankName": "Test Bank",
        "countryISO2": "ZZ",
        "countryName": "TESTLAND",
        "isHeadquarter": True,
        "swiftCode": "ZZZZTESTXXX"
    }

    post_response = client.post("/v1/swift-codes", json=new_code)
    assert post_response.status_code == 200

    get_response = client.get("/v1/swift-codes/ZZZZTESTXXX")
    assert get_response.status_code == 200
    assert get_response.json()["swiftCode"] == "ZZZZTESTXXX"

    del_response = client.delete("/v1/swift-codes/ZZZZTESTXXX") 
    assert del_response.status_code == 200

    get_again = client.get("/v1/swift-codes/ZZZZTESTXXX")
    assert get_again.status_code == 404

#unit tests

def is_headquarter(swift_code: str) -> bool:
    return swift_code.endswith("XXX")


def test_is_headquarter_true():
    assert is_headquarter("ABCDEF12XXX") is True

def test_is_headquarter_false():
    assert is_headquarter("ABCDEF12001") is False


def test_post_missing_field():
    bad_code = {
        "address": "No Town",
        "bankName": "Bank",
        "countryISO2": "XX",
        "countryName": "NOWHERE",
        "codeType": "BIC11",
        "timeZone": "Europe/Test",
        "isHeadquarter": True,
        "swiftCode": "NOMISSINGXXX"
        # brak "townName"
    }
    response = client.post("/v1/swift-codes", json=bad_code)
    assert response.status_code == 422

def test_post_duplicate_swift_code():
    new_code = {
        "address": "Dup St",
        "townName": "DUPVILLE",
        "bankName": "Dup Bank",
        "countryISO2": "DP",
        "countryName": "DUPLICATIA",
        "codeType": "BIC11",
        "timeZone": "Europe/Dup",
        "isHeadquarter": True,
        "swiftCode": "DUPLICATEXXX"
    }

    client.post("/v1/swift-codes", json=new_code)
    duplicate_response = client.post("/v1/swift-codes", json=new_code)
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"]

    client.delete("/v1/swift-codes/DUPLICATEXXX")

def test_get_nonexistent_code():
    response = client.get("/v1/swift-codes/NONEXIST123")
    assert response.status_code == 404

def test_delete_nonexistent_code():
    response = client.delete("/v1/swift-codes/NOTREAL123")
    assert response.status_code == 404
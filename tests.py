import pytest 
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_swift_payload(swift_code: str, is_headquarter=True):
    return {
        "address": "Test Address",
        "bankName": "Test Bank",
        "countryISO2": "ZZ",
        "countryName": "TESTLAND",
        "isHeadquarter": is_headquarter,
        "swiftCode": swift_code
    }

#testy jednostkowe

def is_headquarter(swift_code: str) -> bool:
    return swift_code.endswith("XXX")

def test_is_headquarter_true():
    assert is_headquarter("ABCDEF12XXX") is True

def test_is_headquarter_false():
    assert is_headquarter("ABCDEF12001") is False

def test_is_headquarter_false_with_branch_code():
    assert is_headquarter("AAAAUS33ABC") is False

def test_is_headquarter_with_short_code():
    assert is_headquarter("XXX") is True

def test_is_headquarter_empty_string():
    assert is_headquarter("") is False

def test_is_headquarter_non_swift_format():
    assert is_headquarter("HELLO") is False


#testy integracyjne

def test_POST_GET_DELETE():
    code = "ZZZZTESTXXX"
    payload = create_swift_payload(code)

    post_response = client.post("/v1/swift-codes", json=payload)
    assert post_response.status_code == 200
    assert post_response.json()["message"] == "SWIFT code added successfully"

    get_response = client.get(f"/v1/swift-codes/{code}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["swiftCode"] == code
    assert data["isHeadquarter"] is True

    del_response = client.delete(f"/v1/swift-codes/{code}")
    assert del_response.status_code == 200
    assert del_response.json()["message"] == "SWIFT code deleted successfully"

    get_again = client.get(f"/v1/swift-codes/{code}")
    assert get_again.status_code == 404

def test_POST_missing_townName():
    #townName to pusty string -> test powinien przejsc
    payload = create_swift_payload("MISSINGTOWNXXX")
    payload.pop("address") 

    response = client.post("/v1/swift-codes", json=payload)
    assert response.status_code == 422

def test_POST_duplicate_swift_code():
    code = "DUPLICATEXXX"
    payload = create_swift_payload(code)

    #1 wstawienie
    response1 = client.post("/v1/swift-codes", json=payload)
    assert response1.status_code == 200

    # 2 wstawienie
    response2 = client.post("/v1/swift-codes", json=payload)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

    client.delete(f"/v1/swift-codes/{code}")

def test_GET_nonexistent_swift_code():
    response = client.get("/v1/swift-codes/DOESNOTEXIST")
    assert response.status_code == 404

def test_DELETE_nonexistent_swift_code():
    response = client.delete("/v1/swift-codes/FAKECODE123")
    assert response.status_code == 404

def test_GET_by_country():
    #wstawienie 2 rekordow
    code1 = "COUNTRYTST1X"
    code2 = "COUNTRYTST2X"
    payload1 = create_swift_payload(code1)
    payload2 = create_swift_payload(code2, is_headquarter=False)

    client.post("/v1/swift-codes", json=payload1)
    client.post("/v1/swift-codes", json=payload2)

    response = client.get("/v1/swift-codes/country/ZZ")
    assert response.status_code == 200
    data = response.json()
    assert data["countryISO2"] == "ZZ"
    assert len(data["swiftCodes"]) >= 2

    client.delete(f"/v1/swift-codes/{code1}")
    client.delete(f"/v1/swift-codes/{code2}")
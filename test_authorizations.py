#!/usr/bin/env python3
"""
Test cases for the simple OPA example rules
"""
import requests
import json

OPEN_DATASETS = ["open1", "open2", "open3"]
REGISTERED_DATASETS = ["registered1"]
ALICE_CONTROLLED = ["controlled1"]
BOB_CONTROLLED = ["controlled2"]
CHARLIE_CONTROLLED = []

URL = "http://localhost:8181/v1/data/permissions/allowed"

def make_opa_request_for_service(user_token, service="beacon"):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    input = {"method": "GET", "path": [service]}
    if user_token:
       input["user"] = user_token

    response = requests.post(URL, json={"input": input}, headers=headers)
    json_response = response.json()

    assert("result" in json_response)

    return json_response["result"]


def test_unauthenticated():
    assert make_opa_request_for_service(None) == OPEN_DATASETS

def test_other_service():
    assert make_opa_request_for_service(None, service="WES") == []

def authenticated_request(tokenfilename, expected):
    with open(tokenfilename, "r") as tokenfile:
        token = tokenfile.read()

    result = make_opa_request_for_service(token)
    assert set(result) == set(expected)
   
def test_alice():
    expected = OPEN_DATASETS + REGISTERED_DATASETS + ALICE_CONTROLLED
    authenticated_request("crypto/alice_id.jwt", expected)

def test_expired_alice():
    expected = OPEN_DATASETS
    authenticated_request("crypto/alice_expired_id.jwt", expected)

def test_bob():
    expected = OPEN_DATASETS + REGISTERED_DATASETS + BOB_CONTROLLED
    authenticated_request("crypto/bob_id.jwt", expected)

def test_charlie():
    expected = OPEN_DATASETS + REGISTERED_DATASETS + CHARLIE_CONTROLLED
    authenticated_request("crypto/charlie_id.jwt", expected)
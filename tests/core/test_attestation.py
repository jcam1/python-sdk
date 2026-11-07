import base64

import pytest

pytest.importorskip("dilithium_py")

from packages.core.jpyc_core_sdk import attestation  # noqa: E402

TRANSFER = {
    "chain_id": 1,
    "operation": "transfer",
    "from": "0xC8CD2BE653759aed7B0996315821AAe71e1FEAdF",
    "to": "0x1111111111111111111111111111111111111111",
    "value": "1000000000000000000",
    "nonce": 7,
}


def test_build_and_verify_roundtrip() -> None:
    payload = attestation.canonicalize(TRANSFER)
    public_key, secret_key = attestation.generate_keypair()
    att = attestation.build_attestation(payload, public_key, secret_key)
    assert att["scheme"] == "ML-DSA-65"
    assert att["issuer"] == "Quantova"
    assert attestation.verify_attestation(payload, att) is True
    assert attestation.verify_attestation(payload, att, public_key) is True


def test_tampered_payload_is_rejected() -> None:
    payload = attestation.canonicalize(TRANSFER)
    public_key, secret_key = attestation.generate_keypair()
    att = attestation.build_attestation(payload, public_key, secret_key)
    altered = attestation.canonicalize({**TRANSFER, "value": "9" * 18})
    assert attestation.verify_attestation(altered, att) is False


def test_wrong_signer_is_rejected_when_pinned() -> None:
    payload = attestation.canonicalize(TRANSFER)
    public_key, secret_key = attestation.generate_keypair()
    other_public_key, _ = attestation.generate_keypair()
    att = attestation.build_attestation(payload, public_key, secret_key)
    assert attestation.verify_attestation(payload, att, other_public_key) is False


def test_forged_signature_is_rejected() -> None:
    payload = attestation.canonicalize(TRANSFER)
    public_key, secret_key = attestation.generate_keypair()
    att = attestation.build_attestation(payload, public_key, secret_key)
    att["signature"] = base64.b64encode(b"\x00" * 64).decode("ascii")
    assert attestation.verify_attestation(payload, att) is False


def test_malformed_field_is_rejected() -> None:
    payload = attestation.canonicalize(TRANSFER)
    public_key, secret_key = attestation.generate_keypair()
    att = attestation.build_attestation(payload, public_key, secret_key)
    att["public_key"] = "!!!not base64!!!"
    assert attestation.verify_attestation(payload, att) is False


def test_canonicalize_is_order_independent() -> None:
    assert attestation.canonicalize({"a": 1, "b": 2}) == attestation.canonicalize(
        {"b": 2, "a": 1}
    )

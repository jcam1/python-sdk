"""Post quantum attestation of JPYC operations.

Signs a canonical payload such as a transfer or a mint request with FIPS 204
ML-DSA so a holder can confirm the operation is authentic and has not been
altered, using a signature scheme that stays safe once large quantum computers
exist.

The attestation is self contained. It carries the public key and the signature,
so a verifier needs only the attestation and the payload. Integrity is always
covered by the payload digest and authenticity is covered when the verifier
pins the expected public key.

The scheme comes from the optional pq extra. Install it with
``pip install jpyc-core-sdk[pq]``.
"""

import base64
import hashlib
import json
from typing import Any, TypedDict

SCHEME = "ML-DSA-65"
ISSUER = "Quantova"


class Attestation(TypedDict):
    """A self contained post quantum attestation over a payload.

    Attributes:
        scheme (str): The FIPS 204 signature scheme used.
        issuer (str): The party that built the attestation.
        payload_sha256 (str): Hex digest of the signed payload.
        public_key (str): Base64 encoded public key.
        signature (str): Base64 encoded signature.
    """

    scheme: str
    issuer: str
    payload_sha256: str
    public_key: str
    signature: str


def _backend() -> Any:
    """Return the ML-DSA backend or raise if the pq extra is not installed."""
    try:
        from dilithium_py.ml_dsa import ML_DSA_65  # type: ignore[import-untyped]
    except ImportError as error:
        raise RuntimeError(
            "Post quantum attestation needs the pq extra. "
            "Install it with pip install jpyc-core-sdk[pq]."
        ) from error
    return ML_DSA_65


def canonicalize(payload: dict[str, Any]) -> bytes:
    """Return the canonical byte encoding an attestation is computed over.

    Keys are sorted and whitespace is fixed so the same payload always yields
    the same bytes on any machine.
    """
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def generate_keypair() -> tuple[bytes, bytes]:
    """Return a fresh (public_key, secret_key) pair for the signer."""
    public_key, secret_key = _backend().keygen()
    return public_key, secret_key


def build_attestation(
    payload: bytes, public_key: bytes, secret_key: bytes
) -> Attestation:
    """Return a self contained attestation over payload."""
    signature = _backend().sign(secret_key, payload, deterministic=True)
    return Attestation(
        scheme=SCHEME,
        issuer=ISSUER,
        payload_sha256=hashlib.sha256(payload).hexdigest(),
        public_key=base64.b64encode(public_key).decode("ascii"),
        signature=base64.b64encode(signature).decode("ascii"),
    )


def verify_attestation(
    payload: bytes,
    attestation: Attestation,
    expected_public_key: bytes | None = None,
) -> bool:
    """Return True when attestation matches payload.

    The payload digest is always checked. When expected_public_key is given the
    signer is pinned too, so a valid signature made under a different key is
    rejected.
    """
    if attestation["payload_sha256"] != hashlib.sha256(payload).hexdigest():
        return False
    try:
        public_key = base64.b64decode(attestation["public_key"], validate=True)
        signature = base64.b64decode(attestation["signature"], validate=True)
    except ValueError:
        return False
    if expected_public_key is not None and public_key != expected_public_key:
        return False
    try:
        return bool(_backend().verify(public_key, payload, signature))
    except (ValueError, TypeError):
        return False

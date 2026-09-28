from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def key_stream(key: bytes, size: int) -> bytes:
    chunks = []
    counter = 0
    while sum(len(chunk) for chunk in chunks) < size:
        counter_bytes = counter.to_bytes(4, "big")
        chunks.append(hmac.new(key, counter_bytes, hashlib.sha256).digest())
        counter += 1
    return b"".join(chunks)[:size]


def xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right))


class KeyVault:
    def __init__(self) -> None:
        self._keys: Dict[str, bytes] = {}

    def create_key(self, passenger_id: str) -> None:
        seed = f"demo-key::{passenger_id}".encode("utf-8")
        self._keys[passenger_id] = hashlib.sha256(seed).digest()

    def destroy_key(self, passenger_id: str) -> None:
        del self._keys[passenger_id]

    def encrypt(self, passenger_id: str, value: str) -> str:
        key = self._keys[passenger_id]
        plain = value.encode("utf-8")
        cipher = xor_bytes(plain, key_stream(key, len(plain)))
        return base64.b64encode(cipher).decode("ascii")

    def decrypt(self, passenger_id: str, token: str) -> Optional[str]:
        key = self._keys.get(passenger_id)
        if key is None:
            return None
        cipher = base64.b64decode(token.encode("ascii"))
        plain = xor_bytes(cipher, key_stream(key, len(cipher)))
        try:
            return plain.decode("utf-8")
        except UnicodeDecodeError:
            return None


@dataclass(frozen=True)
class Event:
    sequence: int
    event_type: str
    occurred_at: str
    payload: dict
    previous_hash: str
    event_hash: str


class EventStore:
    def __init__(self) -> None:
        self._events: List[Event] = []

    def append(self, event_type: str, occurred_at: str, payload: dict) -> Event:
        sequence = len(self._events) + 1
        previous_hash = self._events[-1].event_hash if self._events else "GENESIS"
        body = {
            "sequence": sequence,
            "event_type": event_type,
            "occurred_at": occurred_at,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        event_hash = digest(stable_json(body))
        event = Event(sequence, event_type, occurred_at, payload, previous_hash, event_hash)
        self._events.append(event)
        return event

    def all(self) -> Iterable[Event]:
        return tuple(self._events)

    def verify_chain(self) -> bool:
        previous_hash = "GENESIS"
        for event in self._events:
            body = {
                "sequence": event.sequence,
                "event_type": event.event_type,
                "occurred_at": event.occurred_at,
                "payload": event.payload,
                "previous_hash": previous_hash,
            }
            if event.previous_hash != previous_hash:
                return False
            if event.event_hash != digest(stable_json(body)):
                return False
            previous_hash = event.event_hash
        return True


def pseudonym(passenger_id: str) -> str:
    return digest(f"audit-salt::{passenger_id}")[:16]


def iso(day: str) -> str:
    value = datetime.fromisoformat(f"2026-09-{day}T07:30:00+00:00")
    return value.astimezone(timezone.utc).isoformat()


def append_trip(
    store: EventStore,
    vault: KeyVault,
    passenger_id: str,
    card_id: str,
    counter: int,
    operator: str,
    line: str,
    amount_cents: int,
    day: str,
) -> None:
    store.append(
        "PassagemValidada",
        iso(day),
        {
            "passenger_ref_encrypted": vault.encrypt(passenger_id, passenger_id),
            "card_pseudonym": pseudonym(card_id),
            "transaction_counter": counter,
            "operator": operator,
            "line": line,
            "amount_cents": amount_cents,
        },
    )


def project_operator_totals(events: Iterable[Event]) -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for event in events:
        if event.event_type != "PassagemValidada":
            continue
        operator = event.payload["operator"]
        totals[operator] = totals.get(operator, 0) + event.payload["amount_cents"]
    return dict(sorted(totals.items()))


def find_duplicate_uses(events: Iterable[Event]) -> List[str]:
    seen: Dict[tuple, str] = {}
    duplicates: List[str] = []
    for event in events:
        if event.event_type != "PassagemValidada":
            continue
        key = (event.payload["card_pseudonym"], event.payload["transaction_counter"])
        bus_line = event.payload["line"]
        if key in seen and seen[key] != bus_line:
            duplicates.append(f"{key[0]}#{key[1]} em {seen[key]} e {bus_line}")
        seen[key] = bus_line
    return duplicates


def identify_passenger(store: EventStore, vault: KeyVault, passenger_id: str) -> List[str]:
    identities = []
    for event in store.all():
        encrypted = event.payload.get("passenger_ref_encrypted")
        if not encrypted:
            continue
        identity = vault.decrypt(passenger_id, encrypted)
        if identity is not None:
            identities.append(identity)
    return identities


def main() -> None:
    vault = KeyVault()
    store = EventStore()

    vault.create_key("P-100")
    vault.create_key("P-200")

    append_trip(store, vault, "P-100", "CARD-77", 10, "Operadora Azul", "Linha 332", 550, "10")
    append_trip(store, vault, "P-200", "CARD-88", 5, "Operadora Verde", "Linha 410", 550, "10")
    append_trip(store, vault, "P-100", "CARD-77", 11, "Operadora Azul", "Linha 332", 550, "11")
    append_trip(store, vault, "P-100", "CARD-77", 11, "Operadora Verde", "Linha 115", 550, "11")

    before = identify_passenger(store, vault, "P-100")
    totals_before = project_operator_totals(store.all())
    duplicates = find_duplicate_uses(store.all())

    vault.destroy_key("P-100")
    store.append(
        "ChaveDestruida",
        iso("12"),
        {"passenger_pseudonym": pseudonym("P-100"), "reason": "pedido LGPD validado"},
    )

    after = identify_passenger(store, vault, "P-100")
    totals_after = project_operator_totals(store.all())

    print("cadeia_eventos_valida:", store.verify_chain())
    print("identidades_P-100_antes:", before)
    print("identidades_P-100_depois:", after)
    print("totais_antes:", totals_before)
    print("totais_depois:", totals_after)
    print("duplicidades:", duplicates)
    print("eventos_no_log:", len(tuple(store.all())))


if __name__ == "__main__":
    main()

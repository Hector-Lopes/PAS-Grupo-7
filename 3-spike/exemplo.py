from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Event:
    tenant_id: str
    event_type: str
    payload: dict


@dataclass
class TenantConfig:
    tenant_id: str
    city_name: str
    max_events_per_tick: int
    circuit_breaker_open: bool = False


@dataclass
class TenantCell:
    config: TenantConfig
    queue: List[Event] = field(default_factory=list)
    dead_letters: List[Event] = field(default_factory=list)
    processed: List[Event] = field(default_factory=list)
    operator_totals: Dict[str, int] = field(default_factory=dict)
    duplicate_uses: List[str] = field(default_factory=list)
    _seen_cards: Dict[tuple, str] = field(default_factory=dict)

    def enqueue(self, event: Event) -> None:
        if event.tenant_id != self.config.tenant_id:
            raise ValueError("evento enviado para a celula errada")
        self.queue.append(event)

    def process_tick(self) -> None:
        if self.config.circuit_breaker_open:
            return

        budget = self.config.max_events_per_tick
        batch = self.queue[:budget]
        self.queue = self.queue[budget:]

        for event in batch:
            try:
                self._process(event)
            except ValueError:
                self.dead_letters.append(event)

    def _process(self, event: Event) -> None:
        if event.event_type == "FalhaIntegracaoExterna":
            raise ValueError("integracao externa indisponivel")

        if event.event_type != "PassagemValidada":
            self.processed.append(event)
            return

        operator = event.payload["operator"]
        amount = event.payload["amount_cents"]
        card_key = (event.payload["card_pseudonym"], event.payload["counter"])
        line = event.payload["line"]

        previous_line = self._seen_cards.get(card_key)
        if previous_line is not None and previous_line != line:
            self.duplicate_uses.append(
                f"{event.tenant_id}:{card_key[0]}#{card_key[1]} em {previous_line} e {line}"
            )
        self._seen_cards[card_key] = line
        self.operator_totals[operator] = self.operator_totals.get(operator, 0) + amount
        self.processed.append(event)


class TenantRouter:
    def __init__(self, cells: Dict[str, TenantCell]) -> None:
        self.cells = cells

    def publish(self, event: Event) -> None:
        cell = self.cells[event.tenant_id]
        cell.enqueue(event)


def trip(
    tenant_id: str,
    card: str,
    counter: int,
    operator: str,
    line: str,
    amount_cents: int = 550,
) -> Event:
    return Event(
        tenant_id=tenant_id,
        event_type="PassagemValidada",
        payload={
            "card_pseudonym": card,
            "counter": counter,
            "operator": operator,
            "line": line,
            "amount_cents": amount_cents,
        },
    )


def external_failure(tenant_id: str) -> Event:
    return Event(tenant_id, "FalhaIntegracaoExterna", {"system": "adquirente"})


def run_simulation() -> Dict[str, TenantCell]:
    cells = {
        "campinas": TenantCell(TenantConfig("campinas", "Campinas", max_events_per_tick=3)),
        "valinhos": TenantCell(TenantConfig("valinhos", "Valinhos", max_events_per_tick=2)),
        "sumare": TenantCell(TenantConfig("sumare", "Sumare", max_events_per_tick=1)),
    }
    router = TenantRouter(cells)

    events = [
        trip("campinas", "CAMP-77", 10, "Operadora Azul", "Linha 332"),
        trip("campinas", "CAMP-77", 11, "Operadora Azul", "Linha 332"),
        trip("campinas", "CAMP-77", 11, "Operadora Verde", "Linha 115"),
        trip("campinas", "CAMP-99", 1, "Operadora Azul", "Linha 300"),
        trip("campinas", "CAMP-100", 1, "Operadora Azul", "Linha 301"),
        trip("campinas", "CAMP-101", 1, "Operadora Azul", "Linha 302"),
        trip("campinas", "CAMP-102", 1, "Operadora Azul", "Linha 303"),
        trip("campinas", "CAMP-103", 1, "Operadora Azul", "Linha 304"),
        trip("campinas", "CAMP-104", 1, "Operadora Azul", "Linha 305"),
        trip("campinas", "CAMP-105", 1, "Operadora Azul", "Linha 306"),
        trip("campinas", "CAMP-106", 1, "Operadora Azul", "Linha 307"),
        trip("valinhos", "VAL-1", 1, "Operadora Verde", "Linha 10"),
        trip("valinhos", "VAL-2", 1, "Operadora Verde", "Linha 11"),
        external_failure("valinhos"),
        trip("sumare", "SUM-1", 1, "Operadora Laranja", "Linha 20"),
        trip("sumare", "SUM-2", 1, "Operadora Laranja", "Linha 21"),
    ]

    for event in events:
        router.publish(event)

    for _ in range(3):
        for cell in cells.values():
            cell.process_tick()

    return cells


def describe_cell(cell: TenantCell) -> str:
    totals = dict(sorted(cell.operator_totals.items()))
    return (
        f"{cell.config.tenant_id}: processados={len(cell.processed)}, "
        f"fila={len(cell.queue)}, dead_letters={len(cell.dead_letters)}, "
        f"totais={totals}, duplicidades={cell.duplicate_uses}"
    )


def main() -> None:
    cells = run_simulation()

    print("resultado_por_cidade:")
    for tenant_id in sorted(cells):
        print(describe_cell(cells[tenant_id]))

    campinas_backlog = len(cells["campinas"].queue)
    other_cities_processed = len(cells["valinhos"].processed) + len(cells["sumare"].processed)
    valinhos_failure = len(cells["valinhos"].dead_letters)
    isolated = campinas_backlog > 0 and other_cities_processed == 4 and valinhos_failure == 1

    print("pico_campinas_deixou_backlog:", campinas_backlog)
    print("falha_valinhos_dead_letters:", valinhos_failure)
    print("outras_cidades_continuaram:", other_cities_processed)
    print("isolamento_comprovado:", isolated)


if __name__ == "__main__":
    main()

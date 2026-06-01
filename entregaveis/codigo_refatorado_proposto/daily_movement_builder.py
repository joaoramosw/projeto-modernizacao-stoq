"""Proposed extraction for daily till movement reporting.

The original `_generate_dailymovement_data()` method mixes database queries,
payment grouping, card/check formatting, till entry retrieval and UI state
mutation. This artifact separates query, aggregation and report data.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, Protocol


@dataclass(frozen=True)
class DailyMovementCriteria:
    branch_id: int
    start_date: str
    end_date: str


@dataclass(frozen=True)
class MethodSummary:
    method_name: str
    income: Decimal = Decimal("0")
    outcome: Decimal = Decimal("0")


@dataclass(frozen=True)
class DailyMovementReport:
    sales: list = field(default_factory=list)
    return_sales: list = field(default_factory=list)
    purchases: list = field(default_factory=list)
    lonely_in_payments: list = field(default_factory=list)
    lonely_out_payments: list = field(default_factory=list)
    method_summary: list[MethodSummary] = field(default_factory=list)
    card_summary: dict = field(default_factory=dict)
    supplies: list = field(default_factory=list)
    removals: list = field(default_factory=list)


class DailyMovementRepository(Protocol):
    def find_in_payments(self, criteria: DailyMovementCriteria) -> Iterable:
        ...

    def find_out_payments(self, criteria: DailyMovementCriteria) -> Iterable:
        ...

    def find_till_supplies(self, criteria: DailyMovementCriteria) -> Iterable:
        ...

    def find_till_removals(self, criteria: DailyMovementCriteria) -> Iterable:
        ...


class MethodSummaryAggregator:
    def aggregate(self, in_payments: Iterable, out_payments: Iterable) -> list[MethodSummary]:
        totals: dict[str, list[Decimal]] = {}

        for payment in in_payments:
            totals.setdefault(payment.method_name, [Decimal("0"), Decimal("0")])
            totals[payment.method_name][0] += payment.value

        for payment in out_payments:
            totals.setdefault(payment.method_name, [Decimal("0"), Decimal("0")])
            totals[payment.method_name][1] += payment.value

        return [
            MethodSummary(method_name=name, income=values[0], outcome=values[1])
            for name, values in sorted(totals.items())
        ]


class DailyMovementReportBuilder:
    def __init__(
        self,
        repository: DailyMovementRepository,
        method_summary: MethodSummaryAggregator,
    ) -> None:
        self.repository = repository
        self.method_summary = method_summary

    def build(self, criteria: DailyMovementCriteria) -> DailyMovementReport:
        in_payments = list(self.repository.find_in_payments(criteria))
        out_payments = list(self.repository.find_out_payments(criteria))

        return DailyMovementReport(
            sales=[p for p in in_payments if p.sale_id],
            return_sales=[p for p in out_payments if p.sale_id],
            purchases=[p for p in out_payments if p.purchase_id],
            lonely_in_payments=[p for p in in_payments if not p.sale_id],
            lonely_out_payments=[
                p for p in out_payments if not p.sale_id and not p.purchase_id
            ],
            method_summary=self.method_summary.aggregate(in_payments, out_payments),
            supplies=list(self.repository.find_till_supplies(criteria)),
            removals=list(self.repository.find_till_removals(criteria)),
        )


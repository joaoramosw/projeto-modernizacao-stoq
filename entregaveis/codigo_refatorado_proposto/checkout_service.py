"""Proposed refactoring for the Stoq POS checkout flow.

This file is an illustrative artifact for the academic project. It does not
replace the original Stoq implementation directly. Its goal is to show how the
large `PosApp.checkout()` method could be moved from the GTK screen into an
application service with explicit dependencies.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Optional, Protocol


@dataclass(frozen=True)
class CheckoutItem:
    sellable_id: int
    quantity: Decimal
    unit_price: Decimal
    batch_id: Optional[int] = None


@dataclass(frozen=True)
class CheckoutCommand:
    operator_id: int
    branch_id: int
    items: Iterable[CheckoutItem]
    client_id: Optional[int] = None
    token_id: Optional[int] = None
    trade_id: Optional[int] = None
    save_only: bool = False
    cancel_clear: bool = False


@dataclass(frozen=True)
class CheckoutResult:
    sale_id: Optional[int]
    status: str
    message: str = ""


class SaleRepository(Protocol):
    def create_sale(self, command: CheckoutCommand):
        ...

    def save_order(self, sale):
        ...


class TradeService(Protocol):
    def apply_trade(self, trade_id: int, sale) -> None:
        ...


class SaleConfirmationWorkflow(Protocol):
    def confirm(self, sale, cancel_on_failure: bool) -> CheckoutResult:
        ...


class CheckoutValidator:
    def validate(self, command: CheckoutCommand) -> None:
        items = list(command.items)

        if not command.save_only and not items:
            raise ValueError("A sale checkout requires at least one item.")

        if command.trade_id and not items:
            raise ValueError("A trade checkout requires a replacement sale.")


class CheckoutService:
    """Coordinates checkout without depending on GTK widgets."""

    def __init__(
        self,
        validator: CheckoutValidator,
        sale_repository: SaleRepository,
        trade_service: TradeService,
        confirmation_workflow: SaleConfirmationWorkflow,
    ) -> None:
        self.validator = validator
        self.sale_repository = sale_repository
        self.trade_service = trade_service
        self.confirmation_workflow = confirmation_workflow

    def checkout(self, command: CheckoutCommand) -> CheckoutResult:
        self.validator.validate(command)

        sale = self.sale_repository.create_sale(command)

        if command.trade_id is not None:
            self.trade_service.apply_trade(command.trade_id, sale)

        if command.save_only:
            ordered_sale = self.sale_repository.save_order(sale)
            return CheckoutResult(
                sale_id=ordered_sale.id,
                status="ordered",
                message="Sale saved as order.",
            )

        return self.confirmation_workflow.confirm(
            sale=sale,
            cancel_on_failure=command.cancel_clear,
        )


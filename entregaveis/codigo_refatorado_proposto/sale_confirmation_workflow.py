"""Proposed workflow extraction for sale confirmation.

The original `FiscalPrinter.confirm()` mixes UI confirmation, fiscal device
steps, payment setup, transaction control, post-commit printing and generic
exception handling. This proposed design makes the steps explicit.
"""

from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class ConfirmationResult:
    sale_id: Optional[int]
    confirmed: bool
    message: str = ""


class PaymentGuard(Protocol):
    def ensure_not_overpaid(self, sale) -> None:
        ...


class ConfirmationDialog(Protocol):
    def request_confirmation(self, sale):
        ...


class FiscalGateway(Protocol):
    def identify_customer_if_needed(self, sale) -> None:
        ...

    def totalize(self, sale) -> None:
        ...

    def close_coupon(self, sale) -> None:
        ...


class PaymentGateway(Protocol):
    def setup_payments(self, sale) -> None:
        ...


class SaleService(Protocol):
    def confirm_sale(self, sale) -> None:
        ...


class TransactionManager(Protocol):
    def begin(self):
        ...


class PostCommitPrinter(Protocol):
    def print_optional_documents(self, sale) -> None:
        ...


class SaleConfirmationWorkflow:
    def __init__(
        self,
        payment_guard: PaymentGuard,
        confirmation_dialog: ConfirmationDialog,
        fiscal_gateway: FiscalGateway,
        payment_gateway: PaymentGateway,
        sale_service: SaleService,
        transaction_manager: TransactionManager,
        post_commit_printer: PostCommitPrinter,
    ) -> None:
        self.payment_guard = payment_guard
        self.confirmation_dialog = confirmation_dialog
        self.fiscal_gateway = fiscal_gateway
        self.payment_gateway = payment_gateway
        self.sale_service = sale_service
        self.transaction_manager = transaction_manager
        self.post_commit_printer = post_commit_printer

    def confirm(self, sale, cancel_on_failure: bool = False) -> ConfirmationResult:
        try:
            with self.transaction_manager.begin() as tx:
                self.payment_guard.ensure_not_overpaid(sale)
                confirmation_model = self.confirmation_dialog.request_confirmation(sale)

                if not confirmation_model:
                    tx.rollback()
                    return ConfirmationResult(None, False, "Sale confirmation cancelled.")

                self.fiscal_gateway.identify_customer_if_needed(sale)
                self.fiscal_gateway.totalize(sale)
                self.payment_gateway.setup_payments(sale)
                self.fiscal_gateway.close_coupon(sale)
                self.sale_service.confirm_sale(sale)
                tx.commit(confirmation_model)

            self.post_commit_printer.print_optional_documents(sale)
            return ConfirmationResult(sale.id, True, "Sale confirmed.")

        except Exception as exc:
            if cancel_on_failure:
                # In production, this branch should call a fiscal cancellation
                # adapter and produce auditable logs.
                return ConfirmationResult(None, False, f"Sale cancelled after failure: {exc}")

            return ConfirmationResult(None, False, f"Sale confirmation failed: {exc}")


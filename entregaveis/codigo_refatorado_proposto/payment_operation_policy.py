"""Proposed policy object to reduce duplication in payment operations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentOperationPolicy:
    can_cancel: bool = True
    can_change_due_date: bool = True
    can_pay: bool = True
    can_print: bool = False
    can_set_not_paid: bool = True
    create_transaction: bool = True
    pay_on_sale_confirm: bool = False


class PaymentOperation:
    policy = PaymentOperationPolicy()

    def can_cancel(self, payment):
        return self.policy.can_cancel

    def can_change_due_date(self, payment):
        return self.policy.can_change_due_date

    def can_pay(self, payment):
        return self.policy.can_pay

    def can_print(self, payment):
        return self.policy.can_print

    def can_set_not_paid(self, payment):
        return self.policy.can_set_not_paid

    def create_transaction(self):
        return self.policy.create_transaction

    def pay_on_sale_confirm(self):
        return self.policy.pay_on_sale_confirm


class StoreCreditOperation(PaymentOperation):
    policy = PaymentOperationPolicy(
        can_print=True,
        pay_on_sale_confirm=True,
    )


class CardOperation(PaymentOperation):
    policy = PaymentOperationPolicy(
        can_change_due_date=False,
        can_print=True,
    )


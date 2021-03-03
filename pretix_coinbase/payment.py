"""
pretix-coinbase
Copyright 2021 Marvin Schopf

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from collections import OrderedDict
from django import forms
from django.http import HttpRequest
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.models import OrderPayment, OrderRefund, Order
from pretix.base.payment import BasePaymentProvider, PaymentException


class Coinbase(BasePaymentProvider):
    identifier = "coinbase"
    verbose_name = _("Coinbase Commerce")
    public_name = _("Coinbase")

    @property
    def settings_form_fields(self):
        return OrderedDict(
            list(super().settings_form_fields.items())
            + [
                (
                    "coinbase_api_key",
                    forms.CharField(
                        widget=forms.Textarea,
                        label=_("Coinbase Commerce API key"),
                        required=True,
                    ),
                )
            ]
        )

    @cached_property
    def client(self):
        from coinbase_commerce.client import Client

        return Client(api_key=self.settings.coinbase_api_key)

    def checkout_confirm_render(self, request: HttpRequest, order: Order):
        return _(
            "After you confirm your order, you will be automatically redirected to Coinbase."
        )

    def execute_payment(self, request: HttpRequest, payment: OrderPayment):
        charge = self.client.charge.create(
            name=payment.order.event.name,
            description=payment.order.event.name,
            local_price={
                "amount": payment.amount,
                "currency": payment.order.event.currency,
            },
            pricing_type="fixed_price",
            metadata={"paymentId": payment.id},
        )
        payment.info = json.dumps(charge)
        payment.save(update_fields=["info"])
        return charge.data.hosted_url

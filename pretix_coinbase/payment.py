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

from collections import OrderedDict
from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _  # NoQA
from pretix.base.models import OrderPayment, OrderRefund
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

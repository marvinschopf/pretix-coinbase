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

from django.conf.urls import url, include
from pretix.multidomain import event_url

event_patterns = [
    url(
        r"^coinbase/",
        include(
            [
                event_url(r"^webhook/$", webhook, name="webhook", require_live=False),
                event_url(
                    r"^redirect/$", redirect_view, name="redirect", require_live=False
                ),
                url(
                    r"^return/(?P<order>[^/]+)/(?P<hash>[^/]+)/(?P<payment>[^/]+)/$",
                    ReturnView.as_view(),
                    name="return",
                ),
            ]
        ),
    ),
]

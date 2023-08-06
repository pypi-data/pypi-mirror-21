# AbuseHQ API Client

## About
**ahqapiclient** is a library which reflects the AbuseHQ API on client side.

## Dependencies

Needs python-dev packages for setup due to the usage of ujson. E.g. python-dev or python3-dev

## Usage

import Client from ahqapiclient

### Setup

endpoint = {
  "auth_method": "HMAC",
  "auth_options": {
    "key": "zwz5si71w3k4ftqkwlf1mhm84rjb13ke88xvixlf",
    "user": "user"
  },
  "name": "INTERNAL",
  "url": "https://yourcompany.abusehq.net/api/v1"
}

api_client = Client(endpoint)

### Usage

#### Get a case
case = api_client.case.get_case('case_id')

#### Perform a transition

api_client.case.trigger_transition('case_id', 'transition_id')

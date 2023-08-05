# intercomic
Tiny Client for the Intercom API (https://api.intercom.io/)

## Installation

Will be soon at PYPI

## Basic Usage

### Configure your client

```python
from intercomic import IntercomApp

intercom = IntercomApp(access_token='your-access-token')
```

### Examples

#### Users

```python
# Create a user
import json
user = intercom.users.create(json.dumps({'email': 'john@example.com', 'name': 'John'}))
# Find user by user_id
user = intercom.users.get(filters={'user_id': 1})
# Find user by email
user = intercom.users.get(filters={'email': email})
# Delete a user
user = intercom.users.delete(filters={'user_id': 1})
```



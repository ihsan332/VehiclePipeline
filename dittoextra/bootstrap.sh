#!/usr/bin/env bash
BASE=http://localhost:8080/api/2
AUTH="ditto:ditto"

# Create default policy
curl -sX PUT $BASE/policies/my.namespace:vehicle-policy \
  -u $AUTH -H "Content-Type: application/json" -d '{
  "entries": {
    "owner": {
      "subjects": {
        "nginx:ditto": {"type": "suite-auth"}
      },
      "resources": {
        "thing:/": {"grant": ["READ","WRITE"], "revoke": []},
        "policy:/": {"grant": ["READ","WRITE"], "revoke": []},
        "message:/": {"grant": ["READ","WRITE"], "revoke": []}
      }
    }
  }
}'

echo ""

# Create vehicle Thing
curl -sX PUT $BASE/things/my.namespace:vehicle-01 \
  -u $AUTH -H "Content-Type: application/json" -d '{
  "policyId": "my.namespace:vehicle-policy",
  "attributes": {"vin": "1HGBH41JXMN109186"},
  "features": {
    "speed": {},
    "obd": {},
    "diagnostics": {}
  }
}'

echo ""
echo "✓ Twin created: my.namespace:vehicle-01"
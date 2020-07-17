# Demo OPA permissions service

This is a very simple demo, returning a list of authorized "datasets",
some of which are open (which anyone can access), one of which is registered
(which here means anyone authenticated can access), but we can add more stringent
requirements, and some are controlled access with an access list.

```
open_datasets = ["open1", "open2", "open3"]
registered_datasets = ["registered1"]

controlled_access_list = {"alice":["controlled1"],
                          "bob":  ["controlled2"]}

```

For clarity here everything is in one static rego file, but it's possible to
incorporate [external data](https://www.openpolicyagent.org/docs/latest/external-data/)
into OPA documents in a nmber of ways.

Valid JWT tokens are created for alice, bob, charlie (who has no controlled access
authorizations), as well as an expired token for alice.  Then these are tested
against expectations for the policy.

## Running

First install the necessary python packages (just used to generate JWTs and
keys):

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

Then create the necessary keys and tokens, and update
the static policy

```bash
make
```

Start up OPA using the new policy:

```bash
docker-compose up -d
```

and you should shortly be able to test that unauthenticated requests can access
the open datasets:

```bash
curl -i localhost:8181/v1/data/permissions/allowed \
      -d @request_unauthenticated.json \
      -H 'Content-Type: application/json'
```

where the post body was:

```json
{
    "input":{
        "method": "GET",
        "path": ["beacon"]
    }
}
```

and get back the result:

```
{"result":["open1","open2","open3"]}
```

as expected, the unauthenticated user could only access the open datasets.

You can try with Alice's token:

```
source crypto/token_envs.sh
curl -i localhost:8181/v1/data/permissions/allowed \
     -H 'Content-Type: application/json' \
     -d "{ \"input\": { \"method\": \"GET\", \"path\": [\"beacon\"], \"user\": \"$ALICE\" } }"
```

And sure enough, Alice can see the open datasets, registered datasets 
(because she's an authenticated user here) and the `controlled1` dataset:
```
{"result":["open1","open2","open3","registered1","controlled1"]}
```

You can then run the tests (and see how the service is called using the 
requests library in python) with:
```
pytest
```

The policy is in policy/permissions.rego; it is written in a DSL called
[rego](https://www.openpolicyagent.org/docs/latest/policy-language/), and
the OPA team provides a very handy [rego sandbox](https://play.openpolicyagent.org)
for playing with policies.

If you update the policy, you can restart OPA with `docker-compose restart opa`, 
or, less heavy-handedly, use the [REST API](https://www.openpolicyagent.org/docs/latest/rest-api/)
to trigger a reload.

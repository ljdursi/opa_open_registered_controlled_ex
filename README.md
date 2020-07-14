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

## Running

First install the necessary python packages:

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

Startup OPA using the new policy:

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


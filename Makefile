POLICY=policy/permissions.rego
POLICY_TEMPLATE=policy/permissions.rego.template
KEYS=crypto/${PUBLIC_KEY} crypto/${PRIVATE_KEY}
PUBLIC_KEY=public.pem
PRIVATE_KEY=private.pem
TOKENS=crypto/alice_expired_id.jwt crypto/alice_id.jwt crypto/bob_id.jwt crypto/charlie_id.jwt
ISSUER=trustedIdP

all: ${POLICY} ${KEYS} ${TOKENS}

${POLICY}: ${POLICY_TEMPLATE} ${KEYS} 
	./generate_static_policy.py ${POLICY_TEMPLATE} crypto/${PUBLIC_KEY} -i ${ISSUER}

crypto/${PRIVATE_KEY} crypto/${PUBLIC_KEY}:
	(cd crypto; ./generate_keys.py)

${TOKENS}: crypto/${PRIVATE_KEY}
	(cd crypto; python3 generate_tokens.py ${PRIVATE_KEY} -i ${ISSUER})

clean:
	- rm -f ${POLICY}
	- rm -f crypto/${PUBLIC_KEY}
	- rm -f crypto/${PRIVATE_KEY}
	- rm -f ${TOKENS}
# Elastic / Kibana Keycloak Integration

This document summarizes helm values and manual steps that are required to integrate with keycloak.

## Configuration Steps

These are the items you need to do to configure keycloak, elastic search, and kibana for SSO on the ECK stack in your Big Bang installation. 

### Keycloak Configuration

#### Prerequisites

Keycloak is configured with a working Realm including Groups and Users.

#### Process

- Create an elastic OIDC client scope with the following mappings
  
  | Name     | Mapper Type      | Mapper Selection Sub | Token Claim Name   | Claim JSON Type |
  |----------|------------------|----------------------|--------------------|-----------------|
  | email    | user property    | email                | email              | string          |
  | group    | Group Membership | N/A                  | groups             | N/A             |
  | username | User Property    | username             | preferred_username | string          |
  
- Create an elastic client 
  - Change the following configuration items
    - access type: confidential _this will enable "Credentials"_
    - Direct Access Grants Enabled: Off
    - Valid Redirect URIs: kibana.${DOMAIN}/*
  - Set Client Scopes
    - Default Client Scopes: elastic (the client scope you created in the previous step)
    - optional client scopes: N/A
  - Take note of the client secret in the credential tab

To verify the client, check that these fields are present:

```json
{
  "exp": 9999999999,
  "iat": 9999999999,
  "jti": "00000000-0000-0000-0000-000000000000",
  "iss": "https://${keycloakRootUrl}/auth/realms/{realm_name}",
  "sub": "00000000-0000-0000-0000-000000000000",
  "typ": "Bearer",
  "azp": "${client_id}",
  "session_state": "00000000-0000-0000-0000-000000000000",
  "acr": "1",
  "scope": "openid elastic",
  "groups": [
    "group_1",
    "...",
    "group_n"
  ],
  "preferred_username": "${username}",
  "email": "${email}"
}
```

### Elastic Configuration

The config changes needed for SSO/Keycloak in Elastic are embedded in the helm chart and require values to be set.

Set the values for your elasticsearch-kibana helm chart as follows:

```yaml
sso:
  enabled: true # Toggle this on
  client_id: # Set this to your elastic client id from Keycloak
  client_secret: # Set this to the client credential from keycloak
  oidc:
    host: # Set this to the base URL for your Keycloak instance, i.e. keycloak.example.com
    realm: # Set this to the realm being used from Keycloak

kibanaBasicAuth:
  enabled: true # This should initially be enabled to allow you to setup role mappings
```

Make sure that you have enabled an enterprise license via the operator - this can be done in Big Bang via the logging values section.

NOTE: Local development makes use of login.dsop.io and the necessary values are committed in the values.yaml files in each repo.

#### OIDC Custom CA

Elasticsearch can be configured to point to specific files to trust with an OIDC auth connection, here is an example when using Big Bang to deploy elasticsearch-kibana, assuming you are populating a secret named "oidc-ca-cert" in the same namespace, with a key of `ca.crt` and value of a single PEM encoded certificate:

```yaml
logging:
  values:
    elasticsearch:
      master:
        volumes:
        - name: cert
          secret:
            secretName: oidc-ca-cert
            defaultMode: 0644
        volumeMounts:
        - mountPath: "/usr/share/elasticsearch/config/oidc/ca.crt"
          name: cert
          subPath: ca.crt
          readOnly: true
      data:
        volumes:
        - name: cert
          secret:
            secretName: oidc-ca-cert
            defaultMode: 0644
        volumeMounts:
        - mountPath: "/usr/share/elasticsearch/config/oidc/ca.crt"
          name: cert
          subPath: ca.crt
          readOnly: true
    sso:
      cert_authorities: ["/usr/share/elasticsearch/config/oidc/ca.crt"]
```

NOTE: Only Elasticsearch contains the SSO configuration, no need to add volumes/Mounts to Kibana via values.

NOTE: The path for the cert authority can be any path on the container as long as it's not overwriting an existing file, the path above is an example that has been used for testing.

### Kibana Configuration

Kibana requires no additional helm values changes, since all of the above will incorporate the necessary Kibana changes.

To set up role mappings and fully enable SSO:
 - Decrypt the elasticsearch user secret from the kubernetes secret
   - `kubectl get secrets -n logging logging-ek-es-elastic-user -o yaml | grep elastic: | awk 'NR==1{printf $2}' | base64 -d | xargs echo`
 - Log into kibana with user elastic and the decrypted password
 - Go to Management -> Stack Management -> Security -> Role Mappings
 - Create the desired role 
    - For development the following settings will make everyone a super user. Roles: Superuser, Mapping rules: groups = *
    - NOTE: for integration other oauth providers (such as google), you may need to adjust this role mapping to something like `username = *`
 - You should now be able to login to Kibana with Keycloak realm users

## Dev Reference Resources

- [parent eck documentation](https://www.elastic.co/guide/en/cloud-on-k8s/1.2/index.html)
- [elastic secure settings](https://www.elastic.co/guide/en/cloud-on-k8s/1.2/k8s-es-secure-settings.html)
- [kibana configuration](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/oidc-kibana.html)
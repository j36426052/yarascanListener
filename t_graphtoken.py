from msal import ConfidentialClientApplication
import msal

def getToken():

    client_secret = 'DJg8Q~owtzmiMN-szjmADMMec-ibcxhnTiPu7bN.'
    client_id = 'ff9050b9-ddad-4b30-b158-26b93bb7a296'
    tenant_id = "a9dbaac3-efaf-4de3-bb0d-ac6a160ebee3"
    SCOPES = ['Mail.Read','Mail.ReadWrite','Mail.ReadBasic']

    msal_authority = f"https://login.microsoftonline.com/{tenant_id}"

    msal_scope = ["https://graph.microsoft.com/.default"]

    msal_app = ConfidentialClientApplication(
        client_id = client_id,
        client_credential=client_secret,
        #authority = msal_authority,
    )

    result = msal_app.acquire_token_silent(
        scopes = SCOPES,
        account=None,
    )

    if not result:
            result = msal_app.acquire_token_for_client(scopes=msal_scope)



    if "access_token" in result:
            access_token = result["access_token"]
    else:
        raise Exception("No Access Token found")
    
    return access_token

def get_access_token():
    tenantID = "a9dbaac3-efaf-4de3-bb0d-ac6a160ebee3"
    authority = 'https://login.microsoftonline.com/' + tenantID
    clientID = 'ff9050b9-ddad-4b30-b158-26b93bb7a296'
    clientSecret = 'DJg8Q~owtzmiMN-szjmADMMec-ibcxhnTiPu7bN.'
    scope = ['https://graph.microsoft.com/.default']
    #scope = ['Mail.Read','Mail.ReadWrite','Mail.ReadBasic']
    app = msal.ConfidentialClientApplication(clientID, authority=authority, client_credential = clientSecret)
    access_token = app.acquire_token_for_client(scopes=scope)
    return access_token['access_token']

print(get_access_token())

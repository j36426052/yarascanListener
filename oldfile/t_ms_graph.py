import webbrowser
import os
import msal# import ConfidentialClientApplication, PublicClientApplication



def generate_accesstoken(app_id,scopes):
    access_token_cache = msal.SerializableTokenCache()
    

    if os.path.exists('api_token.json'):
        access_token_cache.deserialize(open("api_token.json","r").read())
    client = msal.PublicClientApplication(client_id=app_id,client_credential=access_token_cache)#
    accounts = client.get_accounts()
    if accounts:
        token_response = client.acquire_token_silent(scopes,accounts[0])
    else:
        flow = client.initiate_device_flow(scopes = scopes)
        print(flow)
        print('user_code'+flow['user_code'])
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('api_token.json','w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

if __name__ == '__main__':
    ...

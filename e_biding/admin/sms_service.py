def sendSMS(contact, message):
    import requests

    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS&language=english&route=p&numbers="+contact+"&message="+message
    headers = {
        'authorization': "SoMGEDigsZUJ186Au4BTm7hcdvFnfeCXWVlN30Y52pkROwqjyLnih4LQmXc8SdVbYI3zB5DNxPf6waes",
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    s1 = response.text
    return s1

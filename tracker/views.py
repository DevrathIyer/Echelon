from django.shortcuts import redirect, render
from django.db import models
from random import randint
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
import base64
import requests
import os

def home(request):
    return render(request, 'tracker/index.html', {})

def signedin(request):
    id_token = request.POST.get('TokenID')
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+id_token
    response = requests.get(url)
    f = """-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,2F5252FFFF575D73

EAOm5SztxVoaNQgh0PyR0FZlyJM5Hdyz+GL/GVQyJjaUFMmOkDTUsNcv8k4AzB7V
9yz0gpWajwQCqJDfC3u9FO8PtPKisqvB1/cy0QfAvODND6XapYotav94K8y2ape2
2amfaifN0Nci/DnbU5t5trwRyh6A/iC2RVTFuqssFMFDUMagXbzgD56stb0n6ccF
NqprkbNNN/ICaFG+YcwX0Pr5i2EaSiqP/6a9+seK0cf+/tU4Uc43Rbgzj8jxAWkM
nb0ufGPmV0U2a5i3G7/4Vh/1/HQa8uLYDvANCpknuWyV1qvU8ez+KF2iSo+WNApi
avEi785Rw8hzA1OOnxkYsPp1Klrj5xPMZBv45MF4PLji32K37BvFNhxM7svtotmi
akyVmLLwBnSjqWW48e9s0iFMcreVKSwG03uCq/s4iXJFdxLPp3NVU3I+nb3BPdeV
dQRsV6M/eDMsvhXuAx7d7wMkl6cB0rOxbZ2Gxmvwwx1tT70NtAJFtCPIkx3JDEOH
bBynvMdKBP43cGfjSYpcnUtVlgRTCRFxiQgd8ozIDe+I7zUAhDFiLdksiHidM75O
vB3AnkiLTmsesPixMABd6peL/d1dKDEe+yhr02mhwLFx/6aV4eRU2PTzJudHNHOD
hJ5Dc2o0vDI/1hSY02boI5qqgllWfkB8zhSkcrn+o6nt59zPEidiuxPVkFtd+K15
dzPNi+br/cLPatcQlDLlt/mNIK4LmJVzIGxgspvEN1hO2toh7gEBfQafMRo+o7Yo
z5bAgAD303S3Hp2J0zb3F7UAP0GjlBO3dm+wDJJibSTVFeLOAPMNBQitHcxpAK/L
lscegz/u/qyHvxwDNtlVzJcU1c7N6sgl22kM//t5NVumay1wztUeUoKblyu+Ejlw
wMWYu/f789QanN81tWRVHVCdpH84UnRVEif0BvTIhho+zF7XHNaMrQCPbZwoz2O9
GwbWcadgdKrGjfGO6nV2OPSMEL8q+4k2K2iaVQNWWPkFtmiT2v38mwBBuIt3UL7T
t7sbwATQCg3+PmnBmX6NmYKUllzQfaN+0X74vuPXdEpTtS4AG/u5KL6KB0H/VzzN
zMqVDV3IqoVZtDn3zE5ssh9I61g0U5FByq42AfAKKQd92Asw2bdmJoT+uMzOqbI1
N0gZXIDIi1XWGjygv/9mIWyuljqLRwNPtRE59eNsb2MuQeCH9UBSUPWHHBfyNmpY
WNQ8bjaHmASR0Kba9GugyHdVoNkNKDflSDpkr3VCiSOJewN58MujTOi4HVdgU05o
2vExDYHBzV/wAZXiuNO8nd/bRRJKjhZ/IH3vusz/kzw9fNQjrcLTwb8TCceTvOlG
ZpUSJbN/0oFtbGidplSODGdyRaZ9lHSNA4ylS4S9c1U8Hv/zC+ZHOa8OMAhS2CKG
YA3OpZujVRdQPeodBCqFocvEjEwWhPzpxN/Q3/bMX9gvEZNSjl2N5ms7EkxRqQmA
2GwN4EvxUrfa+xUMXd1mPz0h2V5vY0RUhiZx08DcTE2yHw5jf3kf758tgUb/e3EH
YZwZkOfXiUuP0/8ff94r4B23WE3kAxJXj09IiANe6aX9WJtcGNbhqCNU9hgRMu2h
-----END RSA PRIVATE KEY-----
"""
    r = RSA.importKey(f, passphrase=os.environ['ENCRYPTION_PASSWORD'])
    #string = base64.b64encode(bytes('hello'))
    hash = SHA256.new('hello').digest()
    data = base64.b64encode(bytes(r.sign(hash, 32)))
    post_data = {'command': 'hello', 'signature': data}
    """response.json()['aud'] == GoogleID:"""
    if 1==1:
        try:
            #UserID = response.json()['sub']
            #data = "\xaa\xae\x19.{\xe7\xd9\xb2\xd4\x14\x97\xbf\x95\xeb=\xf3\xc6\xf1\xab^\x9f%22}\xb7YA\xce\xda\xf0\xc3\xb2\xcc\xa9\xe6\x8buP\x85*\x15\x81\xd7\x87\xbd\x14\xee\x1c=-\xd9\xa3`\xa2\xb5\xf4\nt\x92\x0612\xf1^\xc9?;dm\xa2\xbb\xaf\xa9X\x1d\xbb,\xb3\xaf\xdcc\xf6\x97\x05\xe9\xcc\x99U\xdf\x8d\xb5\x95\x92\xe8\xe6\x03\xa2\x07s\xc5`;|\x92\x14\t\xa7\x15T\xa2\x81\xdf\xc8\x18\x0e\xc4\x06\xc0\xeai2\xe6\xb0\xae\xfb:+%\x9f\x04\x9c\xc6\xc0ow\xa5E/S(\xd0\x18i\xb4\x02\x92\x18\xb4\xd4\xb3)\x9ea\xe8\x81e\xd2\xc8\xfe~\x91\x9f\x80\xdb]\xd79\xe0\x89\xfd\xed\xd8\xddA\xe4d\xa4\x1b\xc9\xb7\x9a\x03\x82\xfb\x19\xe6\xf7\xaeU^\x94\x97Da\xc3#H\xdf\xa0\xe3\xaas\x91\xd2\x16!r\xdaT\x9a\xb0\xfa\x1a7w\x11\x95\xef\x06^\xa8\xf6\x14)d\x00[b\x12\xbc+\xe1M\xdf\x05N\x0eqv\xf2\x9f\xbf\x91\\\xb0\xfc+Ql\xb2z7a<\xac\xf8!"
            #response2 = request.get("http://echelon-nn.herokuapp.com/admin/test?text="+data)
            response = requests.post('http://echelon-nn.herokuapp.com/admin/test', data=post_data)
            content = response.content
            return render(request, 'tracker/Faliure.html', {'JSON': content})
            #LoggedInUser = EchelonUser.objects.get(user_email=email)
            #userUrl = 'https://echelonportal.herokuapp.com/tracker/user/' + models.b64encode(LoggedInUser.user_index)
            #return redirect(userUrl)
        except:
            #return render(request, 'tracker/Faliure.html', {'JSON': response.json()})
            #return NewUser(request,email)
            UserID = 0

    else:
        return render(request, 'tracker/Faliure.html', {})
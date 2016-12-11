from django.shortcuts import redirect, render
from django.db import models
from random import randint
from Crypto.PublicKey import RSA
from Crypto import Random
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
DEK-Info: DES-EDE3-CBC,F06040FFE2E81A78

5oQO5bhieEwjonstBJr5RMgda/b+PuaNO/0SrCrYEUpL4DkPs9Kl9j7PL6qlzjT3
6RvuLsI5zMnxPl/5LdiTmuWwBrfKkMIld0bWxmc5BYMFdigoRQDvbkbwNZewQcQj
fFjxF96HqHi7lTFdjP20QOvHw/LbNshIln5V4H408zLLB3EVV79VLtSu5a+ZEayE
RWE7aXy6HLStuZm7i/QA4S6i7UAKkzYwRpwr+A23oCKZ3ljjzEDnbQxZ+05/xCUM
N2XbcMIz0monO2iQOxnqW62ZMN4Q35L/41Da+pwExB4xJnoFBX+YcudNEMRQT/0c
nt+gToIpglvwL5wAxQJK3qPpJGnLbXg2EksgzBeJ3T25ua+59CinjFYs6g9XSvV2
8bL34D6PE1t4d23CrEM2btWFDywAmJ9sEoE6rYMdSQJkEeWoHAHL0gsehNia5/xg
Sn15g+Gyb5N5IWNpOzl1ik74tm6YEoghyXxsaQAxkob0O7KJCRRo5kwMf+fT3vX/
wS/+L8ZeIyY96q8tLyk2DT5iOIwIvFPGL2BJFd6Hk2xbn7ZmFEQnzTxFtjTPQhhl
3ZyEzhXVmR/E1zrT5SXi1iuB1stPKucRSz/X/dRUNFAMn3iR55SbhkR81TZLLdnl
AShiDq97+bWYSAGGBamf5nExjvGaRcwGE81Ng8LiekTL8c973PRODUnOws8ydpvF
7eqJEsKHnLJKwDPKV3qMOXpA6CPmTD7vUQBjxdxlPMACXGt4XNrHC0jduAlr77wm
VRNK+6oofzMrJ6VVzL5gJpenjnp7csMqkrPXyowfjMwYohHJ+Nu8MG7xTj6UHXlT
vavCpj6R/x8GjrWvYtF26/Zd8mHvMXqbMQtuGYngB3pRKbvyVgOP8Am9NOx4widk
GFfU9m/J/PsjMMA+T52nL8Rnqn0FGYj5e/KSXGxiwDVNR3fjUJTAxl/S6p+sNjbD
zVl+TkKSJPr6YiURC1Q0DDcqDfADC4E6BfobjDIuqnsa6BKd2jbU0DID+tWJy9BP
O4emEiQUq6NdPCryqgnoKRGVJqc0DAupHs3c0K43TMPDzXF7I93929y8eO6Uk92l
vZqAANkuoDiX6oOlpeT9YlNtgwSF9fyXejS7JSUSdyrnB3F/wIe10xbBiwKvCt/L
9P6tgc6us5Kiui154I9k1Odkpy5BaGUa8Ad0FG4W/BZyqtKEun0IhaQGuFOWS2i5
EM/h5yDIjiW73cwc3HQpMi5cbiIJmOdtHD0rE74qSVUbmpuyuVsYoaLtRHj8HHfL
8ZCYsjoB/Nb4C8RxqoWcMrB5hIYr1OZxEkaXaltgqG9oUlvxqsQx9YryGTiH2z0O
t7DMpVYQQQm+VNXIqGkbLAULh+RR9/lJfxAGwfE779ZmC6x4eGXZESPfRgyy7fyQ
FEE55MSRclGUIf6nEGUnltLiDqzugTuQdZ2Kex4iNyCmsAa+/SYtwzo4n1IIuq++
e9s3OBorPItUy5jQAVh3sQ0ouTG69xPkpuC+22rX98wbRFCYapeuqaDHrclxHsDT
tW44/tVjrQF5hQuc4mL13EJQsOYqn2+kftjAZSkuZaq/bJM1Vem6oA==
-----END RSA PRIVATE KEY-----
"""
    r = RSA.importKey(f, passphrase=os.environ['ENCRYPTION_PASSWORD'])
    data = r.sign('hello', 32)
    post_data = {'command': 'hello', 'signature': data}
    """response.json()['aud'] == GoogleID:"""
    if 1==1:
        try:
            #UserID = response.json()['sub']
            #data = "\xaa\xae\x19.{\xe7\xd9\xb2\xd4\x14\x97\xbf\x95\xeb=\xf3\xc6\xf1\xab^\x9f%22}\xb7YA\xce\xda\xf0\xc3\xb2\xcc\xa9\xe6\x8buP\x85*\x15\x81\xd7\x87\xbd\x14\xee\x1c=-\xd9\xa3`\xa2\xb5\xf4\nt\x92\x0612\xf1^\xc9?;dm\xa2\xbb\xaf\xa9X\x1d\xbb,\xb3\xaf\xdcc\xf6\x97\x05\xe9\xcc\x99U\xdf\x8d\xb5\x95\x92\xe8\xe6\x03\xa2\x07s\xc5`;|\x92\x14\t\xa7\x15T\xa2\x81\xdf\xc8\x18\x0e\xc4\x06\xc0\xeai2\xe6\xb0\xae\xfb:+%\x9f\x04\x9c\xc6\xc0ow\xa5E/S(\xd0\x18i\xb4\x02\x92\x18\xb4\xd4\xb3)\x9ea\xe8\x81e\xd2\xc8\xfe~\x91\x9f\x80\xdb]\xd79\xe0\x89\xfd\xed\xd8\xddA\xe4d\xa4\x1b\xc9\xb7\x9a\x03\x82\xfb\x19\xe6\xf7\xaeU^\x94\x97Da\xc3#H\xdf\xa0\xe3\xaas\x91\xd2\x16!r\xdaT\x9a\xb0\xfa\x1a7w\x11\x95\xef\x06^\xa8\xf6\x14)d\x00[b\x12\xbc+\xe1M\xdf\x05N\x0eqv\xf2\x9f\xbf\x91\\\xb0\xfc+Ql\xb2z7a<\xac\xf8!"
            #response2 = request.get("http://echelon-nn.herokuapp.com/admin/test?text="+data)
            response = requests.post('http://echelon-nn.herokuapp.com/admin/test', data=post_data)
            content = response.content
            return render(request, 'tracker/Faliure.html', {'JSON': data})
            #LoggedInUser = EchelonUser.objects.get(user_email=email)
            #userUrl = 'https://echelonportal.herokuapp.com/tracker/user/' + models.b64encode(LoggedInUser.user_index)
            #return redirect(userUrl)
        except:
            #return render(request, 'tracker/Faliure.html', {'JSON': response.json()})
            #return NewUser(request,email)
            UserID = 0

    else:
        return render(request, 'tracker/Faliure.html', {})
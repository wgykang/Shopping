# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/6/25/14:44'


# 授权登录
def get_auth_url():
    """
        client_id   必填  string  申请应用时分配的AppKey。
        redirect_uri    必填  string  授权回调地址，站外应用需与设置的回调地址一致。
    """
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://127.0.0.1:8000/complete/weibo/'
    client_id = '432622721'
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=client_id,
                                                                                      re_url=redirect_url)

    print(auth_url)


# 获取用户的uid等信息
def get_access_token(code):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": '432622721',
        "client_secret": "1d62d78ddc2686076506d5194c4ad50d",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/complete/weibo/",
    })
    pass
    # b'{"access_token":"2.00uAcWIB0pvORT8e51c72988fbd5xB","remind_in":"157679999","expires_in":157679999,"uid":"1042116144","isRealName":"true"}'


# 获取用户信息
def get_user_info(access_token):
    user_url = "https://api.weibo.com/2/users/show.json"
    uid = "1042116144"
    get_url = user_url + "?access_token={at}&uid={uid}".format(at=access_token, uid=uid)
    print(get_url)


if __name__ == '__main__':
    get_auth_url()
    get_access_token('316a6bf6ee6fdf30e180d0f11de8e589')
    get_user_info("2.00uAcWIB0pvORT8e51c72988fbd5xB")

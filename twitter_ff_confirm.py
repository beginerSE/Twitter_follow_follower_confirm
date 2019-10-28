import tweepy

api_dict = {
           　'my_account_id':['api_pub',
                               'api_sec',
                               'access_token',
                               'access_token_secret'
                             ]
           }


# フォローしていなくても外さないアカウントのリスト
unrequited_list = {
                   'my_account_id':['MSkieller',
                                    'BitcoinSVinfo',
                                    '_unwriter',
                                    'excalibur0922',
                                    'money_button'
                                    ]
                  }



for k, v in api_dict.items():
    
    consumer_key = v[0]
    consumer_secret = v[1]
    access_token = v[2]
    access_secret = v[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    #自分のuserid
    userid = k

    try:
        #自分のアカウントのフォロワーをすべて取得する
        followers_id = api.followers_ids(userid)

        #自分のアカウントのフォロイングをすべて取得する
        following_id = api.friends_ids(userid)

        #フォローされていなくてもOKなアカウントの情報をIDから取得
        unrequited = unrequited_list[k]
        for i in unrequited:
            try:
                sp_id = api.get_user(i)._json['id']
                followers_id.append(sp_id)
            except Exception as e:
                print(i, e.args)
            
        # API制限などのカウント用変数を定義
        api_limit = 0
        unfollow_user = 0
        follow_user = 0

        # 相互じゃないユーザーのフォローを解除する
        for following in following_id:
            if following not in followers_id and api_limit < 40:
                userfollowers = api.get_user(following).followers_count
                # フォロワー数が10000人以下で自分をフォローしていないユーザーを除外する
                if userfollowers < 10000:
                    username = api.get_user(following).name
                    print("リムーブするユーザー名", username)
                    print("フォロワー数", userfollowers)
                    # フォローを外す
                    api.destroy_friendship(following)
                    api_limit += 1
                    unfollow_user += 1


        for follower in followers_id:
            # フォローを返していないユーザーにフォローを返す
            if follower not in following_id and api_limit < 40:
                try:
                    username = api.get_user(follower).name
                    print("フォローするユーザー名", username)
                    api.create_friendship(follower)
                    api_limit += 1
                    follow_user += 1
                except Exception as e:
                    e_msg = e.args[0][0]['code']
                    # api制限に引っかかった場合（Code161）はループ終了
                    if e_msg == 161:
                        break
                    # それ以外の場合はエラーメッセージを表示
                    else:
                        print(e.args)

        print(f'リムったユーザーは{unfollow_user}人です')
        print(f'フォローしたユーザーは{follow_user}人です')

    except Exception as e:
        print(f'{k}のAPI操作でエラーが発生しました')
        print(e.args)

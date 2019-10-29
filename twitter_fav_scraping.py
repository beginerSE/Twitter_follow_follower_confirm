import tweepy

# 各種APIキーをセット
# twitterのAPI鍵
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# 必要なインスタンスを生成
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# 検索キーワードを指定
q = 'python' 
# 検索するツイート数 
count = 10 
# 検索を実行
search_results = api.search(q=q, count=count)
# 検索したツイート内容を保存する変数
tweet_list = []

# 検索結果を1つずる処理する 
for result in search_results:
    #ツイートのstatusオブジェクトからツイートidを取得、userから内部IDを取得する
    user = result.user.name
    username = result.user._json['screen_name']
    time = result.created_at
    tweet = result.text
    tweet_list.append(tweet)
    print(user, username)
    print(tweet)
    print(time)
    try:
        # いいね！をする
        api.create_favorite(user_id)
    except Exception as e:
        print(e.args)

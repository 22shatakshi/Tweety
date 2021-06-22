import tweepy

api_key = 'API key'
api_secret = 'API Secret'
access_key = 'Access Key'
access_secret = 'Access Secret'

auth = tweepy.OAuthHandler(api_key, api_secret)

auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
	
def retrieve_lastseen_id(file_name):
	f_read = open(file_name, 'r')
	lastseen_id = int(f_read.read().strip())
	f_read.close()
	return lastseen_id
	
def store_lastseen_id(lastseen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(lastseen_id))
	f_write.close()
	return
			
def send_tweet():
	user_text = input('Enter tweet text: ')
	print('Tweeting...', flush = True)
	api.update_status(user_text)
	
def send_tweet_with_media():
	user_text = input('Enter tweet text: ')
	file_name = input('Enter media file name/path: ')
	print('Tweeting...', flush = True)
	api.update_with_media(file_name, user_text)

def follow_back():
	followers = api.followers()
	for follower in followers:
		if not follower.following:
			print('Following back ' + follower.name, flush = True)
			api.create_friendship(follower.id)

def like_mentions():
	mentions = api.mentions_timeline()
	for mention in reversed(mentions):
		if mention.user.id == api.me().id:
			pass
		if not mention.favorited:
			print('Liking tweet by ' + mention.user.screen_name, flush = True)
			mention.favorite()
			
def retweet_mentions():
	mentions = api.mentions_timeline()
	for mention in reversed(mentions):
		if mention.user.id == api.me().id:
			pass
		if not mention.retweeted:
			print('Retweeting tweet by ' + mention.user.screen_name, flush = True)
			mention.retweet()
			
def reply_to_mentions():
	lastseen_id = retrieve_lastseen_id('lastseen_mention_id.txt')
	mentions = api.mentions_timeline(lastseen_id, tweet_mode = 'extended')
	for mention in reversed(mentions):
		lastseen_id = str(mention.id)
		store_lastseen_id(lastseen_id, 'lastseen_mention_id.txt')
		print(mention.full_text, flush = True)
		reply = input('Reply: ')
		print('Responding to tweet...', flush = True)
		api.update_status('@' + mention.user.screen_name + ' ' + reply, mention.id)
			
def reply_to_mentions_with_keyword():
	keyword = input('Enter keyword: ')
	mentions = api.mentions_timeline(tweet_mode = 'extended')
	for mention in reversed(mentions):
		if keyword.upper() in mention.full_text.upper():
			print(mention.full_text, flush = True)
			print('Found ' + keyword, flush = True)
			reply = input('Reply: ')
			print('Responding to tweet...', flush = True)
			api.update_status('@' + mention.user.screen_name + ' ' + reply, mention.id)
			
def reply_to_timeline_tweets():
	keyword = input('Enter keyword: ')	
	lastseen_id = retrieve_lastseen_id('lastseen_id.txt')
	public_tweets = api.home_timeline(20, lastseen_id, tweet_mode = 'extended')
	for tweet in reversed(public_tweets):
		lastseen_id = str(tweet.id)
		store_lastseen_id(lastseen_id, 'lastseen_id.txt')
		if keyword.lower() in tweet.full_text.lower():
			print('Found ' + keyword, flush = True)
			reply = input('Reply: ')
			print('Responding to tweet...', flush = True)
			api.update_status('@' + tweet.user.screen_name + ' ' + reply, tweet.id)

def menu():
	print('1. Tweet without media', flush = True)
	print('2. Tweet with media', flush = True)
	print('3. Follow back followers', flush = True)
	print('4. Like mentions', flush = True)
	print('5. Retweet mentions', flush = True)
	print('6. Reply to mentions', flush = True)
	print('7. Reply to mentions containing user-specified keyword', flush = True)
	print('8. Reply to home timeline tweets containing user-specified keyword', flush = True)
	print('9. Exit', flush = True)
	
loop = True
while loop:
	menu()
	option = input('Enter option: ')
	if option == '1':
		print('Option 1 selected', flush = True)
		send_tweet()
	elif option == '2':
		print('Option 2 selected', flush = True)
		send_tweet_with_media()
	elif option == '3':
		print('Option 3 selected', flush = True)
		follow_back()
	elif option == '4':
		print('Option 4 selected', flush = True)
		like_mentions()
	elif option == '5':
		print('Option 5 selected', flush = True)
		retweet_mentions()
	elif option == '6':
		print('Option 6 selected', flush = True)
		reply_to_mentions()
	elif option == '7':
		print('Option 7 selected', flush = True)
		reply_to_mentions_with_keyword()
	elif option == '8':
		print('Option 8 selected', flush = True)
		reply_to_timeline_tweets()
	elif option == '9':
		print('Option 9 selected', flush = True)
		print('Exiting...', flush = True)
		loop = False
	else:
		print('Invalid option selected. Please try again.', flush = True)

			
	

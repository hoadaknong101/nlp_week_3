import praw
import dotenv

reddit = praw.Reddit(
    client_id = dotenv.get_key('.env','REDDIT_CLIENT_ID'),
    client_secret = dotenv.get_key('.env','REDDIT_CLIENT_SECRET'),
    user_agent="SentimentAnalysisApp/0.1 by Nhom3"
)
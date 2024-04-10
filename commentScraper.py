import praw
import sqlite3
from praw.models import MoreComments

# Create a Reddit instance
reddit = praw.Reddit(client_id='9zdXuNhZ6-4OYvfZS8fRMQ',
                     client_secret='noioJ8Y5QfOzelP35zYAUUg7qzD71A',
                     user_agent='WebScrap')

conn = sqlite3.connect('comments.db')
c = conn.cursor()

# Create tables
c.execute('CREATE TABLE IF NOT EXISTS word_count (word TEXT, count INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS comment_list (comment TEXT)')

# Specify the subreddit and post ID
subreddit_list = ['python', 'funny', 'AmA']
num_posts = 100
num_comments = 100

def scrape_comments(subreddit, num_posts, num_comments):
    for sub in subreddit_list:
        subreddit = reddit.subreddit(sub).hot(limit=num_posts)
        comment_list = []
        
        for post in subreddit:
            post.comments.replace_more(limit=None)
            comments = post.comments.list()[:num_comments]
            
            # Process the comments
            for comment in comments:
                # Do something with the comment
                comment_list.append(comment.body)
                c.execute('INSERT INTO comment_list VALUES (?)', (comment.body,))
        conn.commit()
        return comment_list

def count_words(comment_list):
    word_count = {}
    
    for comment in comment_list:
        words = comment.split()
        
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
            c.execute('INSERT INTO word_count VALUES (?, ?)', (word, word_count[word]))
    conn.commit()
    return word_count


if __name__ == '__main__':
    comment_list = scrape_comments(subreddit_list, num_posts, num_comments)
    word_count = count_words(comment_list)
    print("Saved to database!")
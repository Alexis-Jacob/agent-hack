import redditwarp.SYNC
from redditwarp.SYNC import Client
from redditwarp.models.submission import Submission
from redditwarp.models.comment import Comment

from smolagents import tool

client = redditwarp.SYNC.Client()

def _post_to_dict(post:Submission) -> dict:
    """
    Converts a Reddit post object to a dictionary.
    
    Args:
        post (redditwarp.SYNC.models.submission_SYNC.Submission): The Reddit post object.
        
    Returns:
        dict: A dictionary representation of the post.
    """
    return {
        'title': post.title,
        'author': post.author.name if post.author else 'deleted',
        # 'id': post.id,
        'id36': post.id36,
        'url': post.permalink,
        'score': post.score,
        'created_utc': post.created_at,
        'subreddit': post.subreddit.name,
    }

@tool
def per_sub_top_posts(subreddit : str, limit : int =50) -> list:
    """
    Fetches the top posts from a specific subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to fetch posts from.
        limit (int): The maximum number of posts to return.
        
    Returns:
        list: A list of top posts from the specified subreddit.
    """
    posts = client.p.subreddit.pull.top(subreddit, amount=limit)
    return [_post_to_dict(post) for post in posts]

@tool
def user_info(username: str) -> dict:
    """
    Fetches user information for a given username.
    
    Args:
        username (str): The Reddit username to fetch information for.
        
    Returns:
        dict: A dictionary containing user information.
    """
    user = client.p.user.fetch_by_name(username)
    if not user:
        return None  # User not found or suspended
    return {
        'name': user.name,
        'id36': user.id36,
        'created_utc': user.created_at,
        'post_karma': user.post_karma,
        'comment_karma': user.comment_karma,
        'total_karma': user.total_karma,
        'is_suspended': user.awardee_karma,
    }

@tool
def user_posts(username: str, limit:int=50) -> list:
    """
    Fetches posts made by a specific user.
    
    Args:
        username (str): The Reddit username to fetch posts for.
        limit (int): The maximum number of posts to return.
        
    Returns:
        list: A list of posts made by the specified user.
    """
    user = client.p.user.fetch_by_name(username)
    if not user:
        return []  # User not found or suspended
    posts = client.p.user.pull.submitted(username, amount=limit, sort='new')
    return [_post_to_dict(post) for post in posts]

def _comment_to_dict(comment: Comment) -> dict:
    """
    Converts a Reddit comment object to a dictionary.
    
    Args:
        comment (redditwarp.SYNC.models.comment_SYNC.Comment): The Reddit comment object.
        
    Returns:
        dict: A dictionary representation of the comment.
    """
    return {
        'body': comment.body,
        'author': comment.author.name if comment.author else 'deleted',
        'id36': comment.id36,
        'score': comment.score,
        'created_utc': comment.created_at,
        'subreddit': comment.subreddit.name,
    }

@tool
def user_comments(username: str, limit: int=50) -> list:
    """
    Fetches comments made by a specific user.
    
    Args:
        username (str): The Reddit username to fetch comments for.
        limit (int): The maximum number of comments to return.
        
    Returns:
        list: A list of comments made by the specified user.
    """
    user = client.p.user.fetch_by_name(username)
    if not user:
        return []  # User not found or suspended
    comments = client.p.user.pull.comments(username, amount=limit, sort='new')
    return [_comment_to_dict(comment) for comment in comments]

if __name__ == "__main__":
    subreddit_name = "learnpython"
    top_posts = per_sub_top_posts(subreddit_name, limit=50)
    for post in top_posts:
        print(post)
    
    user_name = "fonisuno"
    user_info_data = user_info(user_name)
    if user_info_data:
        print(user_info_data)
    else:
        print(f"User {user_name} not found or suspended.")

    userposts = user_posts(user_name, limit=50)
    if userposts:
        for post in userposts:
            print(post)

    usercomments = user_comments(user_name, limit=50)
    if usercomments:
        for comment in usercomments:
            print(comment)
    else:
        print(f"No comments found for user {user_name}.")


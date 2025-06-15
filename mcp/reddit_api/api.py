import redditwarp.SYNC
from redditwarp.SYNC import Client
from redditwarp.models.submission import Submission
from redditwarp.models.comment import Comment
from datetime import datetime
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("MCP")

# from smolagents import tool

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

@mcp.tool()
def per_sub_top_posts(subreddit : str, limit : int =50) -> list:
    """
    Fetches the top posts from a specific subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to fetch posts from.
        limit (int): The maximum number of posts to return.
        time (str): The time period for which to fetch top posts. Default is "now". If you want to fetch posts from a specific time period, you can use "day", "week", "month", "year", or "all".
        
    Returns:
        list: A list of top posts from the specified subreddit.
    """
    posts = client.p.subreddit.pull.top(subreddit, amount=limit)
    return [_post_to_dict(post) for post in posts]

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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


def _traverse_nodes(tree_node):
    """Yield each TreeNode in the comment tree."""
    yield tree_node.value
    for child in tree_node.children:
        yield from _traverse_nodes(child)

@mcp.tool()
def get_n_best_comments(post_id36: str, n_comments: int) -> List[Dict[str, Any]]:
    """
    Retrieves the top N best comments for a given post.
    Args:
        post_id36 (str): The base36 ID of the post to fetch comments from.
        n_comments (int): The number of top comments to retrieve.
    Returns:
        list[dict]: A list of dictionaries, each containing information about a comment:
            - author (str): The display name of the comment's author.
            - score (int): The score of the comment.
            - text (str): The body text of the comment.
            - created_at (datetime): The creation time of the comment as a datetime object.
    """

    tree = client.p.comment_tree.fetch(post_id36, sort="top", limit=n_comments, depth=1)
    first_generation_comments: List[Dict[str, Any]] = []
    for cm in _traverse_nodes(tree):
        first_generation_comments.append({
            "author": cm.author_display_name,
            "score": cm.score,
            "text": cm.body,
            "created_at": datetime.fromtimestamp(cm.created_ut)
        })
    return first_generation_comments


if __name__ == "__main__":
    subreddit_name = "learnpython"
    top_posts = per_sub_top_posts(subreddit_name, limit=50)
    for post in top_posts:
        print(post)

    for post in top_posts:
        print(get_n_best_comments(post["id36"], 2))
        break   
    
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


from smolagents import tool
import redditwarp.SYNC as rw
from datetime import datetime
from typing import List, Dict, Any

client = rw.Client()


def traverse_nodes(tree_node):
    """Yield each TreeNode in the comment tree."""
    yield tree_node.value
    for child in tree_node.children:
        yield from traverse_nodes(child)

@tool
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
    for cm in traverse_nodes(tree):
        first_generation_comments.append({
            "author": cm.author_display_name,
            "score": cm.score,
            "text": cm.body,
            "created_at": datetime.fromtimestamp(cm.created_ut)
        })
    return first_generation_comments


if __name__ =="__main__":
    m = next(client.p.subreddit.pull.top("YouShouldKnow", amount=1, time="week"))
    best_comments = get_n_best_comments(m.id36, n_comments=10)
    
    for top_comment in best_comments[:1]:
        print(top_comment)
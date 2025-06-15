"""
id36: The comment’s Reddit ID, in base-36 (e.g. "g7x1ab").
id: Same ID in integer form (parsed from base‑36).
created_at: Timestamp as a datetime.datetime (UTC).
created_ut: Unix timestamp (integer seconds since epoch).
body: The full text content of the comment.
score: Net upvotes (upvotes minus downvotes).
author_display_name: The comment author's username (without u/).
is_edited: bool—True if the comment has been edited.
parent_id36: Base‑36 ID of the parent (a submission or comment).
subreddit.name: Subreddit name (without r/).
subreddit_id36 / subreddit_id: Subreddit ID in base‑36 or integer.
submission.id36: ID of the parent submission.
permalink: Full URL path to the comment.
"""
import redditwarp.SYNC as rw


client = rw.Client()
# 1. Fetch the post
m = next(client.p.subreddit.pull.top("YouShouldKnow", amount=1, time="week"))

# 2. Retrieve comment tree, sorted by top, limit to 1
tree = client.p.comment_tree.fetch(m.id36, sort="top", limit=1)

# 3. Get top comment from the fetched tree
top_comment = tree.children[0].value

# 4. Inspect comment
print(f"Comment ID: {top_comment.id36}")
print(f"Author: u/{top_comment.author_display_name}")
print(f"Score: {top_comment.score}")
print(f"Body: {top_comment.body}")
import redditwarp.SYNC

client = redditwarp.SYNC.Client()
# Display the top submission of the week in the r/YouShouldKnow subreddit.
latest = list(client.p.subreddit.pull.new("YouShouldKnow", amount=50))

# for post in latest:
#     print(f"{post.created_utc=} | {post.id36} | {post.title}")
#     m = next(client.p.subreddit.pull.new('YouShouldKnow', amount=5))

"""
id36: Base‑36 Reddit ID (e.g. '5e1az9').
id: Same ID in integer format, decoded from base‑36.
title: The post title string.
score: Net upvote count (upvotes minus downvotes).
permalink: Path to the post (e.g. '/r/python/comments/...'). Combine with https://reddit.com to form a full URL.
created_at / created_utc: Timestamp of submission (typically a datetime.datetime object in UTC).
is_edited: bool — True if the post has been edited.
author_display_name: The Reddit handle of the poster (e.g. 'Pyprohly').
subreddit.name: Short subreddit name, without the r/ prefix.
subreddit: A Subreddit model, from which you can get other details like its ID or subscriber count.
"""

# => make a dictionnary out of it 


for m in latest:
    print(f'''\
    {m.permalink}
    {m.id36}+ ^{m.score} | {m.title}
    Submitted {m.created_at.astimezone().ctime()}{' *' if m.is_edited else ''} \
    by u/{m.author_display_name} to r/{m.subreddit.name}
    ''')

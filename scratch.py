from smolagents import CodeAgent, InferenceClientModel, Tool, Model, PromptTemplates

from pandas import DataFrame

from reddit_api import api as reddit_api
import retrieval_agent as ra

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel(bill_to="Agents-Hack")  # Uses a default model

api_tools = [
    reddit_api.per_sub_top_posts,
    reddit_api.per_sub_sample_new_posts,
    reddit_api.user_info,
    reddit_api.user_posts,
    reddit_api.user_comments,
]

# Create an agent with no tools
agent = ra.RetrievalAgent(tools=api_tools, model=model)

# Run the agent with a task
result = agent.run("Find the 5 most popular authors of posts in the r/politics subreddit, and return their names and post counts, and the top 5 posts in a DataFrame.")
print(result)
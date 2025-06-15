from smolagents import CodeAgent, Tool, Model, PromptTemplates, ToolCollection

from pandas import DataFrame

class RetrievalAgent(CodeAgent):
    """
    An agent that retrieves information from a subreddit.
    """

    def __init__(self, *args, **kwargs):
        super(RetrievalAgent, self).__init__(*args, additional_authorized_imports=["pandas", "pandas.*", "json"], **kwargs)

    def run(self, query: str) -> str:
        """
        Run the agent with a given query.
        """

        out_df = DataFrame()
        response = super().run("While processing the following request, work with a DataFrame called working_df. When you are done, convert the dataframe to json with working_df.to_json, and return it. " + query,)
        return out_df

    


class OpinionatedRetrievalAgent(RetrievalAgent):
    """
    An agent that retrieves information from a knowledge base with an opinionated model.
    """

    def __init__(self, knowledge_base, opinion_model):
        super().__init__(knowledge_base)
        self.opinion_model = opinion_model
        raise NotImplementedError()

    def retrieve_and_opine(self, query):
        """
        Retrieve relevant information and provide an opinionated response.
        """
        raise NotImplementedError()
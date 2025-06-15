from smolagents import CodeAgent, Tool, Model, PromptTemplates, ToolCollection

from pandas import DataFrame

class RetrievalAgent(CodeAgent):
    """
    An agent that retrieves information from a subreddit.
    """

    def __init__(self, tools: list[Tool], model: Model, prompt_templates: PromptTemplates | None = None):
        super(RetrievalAgent, self).__init__(tools=tools, model=model, prompt_templates=prompt_templates, additional_authorized_imports=["pandas", "pandas.*"])

    def run(self, query: str) -> str:
        """
        Run the agent with a given query.
        """

        out_df = DataFrame()
        response = super().run("You cannot assign to output_df, you can only write to it through dataframe methods. " + query, additional_args={
            "output_df": out_df
        })
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
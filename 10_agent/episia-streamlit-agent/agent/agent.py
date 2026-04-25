"""
EpisiaAgent — LangChain ReAct agent powered by Groq LPU.
Fast, validated epidemiological reasoning for sub-Saharan Africa.
"""

import os
from typing import Generator
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from .tools import ALL_TOOLS
from .prompts import SYSTEM_PROMPT

load_dotenv()


#  Available Groq models 
GROQ_MODELS = {
    "llama-3.3-70b-versatile":  "Llama 3.3 70B · Best quality",
    "llama3-groq-70b-8192-tool-use-preview": "Llama 3 70B · Tool-use optimized",
}


#  EpisiaAgent class 
class EpisiaAgent:
    """
    Epidemiology AI agent using LangChain tool-calling + Groq LPU.
    
    Usage:
        agent = EpisiaAgent(model="llama-3.3-70b-versatile")
        response = agent.run("Sample size for RR=2, baseline risk 10%, power 80%?")
        print(response)
    """

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.0,
        max_iterations: int = 5,
        verbose: bool = False,
    ):
        self.model_name = model
        self.verbose    = verbose

        # LLM via Groq
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY"),
            max_retries=2,
        )

        # Prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])

        # Agent + executor
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=ALL_TOOLS,
            prompt=self.prompt,
        )
        self.executor = AgentExecutor(
            agent=agent,
            tools=ALL_TOOLS,
            verbose=verbose,
            max_iterations=max_iterations,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

        # Conversation history
        self.history: list = []

    def run(self, user_input: str) -> dict:
        """
        Run the agent on a user query.
        
        Returns:
            dict with keys:
                - answer: str (final agent response)
                - tools_used: list of tool names called
                - steps: intermediate reasoning steps
        """
        result = self.executor.invoke({
            "input": user_input,
            "chat_history": self.history,
        })

        # Update history
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=result["output"]))

        # Extract tools used
        tools_used = []
        for step in result.get("intermediate_steps", []):
            if hasattr(step[0], "tool"):
                tools_used.append(step[0].tool)

        return {
            "answer":     result["output"],
            "tools_used": tools_used,
            "steps":      result.get("intermediate_steps", []),
        }

    def stream(self, user_input: str) -> Generator[str, None, None]:
        """
        Stream the agent response token by token.
        Yields text chunks as they are generated.
        """
        # Stream via LLM directly for UI responsiveness
        for chunk in self.executor.stream({
            "input": user_input,
            "chat_history": self.history,
        }):
            if "output" in chunk:
                yield chunk["output"]

    def reset(self):
        """Clear conversation history."""
        self.history = []

    def get_history(self) -> list:
        """Return conversation history as list of (role, content) tuples."""
        return [
            ("user" if isinstance(m, HumanMessage) else "assistant", m.content)
            for m in self.history
        ]

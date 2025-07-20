from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

load_dotenv()

# open_ai_model = ChatOpenAI(model="gpt-4o-mini")
# groq_model = ChatGroq(model="llama-3.1-8b-instant")
# travil_search = TavilySearch(max_results=5)
# custom_prompt = "You are a helpful AI assistant friendly and knowledgeable. " 
def create_agent(llm_id,llm_provider,search_result, query, system_prompt):
    """
    Create a React agent with the specified model and tools.
    """
    if llm_provider == "GROQ":
        llm = ChatGroq(model=llm_id)
    elif llm_provider == "OPENAI":
        llm = ChatOpenAI(model=llm_id)

    # Create the React agent with the specified model and tools
    tools = [TavilySearch(max_results=5) if search_result else []  ]
    agent = create_react_agent(
        model = llm,
        tools=tools,
        prompt=system_prompt,

    )

    # query = "Give me lastest update of crypto market BTC IN LAST FEW DAYS PRICES AND PROFIT"
    state = {"messages":query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages =[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]

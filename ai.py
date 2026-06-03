from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str] = Field(default_factory=list)
    tools_used: list[str] = Field(default_factory=list)


llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=(
        "You are a research assistant that helps generate research-style answers. "
        "Return the answer in the required structured format."
    ),
    response_format=ResearchResponse,
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "WHos is the strongest armwrestler currently?"}]
})

try: 
    print(result["structured_response"].model_dump())
except Exception as e:
    print("Error parsing response", e)
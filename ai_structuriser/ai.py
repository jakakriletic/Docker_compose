from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import httpx
import json

load_dotenv()
getdata = httpx.get('http://api:80/company/getdata')


companies = getdata.json()

class strukturised(BaseModel):
    company_name: str = Field(description="Ime podjetja, omenjeno v besedilu.")
    ceo: str | None = Field(default=None, description="Ime direktorja oziroma CEO-ja podjetja.")
    founded_year: int | None = Field(default=None, description="Leto, ko je bilo podjetje ustanovljeno.")
    industry: str | None = Field(default=None,description="Glavna panoga podjetja, npr. IT, logistika, energetika, proizvodnja, marketing.")
    main_activity: str | None = Field(default=None,description="Kratek opis glavne dejavnosti podjetja.")

llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt = """
        You are an information extraction assistant.

        Your task is to read a noisy, bloated company description and extract only the relevant structured business information.

        Extract the following fields:

        company_name: the official company name mentioned in the text
        ceo: the CEO, director, or main leading person of the company
        founded_year: the year when the company was founded
        industry: the main business sector or industry of the company
        main_activity: a short description of what the company mainly does
        summary: a short clean summary of the company based only on the provided text

        Rules:

        Use only information that is present in the input text.
        Do not invent missing information.
        If a field is not clearly available, return null for that field.
        founded_year must be an integer if available.
        Keep main_activity short and factual.
        Ignore marketing language, filler text, repeated sentences, and vague promotional wording.
        Return the result strictly in the requested structured format.
        """,
    response_format=strukturised,
)
for company in companies:
    user_prompt = f"""
        Extract structured company information from the following JSON-like input.

        Company label:
        {company["company"]}

        Description text:
        {company["text"]}
    """
    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    })
    strukturirano = result["structured_response"]
    postdata = httpx.post('http://api:80/company/saveDb', json=strukturirano.model_dump())

    print(strukturirano)
    postdata

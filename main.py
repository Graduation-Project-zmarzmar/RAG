import os
from dotenv import load_dotenv
from Bio import Entrez
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. 환경 변수 로드 
load_dotenv()

# 2. PubMed 설정
Entrez.api_key = os.getenv("PUBMED_API_KEY")
Entrez.email = "zmarzmzm@naver.com" 

def search_and_summarize(query):
    print(f"🔎 '{query}' 관련 최신 논문을 찾는 중...")
    
    # PubMed 검색 (최신 1건)
    handle = Entrez.esearch(db="pubmed", term=query, retmax=10)
    record = Entrez.read(handle)
    handle.close()
    
    if not record["IdList"]:
        print("논문을 찾을 수 없습니다.")
        return

    pmid = record["IdList"][0]
    
    # 논문 상세 정보(초록) 가져오기
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
    abstract_text = handle.read()
    handle.close()
    
    print(f"📄 논문(PMID: {pmid}) 분석 중...\n")

    # 3. LangChain을 이용한 요약 에이전트 설정
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 생명공학 전문 연구 보조원입니다. 다음 논문 초록을 읽고 1) 연구 목적, 2) 주요 방법론, 3) 핵심 결과를 한국어로 요약하세요."),
        ("user", "{context}")
    ])
    
    # 실행 (Chain 구성)
    chain = prompt | llm
    response = chain.invoke({"context": abstract_text})
    
    print("=== 논문 요약 결과 ===")
    print(response.content)

if __name__ == "__main__":
    # 테스트 키워드
    search_and_summarize("CRISPR gene editing efficiency")
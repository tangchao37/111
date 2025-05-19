from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

load_dotenv()

def get_openai_chain():
    """Builds an LLMChain using OpenAI's model"""
    prompt = PromptTemplate.from_template("Answer this: {question}")
    # key=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

    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    return LLMChain(llm=llm, prompt=prompt)

def get_deepseek_chain():
    """Builds an LLMChain using DeepSeek's model"""
    prompt = PromptTemplate.from_template("Answer this: {question}")
    llm = ChatDeepSeek(api_key=os.getenv("DEEPSEEK_API_KEY"), model="deepseek-chat")
    return LLMChain(llm=llm, prompt=prompt)

def get_chain_by_model(model_name: str):
    """根据指定的模型名称，构建对应的LLMChain"""
    if model_name.lower() == "openai":
        return get_openai_chain()
    elif model_name.lower() == "deepseek":
        return get_deepseek_chain()
    else:
        raise ValueError("不支持的模型名称。目前仅支持'OpenAI'和'DeepSeek'。")

if __name__ == "__main__":
    model_choice = input("请选择模型（OpenAI/DeepSeek）: ").strip()
    question = input("请输入你的问题: ").strip()

    try:
        chain = get_chain_by_model(model_choice)
        response = chain.run({"question": question})
        print(f"\n[回答]:\n{response}")
    except ValueError as e:
        print(f"错误: {e}")

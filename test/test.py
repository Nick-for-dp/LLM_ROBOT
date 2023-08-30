import os
from utils.AuthorizationUtils import generate_authorization_url
from utils.Config import XF_API_ADDRESS
# 设置本地代理
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"


if __name__ == '__main__':
    # llm = OpenAI(temperature=0.5)
    # question = "我女朋友有一只可爱的灰白色小猫，小猫的头上有八二分的灰色斜刘海，她的尾巴是全灰的，请给她起个名字。"
    # print("chatGPT is thinking...")
    # print(llm(question))
    print(generate_authorization_url())

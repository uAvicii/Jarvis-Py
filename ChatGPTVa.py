import openai
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量中获取OpenAI API密钥
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY


def SpeakText(command):
    engine = pyttsx3.init()

    # 设置语速和音量
    engine.setProperty('rate', 180)  # 增加语速到180
    engine.setProperty('volume', 0.8)  # 设置音量到0.8

    engine.say(command)
    engine.runAndWait()


# Initialize the recognizer
r = sr.Recognizer()


def record_text():
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # 准备麦克风，以便接收输入
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("我在听着...")
            # 监听用户的输入
            audio2 = r.listen(source2)
            # 使用Google进行语音识别
            MyText = r.recognize_google(audio2, language="zh-CN")
            return MyText

    except sr.RequestError as e:
        print("无法请求结果: {0}".format(e))

    except sr.UnknownValueError:
        print("发生未知错误")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    reply_content = response.choices[0].message['content']
    return reply_content


if __name__ == "__main__":
    messages = [{
        "role": "system",
        "content": "You are at a party."
    }]

    while True:
        text = record_text()
        messages.append({
            "role": "user",
            "content": text
        })

        response = send_to_chatGPT(messages)
        SpeakText(response)
        print(response)

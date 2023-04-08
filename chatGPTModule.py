import openai
import keys 

model_engine = "text-davinci-003" 

def get_chatgpt_results(text):
    try:
        openai.api_key = keys.PATH_OPENAI
        completion = openai.Completion.create(engine=model_engine, prompt=text, max_tokens=1024, n=1, stop=None, temperature=0.5,)
        response = completion.choices[0].text
        print(response)
        return response
    except Exception as e:
        print(e)
        print("Unable to fetch data from chatgpt")
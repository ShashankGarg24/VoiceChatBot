import openai


openai.api_key = "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" 

model_engine = "text-davinci-003" 

prompt = "how can we code in java"

completion = openai.Completion.create( 
engine=model_engine,
 prompt=prompt,
 max_tokens=1024,
 n=1,
 stop=None,
 temperature=0.5,
 )

response = completion.choices[0].text
print(response)
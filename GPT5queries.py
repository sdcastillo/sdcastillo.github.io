
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    #Read the official documentation for all the settings here!
    model="gpt-5",
    #Input text prompt here
    #other formats, documents, files, that's for another time.
    input= 
)

# Print the result to the console
print(response.output_text)

# Write the result to a text file called "query_logs.txt"
with open("query_logs.txt", "a", encoding="utf-8") as f:
    f.write(response.output_text + "\n")




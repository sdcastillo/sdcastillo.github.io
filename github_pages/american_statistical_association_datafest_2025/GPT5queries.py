
from openai import OpenAI

client = OpenAI()


response = client.responses.create(
    #Read the official documentation for all the settings here!
    model="gpt-5.1",
    #Input text prompt here
    #other formats, documents, files, that's for another time.
    #input="testing22",
)

response = client.responses.create(
    #Read the official documentation for all the settings here!
    model="gpt-5.1",
    #Input text prompt here
    #other formats, documents, files, that's for another time.
    input="Write Christmas happy holidays posts for my facebook, instagram, linkedin, X, personal website, substack, etc.  Today is 12 16, so schedule them out every day until christmas.  About me: from Massachusetts, a New Englander who enjoys Dunkin Donuts and Chill holiday music.  I play guitar and enjoy puzzles.",
)

# Print the result to the console
print(response.output_text)

# Write the result to a text file called "query_logs.txt"
with open("query_logs.txt", "a", encoding="utf-8") as f:
    f.write(response.output_text + "\n")


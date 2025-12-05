
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    #Read the official documentation for all the settings here!
    model="gpt-5",
    #Input text prompt here
    #other formats, documents, files, that's for another time.
    input="Help me do background on my ancestry.  I have a family tree that is series of 24 images of pdf pages (page_1.png ,,, page_24.png.  goes back hundreds of years, saved in the local direcotry as CASTILLO ILLING FAMILY TREE.PDF.  Using open source tools, help me draw or make a nested data format of the tree that i can use to visualize the tree.  i have python 3 installed on windows machine and tesseract 86 win. ",
)

# Print the result to the console
print(response.output_text)

# Write the result to a text file called "query_logs.txt"
with open("query_logs.txt", "a", encoding="utf-8") as f:
    f.write(response.output_text + "\n")



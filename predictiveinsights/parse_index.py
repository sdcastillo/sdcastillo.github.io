#openaikey = "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"

from openai import OpenAI

client = OpenAI()

# Step 1: Read the OCR output
with open("C:/Users/casti/Downloads/futuroinsights-main/futuroinsights-main/index.html", "r", encoding="utf-8") as f:
    webpage = f.read()

# Step 2: Send to GPT-5 to parse into JSON
prompt = (
    "Parse the following website page which is html to improve it and clarify the messaging. "
    "There should be a header on the top with links to other pages on site: contact.html, buy.html, code.html,, privacy.html, terms.thml, studymanual,html, and home (which goes back to index.thml). "
    "This page has all accurate information, however the webdeveloper has not yet formatted and made the page awesthetically pleasing.  Please do the web development to enhance the readability of the webpage, by taking liberty to move parts around, to make the data science sexy.  You can insert image placeholders as well, of me, or of groups, or of charts and graphs.  For personal privacy, omit details which would pose a security risk to me or make complications with my past employers (conflicts of interest).\n\n"
    f"{webpage}"
)

response = client.responses.create(
    model="gpt-5",
    input=prompt,
)

# Print the JSON result to the console
print(response.output_text)

# Save the html to a file for 
with open("sam_main_page.json", "w", encoding="utf-8") as f:
    f.write(response.output_text)

# Optionally, log the query
with open("query_logs.txt", "a", encoding="utf-8") as f:
    f.write(response.output_text + "\n")
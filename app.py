import google.generativeai as genai

genai.configure(api_key="AIzaSyDVq-g2PRh94HK11l2SzBT7dvwy6j0TrPs")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)


import google.generativeai as genai 
genai.configure(api_key="AIzaSyBaoUy174ZGSU1trY9UuNSRK-s07RsOBOw")
model=genai.GenerativeModel(model_name="gemini-2.5-flash")
while(True):
    prompt=input("USER : ")
    response=model.generate_content(prompt).text
    print("GEMINI : ",response)
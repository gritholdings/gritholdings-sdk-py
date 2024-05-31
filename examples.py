import gritholdings

browser_automation = gritholdings.resource('BrowserAutomation')
local_db = gritholdings.resource('LocalDB')

openai_llm = gritholdings.resource('LLM', adapter_type='openai').adapter

# This will cost you openai credits
# response = openai_llm.chat('What is the meaning of life?')
# print(response)

# Must have gmail_api_credentials.json with project_id, auth_uri, token_uri, .. added
# gmail_api = gritholdings.resource('GmailAPI', partner_name='user@example.com')
import gritholdings

browser_automation = gritholdings.resource('BrowserAutomation')
local_db = gritholdings.resource('LocalDB')

openai_llm = gritholdings.resource('LLM', adapter_type='openai').adapter
response = openai_llm.chat('What is the meaning of life?')
print(response)
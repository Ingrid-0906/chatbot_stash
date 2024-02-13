# chatbot_market_intent

vectorstore:
- file that scrape the website links and extracts the text from each one to create a local vectorstore.

support_agent:
- file that generate the chatbot.

Note.
- Need to host a virtual machine on aws to host chromadb.
- Need create a mongodb small database to storage the user section: date_released, company_id and namespace and settings.
- Need create another mongodb small database to storage the chat history (? Optional - the company will pay for an analysis ?)

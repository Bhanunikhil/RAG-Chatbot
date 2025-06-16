import src.scraper as scraper
import src.pdf_ingest as pdf_ingest
import src.index_and_embed as index_and_embed
import src.rag as rag

# scraper.main()
# pdf_ingest.main()
# index_and_embed.main()

print("RAG chatbot initialized. Type your question or 'exit' to quit.")
while True:
    user_q = input("Question: ")
    if not user_q or user_q.lower() in ("exit", "quit"):
        break
    ans = rag.answer_with_rag(user_q)
    print(f"Answer: {ans}\n")
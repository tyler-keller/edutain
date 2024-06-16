import ollama
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

with open('output/deep-learning-chapters-latex/chapter005.md', 'r') as file:
  lines = file.readlines()
  text = ''.join(lines)
  tokens = tokenizer.tokenize(text)
  num_tokens = len(tokens)
  print(f"Number of tokens in your text: {num_tokens}")

  split_tokens = [tokens[i:i+6144] for i in range(0, num_tokens, 6144)]

  for i, split_token in enumerate(split_tokens):

    # decode the tokens
    chapter_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(split_token))

    stream = ollama.chat(
        model='llama3',
        messages=[
          {'role': 'system', 'content': '''You are an AI assistant that summarizes book content into flashcards. 
           The user will give pieces of the book. You are to take those pieces and identify key topics. 
           Only output the chapter\'s content in YAML formatted flashcards. They should be in the format of:
           ```yaml
           - front: "What is the capital of France?"
             back: "Paris"
           - front: "What is the capital of Spain?"
             back: "Madrid"
           ```
           '''},
          {'role': 'user', 'content': f'''# **Book**: Deep Learning
           ## **Chapter**: Machine Learning Basics
           **Text**: {chapter_text}'''},
        ],
        stream=True,
    )

    for chunk in stream:
      print(chunk['message']['content'], end='', flush=True)

# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   response_format="json",
#   messages=[
#     {"role": "system", "content": "You are an AI assistant helping a user retain the knowledge that they're learning in their book. The student asks you for help with their homework. Here is the student's question:"},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)
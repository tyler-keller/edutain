import ollama
from transformers import AutoTokenizer
import os
import sys


system_message = '''You are an AI assistant that summarizes book content into flashcards.
The user will give you pieces of the book in an unclean markdown format. 
You are to take those pieces, identify key topics and return the most important concepts in flashcard format.
Only output the formatted flashcards. Your responses should be in the following format:
```json
[
    {
        "front": "What is the capital of France?",
        "back": "Paris"
    },
    {
        "front": "What is the capital of Spain?",
        "back": "Madrid"
    }
]
```
'''


def get_llama3_gradient_flashcards(text, book_title, chapter_title):
      stream = ollama.chat(
          model='llama3-gradient:latest',
          messages=[
              {'role': 'system', 'content': system_message},
              {'role': 'user', 'content': f'''# **Book**: {book_title}
              ## **Chapter**: {chapter_title}
              Chapter Text: 
              {text}
              '''},
          ],
          stream=True,
          options={
              'temperature': 0.01,
              'num_ctx': 100_000,
          }
      )

      for chunk in stream:
          print(chunk['message']['content'], end='', flush=True)



def get_llama3_flashcards(text, book_title, chapter_title):
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    llama3_context = 8048

    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)
    print(f"Number of tokens in your text: {num_tokens}")

    split_tokens = [tokens[i:i+(llama3_context-1024)] for i in range(0, num_tokens, (llama3_context-1024))]
    split_texts = [tokenizer.convert_tokens_to_string(split_token) for split_token in split_tokens]

    for i, chapter_text in enumerate(split_texts):
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': f'''# **Book**: {book_title}
                ## **Chapter**: {chapter_title}
                **Text**: {chapter_text}'''},
            ],
            stream=True,
            options={
                'temperature': 0,
                'num_ctx': llama3_context,
            }
        )

        print(response['message']['content'])

        


if __name__ == '__main__':
  book_title = 'deep-learning'
  chapter_title = 'chapter-1'

  input_dir = 'output/deep-learning-chapters'
  output_dir = 'output/deep-learning-llama3'

  files = os.listdir(input_dir)

  for file_name in files:
    with open(f'{input_dir}/{file_name}', 'r') as file:
      lines = file.readlines()
      text = ''.join(lines)
      get_llama3_flashcards(text, book_title, chapter_title)
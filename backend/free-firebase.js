import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyC_d7DFaGaSLU1VyPNYeFruraAYqLXYS3o",
  authDomain: "tylerkeller-dev.firebaseapp.com",
  databaseURL: "https://tylerkeller-dev-default-rtdb.firebaseio.com",
  projectId: "tylerkeller-dev",
  storageBucket: "tylerkeller-dev.appspot.com",
  messagingSenderId: "808076940727",
  appId: "1:808076940727:web:c6c66dace3e38accd28432",
  measurementId: "G-1TMS1SJ4VY"
};

const app = initializeApp(firebaseConfig);

import { initializeApp } from "firebase/app";
import { getVertexAI, getGenerativeModel } from "firebase/vertexai-preview";

const firebaseApp = initializeApp(firebaseConfig);

const vertexAI = getVertexAI(firebaseApp);

const model = getGenerativeModel(vertexAI, {
    model: "gemini-1.5-flash",
    systemInstruction: `You are an AI assistant that summarizes book content into flashcards. 
    The user will give a chapter of the book at a time. 
    You are to take those chapters, identify key topics and generate flashcard material. 
    You will come up w/ a name for the chapter given the content, most of the time the chapter text will contain the chapter title. 
    You will only output YAML formatted flashcards. 
    Your flashcard YAML content should be in the following format:
    \`\`\`yaml
    - chapter: Introduction
        questions:
        - question: What is deep learning?
            answer: Deep learning is an approach to artificial intelligence (AI) that uses a hierarchy of concepts, with each concept defined through its relation to simpler concepts. This allows computers to learn from experience and understand the world in a more intuitive way.
        - question: Why is deep learning becoming more popular now?
            answer: Deep learning has been around for decades, but recent advancements in computing power, larger datasets, and improved training algorithms have made it a more viable and powerful technology.
        - question: What are some of the historical trends in deep learning?
            answer: Deep learning has been known by different names throughout its history, such as cybernetics, connectionism, and artificial neural networks. It has gained popularity as the amount of available training data has increased and the size of deep learning models has grown due to advancements in computer infrastructure.
    \`\`\``
});

async function run() {
    const chat = model.startChat({
      history: [
        {
          role: "user",
          parts: [{ text: "Hello, I have 2 dogs in my house." }],
        },
        {
          role: "model",
          parts: [{ text: "Great to meet you. What would you like to know?" }],
        },
      ],
      generationConfig: {
        maxOutputTokens: 100,
      },
    });
  
    const msg = "How many paws are in my house?";
    const result = await chat.sendMessageStream(msg);
  
    let text = '';
    for await (const chunk of result.stream) {
      const chunkText = chunk.text();
      console.log(chunkText);
      text += chunkText;
    }
}
  
run();
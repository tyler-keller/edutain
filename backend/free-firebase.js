import { initializeApp } from "firebase/app";
import { getVertexAI, getGenerativeModel } from "firebase/vertexai-preview";
import fs from 'fs';
import path from 'path';

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

const firebaseApp = initializeApp(firebaseConfig);

const vertexAI = getVertexAI(firebaseApp);

const model = getGenerativeModel(vertexAI, {
    model: "gemini-1.5-flash",
    systemInstruction: `You are an AI assistant that summarizes book content into flashcards. 
    The user will give a chapter of the book at a time. 
    You are to take those chapters, identify key topics and generate flashcard material. 
    You will come up w/ a name for the chapter given the content, most of the time the chapter text will contain the chapter title. 
    You will only output YAML formatted flashcards. Output 5-10 flashcards per chapter depending on the content.
    Your flashcard YAML content should be in the following format:
    \`\`\`yaml
    - chapter: Introduction
        cards:
        - front: What is deep learning?
          back: Deep learning is an approach to artificial intelligence that uses a hierarchy of concepts, with each concept defined through its relation to simpler concepts. This allows computers to learn from experience and understand the world in a more intuitive way.
        - front: Why is deep learning becoming more popular now?
          back: Deep learning has been around for decades, but recent advancements in computing power, larger datasets, and improved training algorithms have made it a more viable and powerful technology.
    \`\`\``
});

async function processFile(filePath, outputDir) {
  const fileContents = fs.readFileSync(filePath, 'utf8');

  const chat = model.startChat({
    generationConfig: {
      maxOutputTokens: 1024,
    },
  });

  const msg = fileContents;
  const result = await chat.sendMessageStream(msg);

  let text = '';
  for await (const chunk of result.stream) {
    const chunkText = chunk.text();
    console.log(chunkText);
    text += chunkText;
  }

  // Optionally, save the output to a file
  // const outputFilePath = path.join(outputDir, `raw_output/${filePath.replace('.md', '')}_full_output.txt`);
  // fs.writeFileSync(outputFilePath, text);
  
  const yamlMatch = text.match(/```yaml([\s\S]*?)```/);
  if (yamlMatch && yamlMatch[1]) {
      const yamlContent = yamlMatch[1].trim();
      const outputFilePath = path.join(outputDir, `${path.basename(filePath).replace('.md', '')}.yaml`);
      fs.writeFileSync(outputFilePath, yamlContent);
  }
}

async function run() {
  const directoryPath = path.resolve('./output/deep-learning-chapters/');
  const outputDir = path.resolve('./output/deep-learning-gemini/');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const files = fs.readdirSync(directoryPath);

  for (const file of files) {
      if (file.includes('chapter') && file.endsWith('.md')) {
          const filePath = path.join(directoryPath, file);
          await processFile(filePath, outputDir);
      }
  }
}

run();
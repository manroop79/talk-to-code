import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
    timeout: 10000,
});

(async () => {
    try {
        const result = await openai.embeddings.create({
            model: "text-embedding-3-small",
            input: "hello world",
        });
        console.log("Embedding:", result.data[0].embedding.length);
    } catch (error) {
        console.error("Error generating embedding:", error);
    }
})();
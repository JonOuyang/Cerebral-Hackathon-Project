require('dotenv').config();

const test = process.env.GEMINI_API_KEY;

console.log(test)

const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-002" });

console.log(model)


const prompt = "How are you doing today?";
// const image = {
//     inlineData: {
//         data: Buffer.from(fs.readFileSync("cookie.png")).toString("base64"),
//         mimeType: "image/png",
//     },
// };

const result = model.generateContent([prompt]);
console.log(result.response);
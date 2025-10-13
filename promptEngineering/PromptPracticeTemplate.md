# Prompt Engineering Practice Templates

A comprehensive collection of prompt templates for various AI interactions and use cases.

## A. Basic Prompt Templates

### 1. General Inquiry
**Template:** Ask a general question about a topic
**Example:**
> Explain advantage of living a life in simple terms.

### 2. Summarization
**Template:** Summarize text in specific format/length
**Example:**
> Summarize the following text in 5 bullet points:
> 
> *Madurai, often called the Athens of the East, is one of the oldest continuously inhabited cities in the world, with a recorded history that goes back more than 2,500 years. Located on the banks of the Vaigai River in Tamil Nadu, India, the city has been a major cultural, political, and religious center for centuries. It is most famous for the Meenakshi Amman Temple, an architectural marvel and one of the most important pilgrimage sites in South India.*

### 3. Paraphrasing
**Template:** Rewrite text while maintaining meaning
**Example:**
> Rewrite this sentence in your own words:
> 
> *"This a small community for AI in future it'll grow and everyone works together and world will ends."*

### 4. Definition Request
**Template:** Ask for meaning/definition
**Example:**
> What is the meaning of nepotism?

### 5. Comparison
**Template:** Compare items based on specific criteria
**Example:**
> Compare iPhone 16 and iPhone 17 based on the performance and price.

## B. Persona-Based Prompt Templates

### 6. Role + Explanation
**Template:** `You are a [role]. Explain [concept] to [audience].`
**Example:**
> You are a medical advisor. Explain the consequences of unhygiene to the layman.

### 7. Style Mimicry
**Template:** Write in the style of a specific person/author
**Example:**
> Write like Vairamuthu: about me

### 8. Professional Writing
**Template:** `You are a [job title]. Write a [document type] about [topic].`
**Example:**
> You are a SDET. Write a blog about SDET.

## C. Few-Shot Prompt Templates

### 9. Classification Template
**Template:** Provide examples and ask for classification
**Example:**
```
Today friday I'm in office → Working day
Tomorrow I'll be on leave → Weekend
Again started working → _______
```

### 10. Translation Template
**Template:** Provide translation examples and request new translation
**Example:**
```
Translate to Tamil:
what is your name? → உன் பெயர் என்ன?
where are you from? → நீங்கள் எங்கிருந்து வருகிறீர்கள்?
The artist was an iconoclast, using controversial imagery to provoke thought. → _______
```

### 11. Question Answering Template
**Template:** Show Q&A pattern and request completion
**Example:**
```
Who wrote "Romeo and Juliet"? → William Shakespeare
What is the capital of France? → Paris
Smallest planet in the solar system? → _______
```

## D. Chain-of-Thought (CoT) Templates

### 12. Step-by-Step Reasoning
**Template:** Break down complex problems into steps
**Example:**
> Let's think step by step about building a mobile-based tax filing software.

### 13. Math Problem Solving
**Template:** Show detailed mathematical reasoning
**Example:**
> Solve step by step: `(2*24*24*24/78/10-12-12+45+45)`

### 14. Logical Puzzle
**Template:** Break down logic puzzles with reasoning
**Example:**
> A person walks 5 km North, then turns left and walks 10 km. They then turn left again and walk 5 km. How far and in which direction are they from the starting point?

## E. Instruction Tuning/Format Control

### 15. Output Formatting
**Template:** Request specific output format
**Example:**
> Summarize the article below in exactly 5 bullet points.

### 16. Table Generation
**Template:** Request structured comparison
**Example:**
> Create a table comparing Samsung S23 Ultra, Samsung S24 Ultra, and iPhone 17 based on camera and performance.

### 17. Email Writing
**Template:** Generate professional communication
**Example:**
> Write a professional email to info@itc.com regarding issues with frozen prawn cleanliness.

## F. Contextual Prompts

### 18. Tailored Explanation
**Template:** `Explain [complex topic] to [age group] with [background knowledge]`
**Example:**
> Explain rocket science to a lower school student who doesn't have basic understanding.

### 19. Industry-Specific Context
**Template:** `As a [expert], explain [topic] impact on [industry]`
**Example:**
> As a financial expert, explain how high gold prices impact the Indian market.

## G. Creative Writing Prompts

### 20. Story Writing
**Template:** `Write about [character] who [goal] but faces [obstacle]`
**Example:**
> Write a short story about Paari who tries to study GenAI but faces distractions from family functions and office work.

### 21. Poem Writing
**Template:** Create poetry with specific parameters
Write a poem in [style/poetic form] about [theme].
**Example:**
> Write a poem in romantic style about pig.

### 22. Dialogue Writing
Write a realistic dialogue between [Person A] and [Person B] discussing [topic].
**Example:**
> Write a realistic dialogue between Modi and Putin discussing about Mutton Biriyani.

## H. Code & Technical Prompts

### 23. Code Generation
Write a [language] function that [does something].
**Example:**
> Write a C# function to calculate bmi.

### 24. Debugging Help
Here is some code. Find and fix any errors:
**Example:**
> a=1;
> b=1;
> c+=a+b;
> read(c);

### 25. API Documentation
Explain how to use the [API name] with an example request and response.
**Example:**
> Explain how to use the WhatsApp API with an example request and response.

## I. Marketing & Business Prompts

### 26. Ad Copywriting
Write a compelling ad for [product/service] targeting [audience].
**Example:**
> Write a compelling ad for curd targeting all age.

### 27. Product Description
Write a persuasive product description for [product name].
**Example:**
> Write a persuasive product description for Paari Soap.

### 28. Social Media Post
Create a social media post promoting [event/product/idea] in a friendly tone.
**Example:**
> Create a social media post promoting small foof kiosk only for idly and dosa in a friendly tone.

## J. Customer Support & Service Prompts

### 29. Response to Complaint
Respond professionally to this customer complaint: [Customer message here]
**Example:**
> Respond professionally to this customer complaint: yAct internet connection is very slow always

### 30. FAQ Generator
Generate 5 common FAQs and answers for [topic/product]
**Example:**
> Generate 5 common FAQs and answers for food delivey app payment

## K. Education & Tutoring Prompts

### 31. Lesson Plan Creation
Create a lesson plan for teaching [topic] to [grade level].
**Example:**
> Create a lesson plan for teaching algebra to LKG in rhymes.

### 32. Quiz Generation
Generate a 5-question quiz about [subject/topic].
**Example:**
> Generate a 5-question quiz about spaces.

### 33. Homework Help
Explain how to solve this [math/science] problem:
**Example:**
> A train crosses a platform 100 m long in 60 seconds at a speed of 45 km / hr. The time taken by the train to cross an > > electric pole is:

### L. Advanced Framework-Based Templates

### 34. ReAct Framework
Thought: [model thinks about what to do next]
Action: [model takes an action]
Observation: [result of the action]
Answer: [final answer]
**Example:**
> who discovered newton 1st law?
> Thought: I want to know who discovered newton first law, it is a gk question
> Action: search my knowledge who discovers light
> Observation: newton 1st law discovered by newton
> Answer: newton 1st law discovered by newton

Simulate agent behavior manually.

### 35. Tree of Thoughts (ToT)
Generate 3 possible solutions to [problem]. Evaluate each and choose the best one.
**Example:**
> Sakarai pongal vadakari
> Payasam Karakolanambu
> Biriyani Pachadi

> Evalution : Biriyani Pachadi

### 36. Self-Consistency Prompting
Solve the following question in 3 different ways and pick the
most consistent answer:
**Example:**
> How to pick a best quality t shirt?

## M. Prompt Optimization & Evaluation

### 37. Prompt Refinement
Improve this prompt: "[Original prompt]" Make it clearer, more specific, and structured.
**Example:**
> Improve this prompt: "Consider you're a jmeter expert, How to extract values from the response header" Make it clearer, > more specific, and structured.

### 38. Prompt Grading Rubric
Rate this output based on the following criteria (1-5):
Relevance:
Accuracy:
Clarity:
Fluency:
Creativity:
Final Score:
**Example:**
> Consider you are a JMeter expert.
> 
> You need to extract the values from response headers
> 
> example: 
> 
> alt-svc :h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
> 
> cache-control : no-cache, must-revalidate
> 
> content-type: text/html; 
> 
> Extract the value of content-type: , the value is text/html
> 
> Give the report in detailed manner anyone can understand in tree of thoughts

### 39. Prompt Iteration Challenge
Take this weak prompt: "[Prompt]"
Now rewrite it 3 times to improve clarity and effectiveness.
**Example:**
> Take this weak prompt: "You are a skilled **Business Requirement Analysis Agent**. Your expertise is in extracting and organizing requirement details from business documents precisely and clearly."
> 
> Now rewrite it 3 times to improve clarity and effectiveness.

## N. Real-World Application Prompts

### 40. Job Posting Creation
Write a job posting for [position] at [company]. Include responsibilities, requirements, and benefits.
**Example:**
> Write a job posting for Senior SDET at FE Fundinfo. Include responsibilities, requirements, and benefits.

### 41. Resume Summary Builder
Create a professional summary for a resume based on the following details:
[Experience, skills, achievements]
**Example:**
> Create a professional summary for a resume based on the following details:
[9+ experience in software testing, skills: manual testing , jmeter, playwright selenium, c# , java , python, Genai, achievements: put siome achievements based on role]

### 42. Business Propcsal
Write a proposal for [project idea] to [client/investor]. Include objectives, methodology, and benefits
**Example:**
> Write a proposal for selfhost chatbot to fundinfo. Include objectives, methodology, and benefits

## O. Miscellaneous Useful Templates

### 43. Opinion Writing
Write an opinion piece on [topic]. Use persuasive arguments and examples.
**Example:**
> Write an opinion piece on Gen Z issue in nepal. Use persuasive arguments and examples.

### 44. Debate Preparation
Prepare arguments for both sides of the debate: "[Debate topic]"
**Example:**
> Prepare arguments for both sides of the debate: "Who is best in home men or women"

### 45. Travel Planning
Plan a 5-day trip to [destination] for [type of traveler]. Include activities, budget, and tips.
**Example:**
> Plan a 5-day trip to Rameswaram for me and wife in bike. Include activities, budget, and tips.

### 46. Book/Movie Review
Write a review of [book/movie]. Include plot summary, strengths, weaknesses, and recommendation.
**Example:**
> Write a review of f1 movie. Include plot summary, strengths, weaknesses, and recommendation.

### 47. Personal Development
Give me actionable advice on how to [goal], including daily habits and mindset shifts.
**Example:**
> Give me actionable advice on how to improve wealth, including daily habits and mindset shifts.

## P. Prompt Chaining Examples

### 48. Multi-step Research Task
Step 1:
Find out the top 5 causes of climate change.
Step 2:
Based on those causes, suggest 5 practical solutions individuals can adopt.
**Example:**
> Step 1: 
>
> Find out the top 5 causes of ai change. 
> Step 2: 
>
> Based on those causes, suggest 5 practical solutions individuals can adopt.

### 49. Idea to Execution
Step 1:
Generate 5 business ideas for eco-friendly products.
Step 2:
Pick one idea and create a marketing strategy for it.
**Example:**
> Step 1:
> 
> Generate 5 business ideas for gen z products.
> 
> Step 2:
> 
> Pick one idea and create a marketing strategy for it.

## Q. Prompt Template Generator

### 50. Universal Prompt Builder

[Role] + [Task] + [Context] + [Example]+ [Format]
**Example:**
> You are a financial expert. Create a detailed plan for saving money and wealth. Include mistakes of saving like bank saving account /FD create a prompt in the R+T+C+E+F format


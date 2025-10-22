# Test assignment

## Python developer

We appreciate your interest in joining our RecMan team. To ensure we select the
most qualified candidates, we have shortlisted you to complete this test task, which
is enclosed in this document.
Furthermore, we value candidates who are highly motivated and committed to
self-improvement. We encourage you to showcase your creativity and your ability to
think outside the box throughout the task.
Please provide a GitHub repository with the completed project. The repository
should include a README.md file with instructions on how to run the application
locally.
We wish you the best of luck with the test, and we appreciate your interest in

## becoming a part of our team!

**Test Task: Python Text Classifier/Summarizer AWS Lambda
Description:**
Develop an AWS Lambda function* in Python that classifies short texts (e.g.,
emails) into predefined topics or produces a 1–2 sentence summary.
The solution must work with one of two backends (your choice):

- External LLM API (OpenAI / Anthropic / other): **use your own API key for**
    **the demo and do not include keys in the repository.**
- Local model: bundle a small local model and code to run it offline. The
    repository **must include everything needed to run locally** (model file or a
    deterministic script that fetches it on first run + lockfile), without requiring
    any cloud keys.


*Local run (simulate Lambda):
python -m app.run --input sample/emails.json --mode classify --log-level INFO
or
python -m app.run --input sample/emails.json --mode summarize --log-level INFO
**Requirements:**

- Modularity: The code should be cleanly structured and modular to allow
    future extensions.
- Modes: The function must support two modes — classify (assign texts to
    predefined topics) and summarize (produce 1–2 sentence summaries).
- Model Abstraction: Design the solution so that the underlying model (API or
    local) can be swapped or upgraded with minimal changes.
- Cost Awareness: Think about cost efficiency when interacting with AI
- Error Handling: Invalid or empty inputs should not stop processing. Provide
    meaningful error logging while continuing with valid items.
**Lambda Input/Output:**
Note: You may extend the body field with short, email-style text of your own choice (e.g., a
few sentences resembling real emails) to make the examples more realistic.
Input (emails.json):
[
{ "id": 1, "subject": "Invoice #1234 overdue", "body": "Dear customer..." },
{ "id": 2, "subject": "Weekly engineering sync", "body": "Agenda: ..." },
{ "id": 3, "subject": "Company retreat announcement", "body": "We invite you..." },
{ "id": 4, "subject": "", "body": " " }
]


Output (classify example):
[
{ "id": 1, "topics": ["finance"] },
{ "id": 2, "topics": ["technical"] },
{ "id": 3, "topics": ["hr", "marketing"] },
{ "id": 4, "error": "empty_input" }
]
Output (summarize example):
[
{ "id": 1, "summary": "Short invoice reminder..." },
{ "id": 2, "summary": "Weekly sync will cover..." },
{ "id": 3, "summary": "Announcement for company retreat..." },
{ "id": 4, "error": "empty_input" }
]
**Deliverables:**
A comprehensive Git repository containing the following:

- Python Code: The complete source code for the AWS Lambda function.
- Code Quality: Clear, well-structured, and readable code, accompanied by
    relevant inline comments to enhance understanding.
- Documentation: A README.md file detailing setup instructions, execution
    procedures, and an overview of the solution.
- Recording of demo with brief overview and explanation of the project in
    English. To record as an example you may use Loom.com or any other tools
    according to your preference which will record voice and screen.
**Evaluation Criteria:**
Submissions will be assessed based on the following:
- Code Quality: Adherence to Python best practices, modular design, and
overall code elegance.
- Functionality: Correct and reliable operation of the Lambda function with
diverse sample inputs.
- Cost-awareness.


- Extensibility: The ease with which new modes or AI models can be integrated
    into the existing solution.
- Documentation: Clarity, completeness, and accuracy of the README.md and
    inline comments.



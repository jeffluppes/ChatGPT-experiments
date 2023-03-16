import openai
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
config = configparser.ConfigParser()

# config contains my api keys.
config.read("configs.txt")
openai.api_key = config.get("ChatGPT", "key")
MODEL = config.get("ChatGPT", "model")


def generate_career_advice_prompts(resume: str) -> dict:
    logger.info("Creating prompts based on your resume..")
    prompts = [
        "Give career advice, focusing on potential next jobs (titles), based on the following resume:",
        "At a high level, what would improve the following resume to pass HR screening?",
        "Can you summarize the following resume for me?",
        "how many years of experience does the following resume have in the candidates main field?",
        "How senior in their main field is the candidate in the following resume: ",
        "Can you find any errors or grammatical mistakes in the following resume:",
    ]
    return [{"prompt": p, "text": f"{p} \n{resume}"} for p in prompts]


def generate_job_posting_prompts(posting: str) -> dict:
    logger.info("Creating prompts based on job posting..")
    prompts = [
        "How would you improve the following job posting?",
        "What is the reading level needed to understand the following job posting: ",
        "How would you make the following job posting appeal more to younger candidates?",
        "Can you summarize this job posting?",
        "Can you see any red flags in the following job posting?",
        "What is the seniority needed in the main field of the following job posting: ",
        "can you find any errors or grammatical mistakes in the following text: ",
        "What are the main skills needed for the following job:",
        "How hard do you think this job is?",
    ]
    return [{"prompt": p, "text": f"{p} \n{posting}"} for p in prompts]


def get_chatgpt_response(prompt: str) -> dict:
    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        max_tokens=2000,
        temperature=0.6,
    )
    return response


def get_text_from_file(doc: str) -> str:
    """
    Mocking a resume parser here because I want to keep things simple.
    Under actual conditions, I'd parse a resume with Apache Tika
    Or a similar tool, then further process the text with regexes and
    text-processing libraries. Also note, that for simplicity, I assume
    the resume is a text file without any structure.

    The file I open contains the first page of my resume
    """
    with open(doc, "r") as f:
        text = f.read()

    return text


if __name__ == "__main__":

    # these are just for testing, take a look at the jupyter notebook for a more verbose example
    resume: str = get_text_from_file("linsresume.txt")
    prompts: dict = generate_career_advice_prompts(resume)

    with open("output_resume_advice", "w") as o:
        for prompt in prompts:
            print(get_chatgpt_response(prompt.get("text")))
            print("-----------------------------")

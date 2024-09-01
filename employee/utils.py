from cases.models import Case
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def create_statement(employee_id, emotion, consistency_analysis, reference_link):

    # handle consistency_analysis and reference_link

    # Step 1: Retrieve all cases for the employee that are not closed
    cases = Case.objects.filter(employee_id=employee_id).exclude(report_status=Case.CLOSED)
    
    # Step 2: Format the case information into a summary
    case_details = []
    for case in cases:
        case_details.append(f"Category: {case.category}, Status: {case.get_report_status_display()}, Date Reported: {case.date_reported.strftime('%Y-%m-%d')}, Report: {case.report[:100]}...")

    case_info = "\n".join(case_details)

    # Step 3: Add the case information to the messages
    messages = [
        {"role": "system", "content": 'You are an AI model tasked with generating a "Statement of Facts" for a case involving an employee, with the goal of favoring the agency while still maintaining a fair, win-win tone where possible. The "Statement of Facts" should be clear, concise, and factual, summarizing the key details and events relevant to the case.'},
        {"role": "user", "content": f"Employee ID: {employee_id}\n\nCase Details:\n{case_info}\nEmotion:\n{emotion}"}
    ]
    
    if consistency_analysis:
        messages.append(
            {"role": "user", "content": f"Consistency Analysis Findings:\n{consistency_analysis}"}
        )

    # Step 5: Include reference link if provided
    if reference_link:
        messages.append(
            {"role": "user", "content": f"Additional Information: Please refer to the following link for more details - {reference_link}"}
        )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None

def build_consistency_analysis(chat_history):
    introduction = (
        "Review the following conversation between the applicant and the agency. "
        "Your task is to evaluate the consistency and truthfulness of the applicant's statements. "
        "Consider the following aspects:\n\n"
        "1. **Consistency**: Are the applicant's statements consistent with each other, or are there contradictions? "
        "Do they align with previously provided information?\n"
        "2. **Truthfulness**: Based on the tone, details, and context, does the applicant appear to be telling the truth? "
        "Are there any signs of deception or exaggeration?\n"
        "3. **Ambiguities or Concerns**: Are there any parts of the conversation that seem unclear, evasive, "
        "or raise concerns about the applicant's credibility?\n\n"
        "Provide a summary that includes:\n"
        "- An overall assessment of the applicant's consistency.\n"
        "- An indication of whether the applicant is likely telling the truth, possibly lying, "
        "or if there are any red flags.\n"
        "- Any specific instances or patterns that led to your judgment.\n\n"
        "**Conversation:**"
    )

    chat_history_string = "\n".join(chat_history)

    # Build the array of messages (this is how you'd typically structure it for an API call)
    messages = [
        {"role": "system", "content": "You are an AI model that evaluates the consistency and truthfulness of text."},
        {"role": "system", "content": introduction},
        {"role": "user", "content": chat_history_string},
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return ""
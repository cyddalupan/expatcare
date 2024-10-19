from django.contrib import admin
from .models import StatementOfFact
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

@admin.register(StatementOfFact)
class StatementOfFactAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'employee', 'creator', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'score', 'created_at', 'employee')
    search_fields = ('title', 'content', 'employee__first_name', 'employee__last_name')
    autocomplete_fields = ['creator']  # Autocomplete only for creator

    # Override to make employee, score, and suggestion read-only in all cases
    def get_readonly_fields(self, request, obj=None):
        # Fields that are always read-only
        return ['creator', 'score', 'suggestion']

    # Override save_model to set the creator automatically
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set creator on creation
            obj.creator = request.user
        
        score, suggestion = ai_check_write(obj.content)
        obj.score = score
        obj.suggestion = suggestion

        super().save_model(request, obj, form, change)
    
def ai_check_write(article):
    rules_text = """
    1. Header Format: Ensure that the document includes the name of the issuing authority (e.g., "Republic of the Philippines"), the department involved (e.g., Department of Labor and Employment), and the specific office or branch, followed by the address. After the header, check if the case title, case number, and type of claim are listed.

    2. Complainant and Respondent Information: Verify that the complainant is listed first, centered and in uppercase, followed by the case number and type of claim. Ensure that "versus" separates the complainant from the respondents, and the respondents are listed next in a similar format.

    3. Opening Statement ("Comes Now"): Check if the document begins with "COMES NOW," followed by the name of the party submitting the position paper. Ensure that their authority or role is clearly stated, and the statement ends with a reference to the Honorable Office.

    4. Prefatory Statement: Ensure that the document includes a Prefatory Statement where general arguments or comments about the allegations are made. Verify that Latin legal maxims or principles are used where appropriate to emphasize key legal points.

    5. Parties' Information: Check if the section titled "THE PARTIES" provides detailed information about all parties involved, including their names, roles, relevant registrations (e.g., SEC, DMW), and addresses. Confirm that the complainant’s employment history is summarized in a concise and relevant manner.

    6. Statement of Facts: Look for a "STATEMENT OF FACTS" section that presents the respondent’s perspective of events. Ensure that the section denies claims or allegations made by the complainant and refutes each point clearly. Verify if evidence or annexes are mentioned and referred to properly.

    7. Issues for Resolution: Ensure that a section titled "ISSUES" is present and lists the legal questions or points to be addressed. Verify that the issues are framed in the form of "WHETHER OR NOT..." and cover all key points, such as dismissal, unpaid salaries, contract terms, and entitlement to damages.

    8. General Style and Formatting: Check if the document uses formal and respectful language throughout, with section headings in uppercase or bold for distinction. Ensure that legal citations, case law references, or legal principles are included where necessary to support arguments. Confirm that paragraphs are numbered for reference.

    Check if these rules are consistently followed throughout the document, and note any violations or missing elements.
    """

    system_message = f"Trigger the score_article function no need for reply. You rate the user content based on these rules: {rules_text}"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": article},
        {"role": "system", "content": "trigger score_article function"},
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "score_article",
                        "description": "this function always triggers. this gives the article score and suggestion on how to improve the score",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "score": {
                                    "type": "integer",
                                    "description": "Score of the writer on how good it follows the rules from 1 to 100. 100 is perfect.",
                                },
                                "suggestion": {
                                    "type": "string",
                                    "description": "Suggestion to the writer on how to get a higher score. use easy to understand words. just congratulate if the score is perfect",
                                },
                            },
                            "required": ["score"],
                        },
                    },
                },
            ],
        )
        tool_calls = completion.choices[0].message.tool_calls
        
        if tool_calls:
            function_name = tool_calls[0].function.name 
            arguments = tool_calls[0].function.arguments 
            arguments_dict = json.loads(arguments)
            
            if function_name == "score_article":
                score = arguments_dict['score']
                suggestion = arguments_dict['suggestion']
                return score, suggestion
            else:
                return None, None
    except Exception as e:
        return None, None

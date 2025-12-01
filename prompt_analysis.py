# prompt_analysis.py
import re

def analyze_prompt(user_prompt: str):
    prompt_lower = user_prompt.lower().strip()

    # ---------------- LENGTH ----------------
    char_count = len(user_prompt)
    word_count = len(user_prompt.split())

    if word_count < 8:
        length_category = "too_short"
    elif word_count < 21:
        length_category = "short"
    elif word_count <= 100:
        length_category = "ideal"
        # you might tweak 100 later if needed
    else:
        length_category = "long"

    # ---------------- CLARITY ----------------
    ACTION_VERBS = [
        "write", "explain", "describe", "summarize", "list", "generate",
        "create", "build", "design", "draft", "compose", "produce",
        "analyze", "review", "compare", "contrast", "improve",
        "refactor", "debug", "solve", "fix", "optimize",
        "assess", "evaluate", "justify", "critique", "argue",
        "predict", "infer", "conclude", "examine", "interpret",
        "format", "structure", "organize", "classify", "tabulate", "outline",
        "categorize", "translate", "rewrite", "paraphrase", "edit", "proofread",
        "question", "respond", "reply", "teach", "coach", "tutor", "guide",
        "code", "program", "script", "implement", "simulate",
        "story", "narrate", "roleplay", "imagine", "brainstorm",
        "visualize", "sketch", "draw"
    ]

    has_action_verb = any(re.search(rf"\b{verb}\b", prompt_lower) for verb in ACTION_VERBS)
    has_clear_task = has_action_verb and word_count >= 5

    # ---------------- SENSITIVE CONTENT ----------------
    SENSITIVE_WORDS = [
        "suicide", "kill myself", "end my life", "self harm",
        "hurt myself", "i want to die", "i don’t want to live",
        "kill", "murder", "torture", "assault", "attack", "stab", "shoot",
        "strangle", "harm","hurting","crime",
        "gun", "pistol", "rifle", "bomb", "grenade", "shotgun", "weapon",
        "explosive", "ammunition",
        "cocaine", "heroin", "meth", "weed", "marijuana", "lsd",
        "ecstasy", "opium",
        "hate", "eliminate", "genocide", "racist", "inferior",
        "porn", "sex", "nude", "explicit", "xxx"
    ]
    has_sensitive_words = any(re.search(rf"\b{w}\b", prompt_lower) for w in SENSITIVE_WORDS)

    # ---------------- PERSONAL INFO ----------------
    PERSONAL_KEYWORDS = [
        "password", "passcode", "otp", "one time password",
        "pin", "security pin", "cvv", "cvc",
        "credit card", "debit card", "card number", "account number",
        "bank account", "ifsc", "iban", "routing number",
        "upi id", "upi handle", "net banking",
        "phone number", "mobile number", "contact number",
        "whatsapp number", "email", "email id",
        "address", "full address", "home address", "office address",
        "street", "road", "lane", "house no", "flat no", "apartment",
        "pincode", "postal code", "zip code", "city", "state",
        "aadhaar", "aadhar", "pan number", "pan card",
        "passport number", "voter id", "driving licence",
        "driving license", "ssn", "social security number"
    ]

    EMAIL_REGEX = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b"
    PHONE_REGEX = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    CREDIT_CARD_REGEX = r"\b(?:\d[ -]*?){13,19}\b"
    AADHAAR_REGEX = r"\b[2-9]\d{11}\b"
    PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    has_personal_keywords = any(re.search(rf"\b{w}\b", prompt_lower) for w in PERSONAL_KEYWORDS)
    has_email = bool(re.search(EMAIL_REGEX, prompt_lower))
    has_phone = bool(re.search(PHONE_REGEX, prompt_lower))
    has_credit_card = bool(re.search(CREDIT_CARD_REGEX, prompt_lower))
    has_aadhaar = bool(re.search(AADHAAR_REGEX, prompt_lower))
    has_pan = bool(re.search(PAN_REGEX, prompt_lower))

    has_personal_info = any([
        has_personal_keywords,
        has_email,
        has_phone,
        has_credit_card,
        has_aadhaar,
        has_pan
    ])

    # ---------------- EXAMPLE CHECK ----------------
    EXAMPLE_KEYWORDS = ["for example", "e.g.", "example:", "sample:", "such as"]
    has_example = any(re.search(rf"\b{w}\b", prompt_lower) for w in EXAMPLE_KEYWORDS)

    # ---------------- OUTPUT FORMAT ----------------
    OUTPUT_FORMAT_KEYWORDS = [
        "list", "as a list", "in a list", "bullet points", "bullets",
        "as bullet points", "in bullet points", "numbered list", "in points",
        "as points", "checklist", "outline", "table", "as a table",
        "in a table", "tabular format", "tabular form", "columns and rows",
        "column wise", "row wise", "markdown table", "json", "as json",
        "in json format", "json object", "valid json", "key value pairs",
        "key-value pairs", "step by step", "in steps", "as steps",
        "in numbered steps", "stepwise", "series of steps", "code block",
        "as code", "in code format", "return only code", "provide only code",
        "without explanation", "no explanation, just code", "one paragraph",
        "single paragraph", "short paragraph", "in a paragraph"
    ]

    JSON_LIKE_REGEX = r"\{\s*\"[^\"}]+\"\s*:\s*[^}]+?\}"
    BULLET_LINE_REGEX = r"^[\-\*]\s+.+"
    NUMBERED_LINE_REGEX = r"^\d+\.\s+.+"
    CODE_BLOCK_REGEX = r"```[a-zA-Z0-9_]*\n[\s\S]*?```"
    MARKDOWN_TABLE_REGEX = r"\|[^|\n]+\|[^|\n]+\|"

    has_output_keywords = any(re.search(rf"\b{w}\b", prompt_lower) for w in OUTPUT_FORMAT_KEYWORDS)
    has_json_output = bool(re.search(JSON_LIKE_REGEX, user_prompt))
    has_bullet_output = bool(re.search(BULLET_LINE_REGEX, user_prompt, re.MULTILINE))
    has_number_line_output = bool(re.search(NUMBERED_LINE_REGEX, user_prompt, re.MULTILINE))
    has_markdown_output = bool(re.search(MARKDOWN_TABLE_REGEX, user_prompt))
    has_code_block_output = bool(re.search(CODE_BLOCK_REGEX, user_prompt))

    has_output_format = any([
        has_output_keywords,
        has_json_output,
        has_bullet_output,
        has_number_line_output,
        has_markdown_output,
        has_code_block_output
    ])

    # ---------------- PERSONA ----------------
    PERSONA_KEYWORDS = [
        "you are a","you are an","you are the","you're a","you're an",
        "act as a","act as an", "act as the","act like a","act like an",
        "pretend you are","pretend to be","take the role of","in the role of",
        "from the perspective of a", "from the perspective of an",
        "answer as a","answer as an","behave like a","behave like an"
    ]
    has_persona = any(re.search(rf"\b{w}\b", prompt_lower) for w in PERSONA_KEYWORDS)

    # ---------------- RETURN ALL FLAGS ----------------
    return {
        "chars": char_count,
        "words": word_count,
        "length_category": length_category,
        "has_action_verb": has_action_verb,
        "has_clear_task": has_clear_task,
        "has_sensitive_words": has_sensitive_words,
        "has_personal_info": has_personal_info,
        "has_example": has_example,
        "has_output_format": has_output_format,
        "has_persona": has_persona
    }


def score_analysis(analysis: dict):
    length_category = analysis["length_category"]
    has_action_verb = analysis["has_action_verb"]
    has_clear_task = analysis["has_clear_task"]
    has_sensitive_words = analysis["has_sensitive_words"]
    has_personal_info = analysis["has_personal_info"]
    has_example = analysis["has_example"]
    has_output_format = analysis["has_output_format"]
    has_persona = analysis["has_persona"]

    # ---------- LENGTH SCORE (0–10) ----------
    if length_category == "too_short":
        length_score = 1   # make this harsher
    elif length_category == "short":
        length_score = 5
    elif length_category == "ideal":
        length_score = 9
    else:  # "long"
        length_score = 6

    # ---------- CLARITY SCORE (0–10) ----------
    clarity_score = 2  # slightly lower base

    if has_action_verb:
        clarity_score += 3
    if has_clear_task:
        clarity_score += 3
    if has_example:
        clarity_score += 1

    if length_category == "too_short":
        # cap clarity harder for tiny prompts
        clarity_score = min(clarity_score, 3)

    clarity_score = max(0, min(10, clarity_score))

    # ---------- STRUCTURE SCORE (0–10) ----------
    structure_score = 2  # lower base

    if has_output_format:
        structure_score += 4

    structure_score = max(0, min(10, structure_score))

    # ---------- SAFETY SCORE (0–10) ----------
    safety_score = 10

    if has_sensitive_words:
        safety_score -= 4
    if has_personal_info:
        safety_score -= 3

    safety_score = max(0, min(10, safety_score))

    # ---------- PERSONA BONUS (0–2) ----------
    persona_bonus = 2 if has_persona else 0

    # ---------- OVERALL SCORE ----------
    base_avg = (length_score + clarity_score + structure_score + safety_score) / 4
    overall_score = int(max(0, min(100, base_avg * 10 + persona_bonus)))

    # 🔴 Hard rule: very short + no clear task = always Poor-ish
    if length_category == "too_short" and not has_clear_task:
        overall_score = min(overall_score, 30)

    # ---------- LABEL ----------
    if overall_score < 50:
        label = "Poor"
    elif overall_score < 70:
        label = "Okay"
    elif overall_score < 85:
        label = "Good"
    else:
        label = "Excellent"

    return {
        "length_score": length_score,
        "clarity_score": clarity_score,
        "structure_score": structure_score,
        "safety_score": safety_score,
        "persona_bonus": persona_bonus,
        "overall_score": overall_score,
        "label": label,
    }


def summarize_prompt_analysis(analysis: dict, score: dict):
    overall_score = score["overall_score"]
    label = score["label"]

    length_category = analysis["length_category"]
    has_action_verb = analysis["has_action_verb"]
    has_clear_task = analysis["has_clear_task"]
    has_example = analysis["has_example"]
    has_output_format = analysis["has_output_format"]
    has_persona = analysis["has_persona"]
    has_sensitive_words = analysis["has_sensitive_words"]
    has_personal_info = analysis["has_personal_info"]

    strengths = []
    improvements = []
    safety_notes = []

    # ---------- Overall line ----------
    overall_line = f"Overall: {label} prompt ({overall_score}/100)."

    # ---------- Length explanation ----------
    if length_category == "too_short":
        improvements.append(
            "The prompt is very short. Add more context or details so the model doesn’t have to guess."
        )
    elif length_category == "short":
        strengths.append(
            "The prompt is short and easy to read."
        )
        improvements.append(
            "You can add a bit more context if the model needs to understand a specific situation."
        )
    elif length_category == "ideal":
        strengths.append(
            "The prompt length is ideal — detailed enough without being too long."
        )
    else:  # long
        strengths.append(
            "The prompt contains a lot of detail."
        )
        improvements.append(
            "Consider removing extra or repeated information to keep it focused."
        )

    # ---------- Clarity explanation ----------
    if has_action_verb:
        strengths.append(
            "You clearly tell the model what to do (e.g. write, explain, generate, etc.)."
        )
    else:
        improvements.append(
            "Add a clear action verb like 'explain', 'generate', or 'summarize' so the model knows what to do."
        )

    if has_clear_task:
        strengths.append(
            "The main task of the prompt is easy to understand."
        )
    else:
        improvements.append(
            "Make the main task more explicit. For example: 'Explain X in simple terms' or 'Generate ideas for Y'."
        )

    if has_example:
        strengths.append(
            "You included an example, which makes your intent much clearer."
        )
    else:
        improvements.append(
            "You can add a small example of the kind of answer you expect. This often improves results."
        )

    # ---------- Output format explanation ----------
    if has_output_format:
        strengths.append(
            "You specified an output format (list, table, JSON, steps, etc.), which helps structure the response."
        )
    else:
        improvements.append(
            "Optionally, you can specify an output format — for example: 'answer in bullet points', 'as a table', or 'in JSON'."
        )

    # ---------- Persona explanation ----------
    if has_persona:
        strengths.append(
            "You defined a role for the assistant (persona), which can make responses more focused and relevant."
        )
    else:
        improvements.append(
            "Optionally, you can define a role for the assistant, e.g. 'You are an expert copywriter' or 'Act as a senior backend engineer'."
        )

    # ---------- Safety & personal info ----------
    if has_sensitive_words:
        safety_notes.append(
            "The prompt may contain sensitive or harmful language. Make sure it follows platform and legal guidelines."
        )

    if has_personal_info:
        safety_notes.append(
            "The prompt seems to include personal or private information (like email, phone, or account details). "
            "Avoid sharing real personal data in prompts when possible."
        )

    # ---------- Remove duplicates & clean ----------
    strengths = list(dict.fromkeys(strengths))       # preserve order, remove duplicates
    improvements = list(dict.fromkeys(improvements))
    safety_notes = list(dict.fromkeys(safety_notes))

    return {
        "overall_line": overall_line,
        "strengths": strengths,
        "improvements": improvements,
        "safety_notes": safety_notes,
    }


# --------- Final helper to call from app.py ---------
def run_prompt_evaluation(user_prompt: str) -> dict:
    """
    Convenience function that runs the full pipeline
    and returns everything in one response object.
    """
    analysis = analyze_prompt(user_prompt)
    score = score_analysis(analysis)
    summary = summarize_prompt_analysis(analysis, score)

    return {
        "analysis": analysis,
        "score": score,
        "summary": summary,
    }

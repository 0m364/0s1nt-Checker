import structlog
from app.core.config import settings

log = structlog.get_logger()

class AIService:
    def __init__(self):
        self.enabled = settings.ai.enabled
        self.provider = settings.ai.provider
        self.openai_client = None
        self.gemini_model = None

        if not self.enabled:
            return

        if self.provider == "openai":
            if settings.ai.openai_api_key:
                try:
                    from openai import OpenAI
                    self.openai_client = OpenAI(api_key=settings.ai.openai_api_key)
                except ImportError:
                    log.error("openai module not found")
                    self.enabled = False
            else:
                log.warning("OpenAI API key missing")
                self.enabled = False

        elif self.provider == "gemini":
            if settings.ai.gemini_api_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=settings.ai.gemini_api_key)
                    self.gemini_model = genai.GenerativeModel(settings.ai.gemini_model)
                except ImportError:
                    log.error("google-generativeai module not found")
                    self.enabled = False
            else:
                log.warning("Gemini API key missing")
                self.enabled = False

    def generate_explanation(self, score_data: dict, evidence_list: list) -> str:
        if not self.enabled:
            return ""

        # Construct prompt
        prompt = f"Analyze the following OSINT threat scan results and provide a concise summary explaining the risk level and key findings.\n\n"
        prompt += f"Computed Score: {score_data.get('computed_score')}\n"
        prompt += f"Confidence Tier: {score_data.get('confidence_tier')}\n"
        prompt += f"Rationale: {score_data.get('rationale')}\n\n"

        prompt += "Evidence Found:\n"
        if not evidence_list:
            prompt += "No evidence found.\n"
        else:
            for ev in evidence_list:
                prompt += f"- Source: {ev.get('source_name')} ({ev.get('source_type')})\n"
                prompt += f"  Match Tier: {ev.get('match_tier')}\n"
                prompt += f"  Confidence: {ev.get('confidence_score')}\n"
                if ev.get('match_notes'):
                    prompt += f"  Notes: {ev.get('match_notes')}\n"

        prompt += "\nPlease provide a summary suitable for a security analyst."

        try:
            if self.provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=settings.ai.openai_model,
                    messages=[
                        {"role": "system", "content": "You are an expert OSINT analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()

            elif self.provider == "gemini" and self.gemini_model:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()

        except Exception as e:
            log.error(f"AI generation failed: {e}")
            return f"AI generation failed. Fallback: {score_data.get('rationale')}"

        return ""

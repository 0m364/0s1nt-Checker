import requests
from typing import List
from app.connectors.base import BaseConnector
from app.schemas import PersonSearch, SearchResult
from app.services.ai import AIService
import structlog

log = structlog.get_logger()

class CIAFactbookConnector(BaseConnector):
    name = "CIA World Factbook & Area Intelligence"
    source_type = "intelligence"

    def search(self, person: PersonSearch) -> List[SearchResult]:
        # We assume person.address or person.full_name contains the requested area
        area = person.address or person.full_name
        if not area:
            return []

        # Strip common words that aren't the country name
        area = area.split(',')[0].strip()

        log.info("scraping_area_data", area=area)

        # We use Wikipedia's summary API as a proxy for factbook data since CIA blocks scraping
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{area.replace(' ', '_')}"
        headers = {"User-Agent": "OSINT-Threat-Scanner/1.0"}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                return []

            data = resp.json()
            extract = data.get("extract", "")
            image_url = data.get("thumbnail", {}).get("source", "")

            # Optional: Use AI agentic capabilities to synthesize the summary
            ai_service = AIService()
            if ai_service.enabled:
                prompt = f"Act as an intelligence agent gathering data on {area}. Summarize the following information concisely:\n\n{extract}"
                if ai_service.provider == "openai" and ai_service.openai_client:
                    ai_resp = ai_service.openai_client.chat.completions.create(
                        model=ai_service.openai_model,
                        messages=[
                            {"role": "system", "content": "You are an intelligence analyst."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    extract = ai_resp.choices[0].message.content.strip()
                elif ai_service.provider == "gemini" and ai_service.gemini_model:
                    ai_resp = ai_service.gemini_model.generate_content(prompt)
                    extract = ai_resp.text.strip()

            raw_json = {
                "summary": extract,
                "image_url": image_url,
                "title": data.get("title", area)
            }

            return [SearchResult(
                source_name=self.name,
                source_type=self.source_type,
                record_id=area,
                evidence_url=data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                raw_json=raw_json,
                confidence_score=1.0 # Exact location match
            )]

        except Exception as e:
            log.error("cia_factbook_error", error=str(e))
            return []

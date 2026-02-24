from typing import List
import httpx
from app.api.books import BookSearchResponse
from app.services.exceptions import ExternalBookClientError

class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org/search.json"

    def search(self, query: str | None, subjects: list[str] | None):
        # filter parameters so that we only pass valid data
        params = {}
        if query:
            params["q"] = query 
        if subjects:
            params["subject"] = subjects

        try:
            # send the query with filtered params to openlibrary
            response = httpx.get(self.BASE_URL, params=params, timeout=10)
            # raises a python exception (HTTPStatusError) if openlibrary not available
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise ExternalBookClientError()

        # make it python pretty
        data = response.json()

        return [
            BookSearchResponse(
                id=None,
                external_id=item["key"],
                source="openlibrary",
                title=item.get("title"),
                author=", ".join(item.get("author_name", [])), # accommodating multiple authors
                cover_url=self._cover_url(item.get("cover_i")) # URL for frontend to grab cover art
            )
            for item in data.get("docs", [])
        ]

    # helper to retrieve cover art
    def _cover_url(self, cover_id: int | None):
        if cover_id is None:
            return None
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

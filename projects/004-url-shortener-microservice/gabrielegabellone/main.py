from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import validators


class UrlShortener(BaseModel):
    original_url: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "original_url": "https://tomorrowdevs.com"
                }
            ]
        }
    }


app = FastAPI(title="URL Shortener Microservice")

short_urls_created = {}


@app.post(
        "/api/shorturl",
        summary="Returns a JSON object with original_url and short_url properties.",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "example": {
                            "original_url": "https://tomorrowdevs.com",
                            "short_url": 1,
                        }
                    }
                }
            },
            400: {
                "content": {
                    "application/json": {
                        "example": {
                            "error": "invalid url",
                        }
                    }
                }
            }
        },
        tags=["Routes"]
    )
def create_short_url(url: UrlShortener) -> JSONResponse:
    original_url = url.original_url
    is_a_valid_url = validators.url(original_url)

    if is_a_valid_url:
        if original_url in short_urls_created.values():
            short_urls = list(short_urls_created.keys())
            original_urls = list(short_urls_created.values())
            i = original_urls.index(original_url)
            short_url = short_urls[i]
        else:
            short_url = len(short_urls_created) + 1
            short_urls_created[short_url] = original_url

        return JSONResponse(status_code=200, content={"original_url": original_url, "short_url": short_url})
    return JSONResponse(status_code=400, content={"error": "invalid url"})


@app.get(
        "/api/shorturl/{short_url}",
        summary="Redirect to the original url.",
        tags=["Routes"],
        responses={
            307: {
                "description": "Redirect"
            },
            404: {
                "content": {
                    "application/json": {
                        "example": {
                            "error": "short url not found",
                        }
                    }
                }
            }
        }
    )
def redirect_to_original_url(short_url: Annotated[int, Path(title="The ID of the url to get")]):
    try:
        original_url = short_urls_created[short_url]
        return RedirectResponse(original_url)
    except KeyError:
        return JSONResponse(status_code=404, content={"error": "short url not found"})

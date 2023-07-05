from typing import Annotated

from fastapi import FastAPI, Request, Header

app = FastAPI(
    title="Request Header Parser"
)


@app.get(
        "/api/whoami",
        summary="Returns a JSON object with your IP address and preferred language and software specified in the header.",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "example": {
                            "ipaddress": "127.0.0.1",
                            "language": "Python",
                            "software": "PyCharm"
                        }
                    }
                }
            }
        },
        tags=["Routes"]
    )
def who_am_i(request: Request, 
             language: Annotated[str | None, Header()] = None,
             software: Annotated[str | None, Header()] = None,
             ) -> dict:
    ip_address = request.client.host
    return {"ipaddress": ip_address, "language": language, "software": software}

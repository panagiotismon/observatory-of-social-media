from fastapi import FastAPI, APIRouter, Query
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.staticfiles import StaticFiles

from dto.sentiment_score_request import SentimentScoreRequest
from dto.subjectivity_score_request import SubjectivityScoreRequest
from orjson_response import ORJSONResponse
from routes.samples_routes import samples_router
from service.ml_metrics_service import get_subjectivity_score, get_sentiment_score

app = FastAPI(
    title="VERITAS API",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="VERITAS API",
        swagger_favicon_url="/static/favicon.ico"
    )


prefix_router = APIRouter(prefix="/veritas/api", default_response_class=ORJSONResponse)


@prefix_router.get("/")
async def checkEndpoint():
    return "ok"


@prefix_router.post("/subjectivity-score")
async def subjectivityScore(subjectivity_score_request: SubjectivityScoreRequest):
    return get_subjectivity_score(subjectivity_score_request)


@prefix_router.post("/sentiment-score")
async def subjectivityScore(sentiment_score_request: SentimentScoreRequest):
    return get_sentiment_score(sentiment_score_request)


app.include_router(prefix_router)
app.include_router(samples_router)

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from pathlib import Path
import traceback
from ..config import templates
from ..models import QuizStreaks, Users
from ..dependencies import db_dependency
from ..utils.auth_utils import redirect_to_login, get_current_user
from ..utils.theme_utils import get_theme_by_id


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        streak = max_streak = 0
        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get("id")).first()
        if streak_model:
            streak = streak_model.streak
            max_streak = streak_model.max_streak

        theme_id = db.query(Users.theme_id).filter(Users.id == user.get("id")).scalar()
        theme = get_theme_by_id(db=db, theme_id=theme_id)

        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "streak": streak,
                "max_streak": max_streak,
                "theme": theme,
            },
        )
    except Exception as e:
        print(traceback.format_exc())
        return redirect_to_login()
    
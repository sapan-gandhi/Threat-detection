# Fixing Red Line Errors in backend/main.py

## Plan Steps:
1. [ ] Remove unused imports `import database` and `import models` in backend/main.py
2. [ ] Add necessary imports: `from fastapi import Query` and Pydantic model for GoogleAuthToken
3. [ ] Move `models.Base.metadata.create_all(bind=engine)` to lifespan startup
4. [ ] Fix all `user_id: int` params to use `Query(...)`
5. [ ] Fix google_auth `token: dict` to Pydantic model
6. [ ] Add missing `Depends(get_db)` to endpoints
7. [ ] Add response_model where missing
8. [ ] [Complete] Verify no red lines

Current progress: Fixed imports, lifespan, user_id Query params for messages/history/dashboard/delete, response_models unqualified, login/register params, google token access, dashboard return. Replacing remaining models.XXX to XXX to resolve Pylance "models not defined".


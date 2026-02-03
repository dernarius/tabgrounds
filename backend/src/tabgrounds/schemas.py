from pydantic import BaseModel
from typing import Optional


class GameStatus(BaseModel):
    tournament_id: Optional[str]
    current_index: int
    is_completed: bool
    total_challenges: int
    current_challenge_description: Optional[str]


class AdvanceResult(BaseModel):
    status: str
    message: str
    new_state: Optional[GameStatus] = None

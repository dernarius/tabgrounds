import asyncio
from typing import List, Optional
from tabgrounds.challenges import BaseChallenge, DummyChallenge
from tabgrounds.schemas import GameStatus, AdvanceResult


class GameState:
    def __init__(self):
        self.tournament_id: Optional[str] = "tourn_1"
        self.current_challenge_index: int = 0
        self.is_completed: bool = False


class GameManager:
    def __init__(self):
        self.state = GameState()
        self.lock = asyncio.Lock()
        # Initialize with a fixed list of challenges acting as the "script"
        self.challenges: List[BaseChallenge] = [
            DummyChallenge(name="Challenge 1"),
            DummyChallenge(name="Challenge 2"),
            DummyChallenge(name="Challenge 3"),
        ]

    @property
    def current_challenge(self) -> Optional[BaseChallenge]:
        if self.state.is_completed:
            return None
        if 0 <= self.state.current_challenge_index < len(self.challenges):
            return self.challenges[self.state.current_challenge_index]
        return None

    async def advance_challenge(self) -> AdvanceResult:
        """
        Attempts to advance to the next challenge.
        Async thread-safe method using an asyncio lock.
        """
        async with self.lock:
            if self.state.is_completed:
                return AdvanceResult(status="error", message="Game already completed.")

            current = self.current_challenge
            if current:
                # Logic: Check completion
                current_completed = current.check_completion()
                # If check_completion becomes async later, await it here.

                if current_completed:
                    self.state.current_challenge_index += 1

                    if self.state.current_challenge_index >= len(self.challenges):
                        self.state.is_completed = True
                        return AdvanceResult(
                            status="completed",
                            message="All challenges completed!",
                            new_state=self.get_status_unsafe(),
                        )

                    return AdvanceResult(
                        status="advanced",
                        message="Advanced to next challenge.",
                        new_state=self.get_status_unsafe(),
                    )
                else:
                    return AdvanceResult(
                        status="error", message="Challenge not completed yet."
                    )
            return AdvanceResult(status="error", message="No active challenge.")

    async def get_status(self) -> GameStatus:
        """Async thread-safe status retrieval."""
        async with self.lock:
            return self.get_status_unsafe()

    def get_status_unsafe(self) -> GameStatus:
        """Helper to get status struct without re-locking (for internal use)."""
        return GameStatus(
            tournament_id=self.state.tournament_id,
            current_index=self.state.current_challenge_index,
            is_completed=self.state.is_completed,
            total_challenges=len(self.challenges),
            current_challenge_description=self.current_challenge.get_description()
            if self.current_challenge
            else None,
        )


# Global Singleton Instance
game_manager = GameManager()

import { useEffect, useState } from "react"
import { DefaultService } from "@/client/services/DefaultService"
import { OpenAPI } from "@/client/core/OpenAPI"
import { GameStatus } from "@/components/GameStatus"
import { AdvanceButton } from "@/components/AdvanceButton"
import type { GameStatus as GameStatusType } from "@/client/models/GameStatus"

// Configure API Base URL
OpenAPI.BASE = "http://localhost:8000"

function App() {
  const [status, setStatus] = useState<GameStatusType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await DefaultService.readRootGet()
        // Ensure we handle 'any' type safely, expecting { game_status: ... }
        if (response && response.game_status) {
          setStatus(response.game_status)
        }
      } catch (error) {
        console.error("Failed to fetch game status:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
  }, [])

  const handleStatusUpdate = (newStatus: GameStatusType) => {
    setStatus(newStatus)
  }

  return (
    <div className="container mx-auto p-8 flex flex-col items-center gap-8 min-h-screen justify-center">
      <h1 className="text-4xl font-bold mb-4">Tabgrounds</h1>

      <GameStatus status={status} loading={loading} />

      <AdvanceButton
        onAdvance={handleStatusUpdate}
        disabled={loading || status?.is_completed}
      />
    </div>
  )
}

export default App

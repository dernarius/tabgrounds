import type { GameStatus } from "@/client/models/GameStatus"
import { Button } from "@/components/ui/button"
import { DefaultService } from "@/client/services/DefaultService"
import { useState } from "react"
import { Loader2 } from "lucide-react"

interface AdvanceButtonProps {
    onAdvance: (newState: GameStatus) => void
    disabled?: boolean
}

export function AdvanceButton({ onAdvance, disabled }: AdvanceButtonProps) {
    const [loading, setLoading] = useState(false)

    const handleAdvance = async () => {
        setLoading(true)
        try {
            const result = await DefaultService.advanceGameAdvancePost()
            if (result.new_state) {
                onAdvance(result.new_state)
            }
        } catch (error) {
            console.error("Failed to advance game:", error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Button onClick={handleAdvance} disabled={disabled || loading}>
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Advance Game
        </Button>
    )
}

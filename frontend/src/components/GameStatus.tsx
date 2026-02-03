import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { GameStatus as GameStatusType } from "@/client/models/GameStatus"

interface GameStatusProps {
    status: GameStatusType | null
    loading: boolean
}

export function GameStatus({ status, loading }: GameStatusProps) {
    if (loading) {
        return (
            <Card className="w-[350px]">
                <CardHeader>
                    <CardTitle>Loading...</CardTitle>
                </CardHeader>
            </Card>
        )
    }

    if (!status) {
        return (
            <Card className="w-[350px]">
                <CardHeader>
                    <CardTitle>No Game Status</CardTitle>
                </CardHeader>
            </Card>
        )
    }

    return (
        <Card className="w-[350px]">
            <CardHeader>
                <CardTitle>Game Status</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col gap-2">
                    <div className="flex justify-between">
                        <span className="font-semibold">Tournament ID:</span>
                        <span>{status.tournament_id || "None"}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="font-semibold">Challenge:</span>
                        <span>{status.current_index} / {status.total_challenges}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="font-semibold">Completed:</span>
                        <span>{status.is_completed ? "Yes" : "No"}</span>
                    </div>
                    {status.current_challenge_description && (
                        <div className="pt-2 border-t mt-2">
                            <p className="text-sm text-muted-foreground">
                                {status.current_challenge_description}
                            </p>
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}

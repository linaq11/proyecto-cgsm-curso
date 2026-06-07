import { CosmicButton } from "@/components/ui/cosmic-button"

export default function TestCultPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-12">
      <h1 className="text-2xl font-semibold text-foreground">
        Smoke test :: Cult UI @cult-ui registry
      </h1>
      <CosmicButton as="button">Cult UI funciona</CosmicButton>
    </main>
  )
}

import type { Metadata } from "next";
import { ProgDeck } from "@/components/presentation/prog-deck";

export const metadata: Metadata = {
  title: "Pipeline multilenguaje CGSM · Programación en SIG — Lina Quintero Fonseca",
  description:
    "Proyecto final de Programación en SIG: pipeline multilenguaje (Python, R, Julia) para el monitoreo del manglar de la Ciénaga Grande de Santa Marta, 2013–2025. Universidad Nacional de Colombia.",
};

export default function Home() {
  return <ProgDeck />;
}

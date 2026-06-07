import type { Metadata } from "next";
import { ThesisDeck } from "@/components/presentation/thesis-deck";

export const metadata: Metadata = {
  title: "GeoAI Digital Twin · Thesis Defense — Lina Quintero Fonseca",
  description:
    "Master's thesis proposal defense: a GeoAI-based Digital Twin for dynamic monitoring of the Cienaga Grande de Santa Marta. Universidad Nacional de Colombia.",
};

export default function TesisPage() {
  return <ThesisDeck />;
}

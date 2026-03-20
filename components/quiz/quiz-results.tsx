"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  BarChart3, 
  MapPin, 
  Camera, 
  RefreshCcw, 
  AlertTriangle,
  CheckCircle2,
  AlertCircle,
  XCircle
} from "lucide-react"
import type { QuizResult } from "@/app/quiz/page"

interface QuizResultsProps {
  results: QuizResult[]
  onRetake: () => void
}

const conditionInfo: Record<string, { 
  name: string
  color: string
  bgColor: string
  description: string 
}> = {
  depression: {
    name: "Depression",
    color: "text-coral",
    bgColor: "bg-coral",
    description: "Depression affects mood, energy, and daily functioning. It is highly treatable with proper support.",
  },
  anxiety: {
    name: "Anxiety",
    color: "text-teal",
    bgColor: "bg-teal",
    description: "Anxiety involves excessive worry and nervousness. Management techniques and therapy can help significantly.",
  },
  ptsd: {
    name: "PTSD",
    color: "text-lavender",
    bgColor: "bg-lavender",
    description: "PTSD can develop after traumatic experiences. Professional support and coping strategies are very effective.",
  },
  bipolar: {
    name: "Bipolar Disorder",
    color: "text-mint",
    bgColor: "bg-mint",
    description: "Bipolar involves mood episodes. With treatment, most people with bipolar disorder lead fulfilling lives.",
  },
}

const severityInfo: Record<string, {
  label: string
  icon: React.ElementType
  color: string
  bgColor: string
}> = {
  minimal: {
    label: "Minimal",
    icon: CheckCircle2,
    color: "text-mint",
    bgColor: "bg-mint/10",
  },
  mild: {
    label: "Mild",
    icon: AlertCircle,
    color: "text-sunshine",
    bgColor: "bg-sunshine/10",
  },
  moderate: {
    label: "Moderate",
    icon: AlertTriangle,
    color: "text-coral",
    bgColor: "bg-coral/10",
  },
  severe: {
    label: "Severe",
    icon: XCircle,
    color: "text-destructive",
    bgColor: "bg-destructive/10",
  },
}

export function QuizResults({ results, onRetake }: QuizResultsProps) {
  const primaryResult = results.reduce((prev, current) => 
    current.score > prev.score ? current : prev
  )
  const hasConcerning = results.some(r => r.severity === "moderate" || r.severity === "severe")

  return (
    <div className="mx-auto max-w-4xl">
      {/* Header */}
      <div className="mb-8 text-center">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">
          <BarChart3 className="h-10 w-10 text-primary" />
        </div>
        <h1 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl">
          Your Assessment Results
        </h1>
        <p className="mx-auto max-w-xl text-pretty text-lg text-muted-foreground">
          Based on your responses, here is an overview of your mental health indicators.
        </p>
      </div>

      {/* Primary Result */}
      {hasConcerning && (
        <Card className="mb-8 border-2 border-primary/20 bg-primary/5">
          <CardContent className="p-6">
            <div className="flex flex-col items-center gap-4 text-center md:flex-row md:text-left">
              <div className={`flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl ${conditionInfo[primaryResult.condition].bgColor}`}>
                <AlertTriangle className="h-8 w-8 text-primary-foreground" />
              </div>
              <div>
                <h3 className="mb-1 text-xl font-semibold text-foreground">
                  Primary Indicator: {conditionInfo[primaryResult.condition].name}
                </h3>
                <p className="text-muted-foreground">
                  {conditionInfo[primaryResult.condition].description}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results Grid */}
      <div className="mb-8 grid gap-4 md:grid-cols-2">
        {results.map((result) => {
          const condition = conditionInfo[result.condition]
          const severity = severityInfo[result.severity]
          const SeverityIcon = severity.icon
          const maxScore = result.condition === "depression" ? 12 : 6
          const percentage = Math.round((result.score / maxScore) * 100)

          return (
            <Card key={result.condition} className="border-2 border-border">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className={`text-lg ${condition.color}`}>
                    {condition.name}
                  </CardTitle>
                  <span className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium ${severity.bgColor} ${severity.color}`}>
                    <SeverityIcon className="h-4 w-4" />
                    {severity.label}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="mb-3">
                  <div className="mb-1 flex justify-between text-sm">
                    <span className="text-muted-foreground">Score: {result.score}/{maxScore}</span>
                    <span className="font-medium">{percentage}%</span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                    <div 
                      className={`h-full ${condition.bgColor} transition-all`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  {condition.description}
                </p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Recommendations */}
      <Card className="mb-8 border-2 border-border">
        <CardHeader>
          <CardTitle>Recommended Next Steps</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <Link href="/emotion-detect" className="group">
              <div className="flex items-start gap-4 rounded-xl border-2 border-border p-4 transition-all hover:border-primary/50 hover:bg-muted">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-teal/10">
                  <Camera className="h-6 w-6 text-teal" />
                </div>
                <div>
                  <h4 className="mb-1 font-semibold text-foreground group-hover:text-primary">
                    Emotion Detection
                  </h4>
                  <p className="text-sm text-muted-foreground">
                    Get a deeper analysis through facial emotion recognition
                  </p>
                </div>
              </div>
            </Link>

            <Link href="/clinics" className="group">
              <div className="flex items-start gap-4 rounded-xl border-2 border-border p-4 transition-all hover:border-primary/50 hover:bg-muted">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-lavender/10">
                  <MapPin className="h-6 w-6 text-lavender" />
                </div>
                <div>
                  <h4 className="mb-1 font-semibold text-foreground group-hover:text-primary">
                    Find Nearby Clinics
                  </h4>
                  <p className="text-sm text-muted-foreground">
                    Connect with mental health professionals in your area
                  </p>
                </div>
              </div>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <Card className="mb-8 border-2 border-sunshine/30 bg-sunshine-light/30">
        <CardContent className="flex gap-4 p-6">
          <AlertTriangle className="h-6 w-6 shrink-0 text-sunshine" />
          <div>
            <h4 className="mb-1 font-semibold text-foreground">Important Reminder</h4>
            <p className="text-sm text-muted-foreground">
              This assessment provides indicators only and is not a clinical diagnosis. 
              Please consult with a qualified healthcare professional for proper evaluation and treatment. 
              If you are in crisis, call 988 (Suicide & Crisis Lifeline) immediately.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
        <Button
          variant="outline"
          onClick={onRetake}
          className="gap-2"
        >
          <RefreshCcw className="h-4 w-4" />
          Retake Assessment
        </Button>
        <Link href="/clinics">
          <Button className="gap-2 bg-primary hover:bg-primary/90">
            <MapPin className="h-4 w-4" />
            Find Professional Help
          </Button>
        </Link>
      </div>
    </div>
  )
}

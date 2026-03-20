"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowLeft, ArrowRight } from "lucide-react"

interface QuizQuestionProps {
  question: {
    id: number
    question: string
    category: string
    options: { text: string; score: number }[]
  }
  currentIndex: number
  totalQuestions: number
  onAnswer: (score: number) => void
  onPrevious: () => void
  canGoBack: boolean
}

const categoryColors: Record<string, { bg: string; text: string; label: string }> = {
  depression: { bg: "bg-coral/10", text: "text-coral", label: "Depression" },
  anxiety: { bg: "bg-teal/10", text: "text-teal", label: "Anxiety" },
  ptsd: { bg: "bg-lavender/10", text: "text-lavender", label: "PTSD" },
  bipolar: { bg: "bg-mint/10", text: "text-mint", label: "Bipolar" },
}

export function QuizQuestion({
  question,
  currentIndex,
  totalQuestions,
  onAnswer,
  onPrevious,
  canGoBack,
}: QuizQuestionProps) {
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const progress = ((currentIndex + 1) / totalQuestions) * 100
  const categoryStyle = categoryColors[question.category]

  const handleOptionClick = (score: number) => {
    setSelectedOption(score)
  }

  const handleNext = () => {
    if (selectedOption !== null) {
      onAnswer(selectedOption)
      setSelectedOption(null)
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      {/* Progress */}
      <div className="mb-8">
        <div className="mb-2 flex items-center justify-between text-sm">
          <span className="text-muted-foreground">
            Question {currentIndex + 1} of {totalQuestions}
          </span>
          <span className="font-medium text-foreground">{Math.round(progress)}%</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
          <div 
            className="h-full bg-primary transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Category Badge */}
      <div className="mb-6 flex justify-center">
        <span className={`rounded-full px-4 py-1.5 text-sm font-medium ${categoryStyle.bg} ${categoryStyle.text}`}>
          {categoryStyle.label} Assessment
        </span>
      </div>

      {/* Question */}
      <Card className="mb-8 border-2 border-border">
        <CardContent className="p-8">
          <h2 className="mb-8 text-center text-xl font-semibold text-foreground md:text-2xl">
            {question.question}
          </h2>

          {/* Options */}
          <div className="space-y-3">
            {question.options.map((option) => (
              <button
                key={option.score}
                onClick={() => handleOptionClick(option.score)}
                className={`w-full rounded-xl border-2 p-4 text-left transition-all ${
                  selectedOption === option.score
                    ? "border-primary bg-primary/10 ring-2 ring-primary/20"
                    : "border-border bg-card hover:border-primary/50 hover:bg-muted"
                }`}
              >
                <div className="flex items-center gap-4">
                  <div
                    className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-all ${
                      selectedOption === option.score
                        ? "border-primary bg-primary"
                        : "border-muted-foreground"
                    }`}
                  >
                    {selectedOption === option.score && (
                      <div className="h-2 w-2 rounded-full bg-primary-foreground" />
                    )}
                  </div>
                  <span className={`font-medium ${
                    selectedOption === option.score ? "text-foreground" : "text-muted-foreground"
                  }`}>
                    {option.text}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={onPrevious}
          disabled={!canGoBack}
          className="gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Previous
        </Button>

        <Button
          onClick={handleNext}
          disabled={selectedOption === null}
          className="gap-2 bg-primary hover:bg-primary/90"
        >
          {currentIndex === totalQuestions - 1 ? "See Results" : "Next"}
          <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

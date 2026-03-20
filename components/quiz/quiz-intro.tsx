"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ClipboardList, Clock, Shield, ArrowRight, AlertCircle } from "lucide-react"

interface QuizIntroProps {
  onStart: () => void
}

export function QuizIntro({ onStart }: QuizIntroProps) {
  return (
    <div className="mx-auto max-w-3xl">
      {/* Header */}
      <div className="mb-8 text-center">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">
          <ClipboardList className="h-10 w-10 text-primary" />
        </div>
        <h1 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl">
          Mental Health Self-Assessment
        </h1>
        <p className="mx-auto max-w-xl text-pretty text-lg text-muted-foreground">
          This questionnaire will help identify potential indicators for Depression, 
          Anxiety, PTSD, and Bipolar Disorder based on your responses.
        </p>
      </div>

      {/* Info Cards */}
      <div className="mb-8 grid gap-4 md:grid-cols-3">
        <Card className="border-2 border-coral/20 bg-coral-light/20">
          <CardContent className="flex flex-col items-center p-6 text-center">
            <ClipboardList className="mb-3 h-8 w-8 text-coral" />
            <h3 className="mb-1 font-semibold text-foreground">12 Questions</h3>
            <p className="text-sm text-muted-foreground">
              Carefully designed questions covering multiple areas
            </p>
          </CardContent>
        </Card>

        <Card className="border-2 border-teal/20 bg-teal-light/20">
          <CardContent className="flex flex-col items-center p-6 text-center">
            <Clock className="mb-3 h-8 w-8 text-teal" />
            <h3 className="mb-1 font-semibold text-foreground">5-10 Minutes</h3>
            <p className="text-sm text-muted-foreground">
              Quick assessment you can complete at your own pace
            </p>
          </CardContent>
        </Card>

        <Card className="border-2 border-lavender/20 bg-lavender-light/20">
          <CardContent className="flex flex-col items-center p-6 text-center">
            <Shield className="mb-3 h-8 w-8 text-lavender" />
            <h3 className="mb-1 font-semibold text-foreground">100% Private</h3>
            <p className="text-sm text-muted-foreground">
              Your answers are confidential and secure
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Instructions */}
      <Card className="mb-8 border-2 border-border">
        <CardContent className="p-6">
          <h3 className="mb-4 text-lg font-semibold text-foreground">
            How to Take This Assessment
          </h3>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                1
              </span>
              <span className="text-muted-foreground">
                Read each question carefully and think about how you have felt over the <strong>past two weeks</strong>.
              </span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                2
              </span>
              <span className="text-muted-foreground">
                Select the answer that best describes your experience. There are no right or wrong answers.
              </span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                3
              </span>
              <span className="text-muted-foreground">
                Be honest with yourself for the most accurate results.
              </span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                4
              </span>
              <span className="text-muted-foreground">
                After completing the quiz, you will receive personalized results and recommendations.
              </span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <Card className="mb-8 border-2 border-sunshine/30 bg-sunshine-light/30">
        <CardContent className="flex gap-4 p-6">
          <AlertCircle className="h-6 w-6 shrink-0 text-sunshine" />
          <div>
            <h4 className="mb-1 font-semibold text-foreground">Important Notice</h4>
            <p className="text-sm text-muted-foreground">
              This assessment is not a diagnostic tool. The results are for educational purposes only 
              and should not replace professional medical advice, diagnosis, or treatment. 
              If you are experiencing a mental health crisis, please contact a healthcare professional 
              or call 988 (Suicide & Crisis Lifeline) immediately.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Start Button */}
      <div className="text-center">
        <Button 
          size="lg" 
          onClick={onStart}
          className="group h-14 gap-2 rounded-xl bg-primary px-8 text-lg font-semibold hover:bg-primary/90"
        >
          Begin Assessment
          <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
        </Button>
      </div>
    </div>
  )
}

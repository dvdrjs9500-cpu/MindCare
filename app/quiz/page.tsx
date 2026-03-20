"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { QuizIntro } from "@/components/quiz/quiz-intro"
import { QuizQuestion } from "@/components/quiz/quiz-question"
import { QuizResults } from "@/components/quiz/quiz-results"

const quizQuestions = [
  {
    id: 1,
    question: "Over the past two weeks, how often have you felt down, depressed, or hopeless?",
    category: "depression",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 2,
    question: "How often have you had little interest or pleasure in doing things?",
    category: "depression",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 3,
    question: "How often have you felt nervous, anxious, or on edge?",
    category: "anxiety",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 4,
    question: "How often have you had trouble relaxing or felt restless?",
    category: "anxiety",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 5,
    question: "Do you have recurring, unwanted memories or nightmares of a stressful experience?",
    category: "ptsd",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Rarely", score: 1 },
      { text: "Sometimes", score: 2 },
      { text: "Very often", score: 3 },
    ],
  },
  {
    id: 6,
    question: "Do you avoid places, people, or activities that remind you of a past traumatic event?",
    category: "ptsd",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Rarely", score: 1 },
      { text: "Sometimes", score: 2 },
      { text: "Very often", score: 3 },
    ],
  },
  {
    id: 7,
    question: "Have you experienced periods of unusually high energy, reduced need for sleep, or racing thoughts?",
    category: "bipolar",
    options: [
      { text: "Never", score: 0 },
      { text: "Rarely", score: 1 },
      { text: "Sometimes", score: 2 },
      { text: "Frequently", score: 3 },
    ],
  },
  {
    id: 8,
    question: "Have you had times when you felt extremely happy or energetic, followed by periods of depression?",
    category: "bipolar",
    options: [
      { text: "Never", score: 0 },
      { text: "Rarely", score: 1 },
      { text: "Sometimes", score: 2 },
      { text: "Frequently", score: 3 },
    ],
  },
  {
    id: 9,
    question: "How often have you had trouble falling or staying asleep, or sleeping too much?",
    category: "depression",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 10,
    question: "How often have you felt tired or had little energy?",
    category: "depression",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 11,
    question: "How often do you feel easily annoyed or irritable?",
    category: "anxiety",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Several days", score: 1 },
      { text: "More than half the days", score: 2 },
      { text: "Nearly every day", score: 3 },
    ],
  },
  {
    id: 12,
    question: "Do you feel emotionally numb or detached from others?",
    category: "ptsd",
    options: [
      { text: "Not at all", score: 0 },
      { text: "Rarely", score: 1 },
      { text: "Sometimes", score: 2 },
      { text: "Very often", score: 3 },
    ],
  },
]

export type QuizAnswer = {
  questionId: number
  score: number
  category: string
}

export type QuizResult = {
  condition: "depression" | "anxiety" | "ptsd" | "bipolar"
  score: number
  severity: "minimal" | "mild" | "moderate" | "severe"
}

export default function QuizPage() {
  const [stage, setStage] = useState<"intro" | "quiz" | "results">("intro")
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<QuizAnswer[]>([])

  const handleStartQuiz = () => {
    setStage("quiz")
    setCurrentQuestion(0)
    setAnswers([])
  }

  const handleAnswer = (score: number) => {
    const question = quizQuestions[currentQuestion]
    const newAnswer: QuizAnswer = {
      questionId: question.id,
      score,
      category: question.category,
    }
    
    setAnswers([...answers, newAnswer])
    
    if (currentQuestion < quizQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      setStage("results")
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
      setAnswers(answers.slice(0, -1))
    }
  }

  const calculateResults = (): QuizResult[] => {
    const categories = ["depression", "anxiety", "ptsd", "bipolar"] as const
    
    return categories.map((category) => {
      const categoryAnswers = answers.filter(a => a.category === category)
      const totalScore = categoryAnswers.reduce((sum, a) => sum + a.score, 0)
      const maxScore = categoryAnswers.length * 3
      const percentage = (totalScore / maxScore) * 100
      
      let severity: QuizResult["severity"]
      if (percentage <= 25) severity = "minimal"
      else if (percentage <= 50) severity = "mild"
      else if (percentage <= 75) severity = "moderate"
      else severity = "severe"
      
      return {
        condition: category,
        score: totalScore,
        severity,
      }
    })
  }

  const handleRetake = () => {
    setStage("intro")
    setCurrentQuestion(0)
    setAnswers([])
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-12">
        {stage === "intro" && <QuizIntro onStart={handleStartQuiz} />}
        
        {stage === "quiz" && (
          <QuizQuestion
            question={quizQuestions[currentQuestion]}
            currentIndex={currentQuestion}
            totalQuestions={quizQuestions.length}
            onAnswer={handleAnswer}
            onPrevious={handlePrevious}
            canGoBack={currentQuestion > 0}
          />
        )}
        
        {stage === "results" && (
          <QuizResults 
            results={calculateResults()} 
            onRetake={handleRetake}
          />
        )}
      </main>
      <Footer />
    </div>
  )
}

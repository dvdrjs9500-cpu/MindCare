"use client"

import { ClipboardList, Camera, MapPin, BookOpen, Heart, Brain } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

const features = [
  {
    icon: ClipboardList,
    title: "Self-Assessment Quiz",
    description: "Answer carefully designed questions to understand your mental health state. Our quiz detects Depression, Anxiety, PTSD, and Bipolar indicators.",
    color: "bg-coral/10 text-coral",
    borderColor: "border-coral/20",
  },
  {
    icon: Camera,
    title: "Emotion Detection",
    description: "Using advanced AI and facial recognition, we analyze your expressions while you share your thoughts for a comprehensive emotional assessment.",
    color: "bg-teal/10 text-teal",
    borderColor: "border-teal/20",
  },
  {
    icon: MapPin,
    title: "Find Nearby Clinics",
    description: "Get personalized recommendations for mental health professionals near you. Our GPS feature helps you find the right support quickly.",
    color: "bg-lavender/10 text-lavender",
    borderColor: "border-lavender/20",
  },
  {
    icon: BookOpen,
    title: "Educational Resources",
    description: "Access comprehensive information about mental health conditions, coping strategies, and wellness tips curated by experts.",
    color: "bg-mint/10 text-mint",
    borderColor: "border-mint/20",
  },
  {
    icon: Heart,
    title: "Personal Workbook",
    description: "Maintain a private journal to track your thoughts, feelings, and progress. Reflect on your journey towards better mental health.",
    color: "bg-sunshine/10 text-sunshine",
    borderColor: "border-sunshine/20",
  },
  {
    icon: Brain,
    title: "AI-Powered Insights",
    description: "Our machine learning algorithms provide personalized insights based on your assessments and emotional patterns.",
    color: "bg-primary/10 text-primary",
    borderColor: "border-primary/20",
  },
]

export function FeaturesSection() {
  return (
    <section className="px-4 py-20" id="features">
      <div className="container mx-auto">
        <div className="mx-auto mb-16 max-w-2xl text-center">
          <span className="mb-4 inline-block rounded-full bg-secondary/20 px-4 py-1.5 text-sm font-medium text-secondary-foreground">
            Comprehensive Features
          </span>
          <h2 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl lg:text-5xl">
            Everything You Need for Mental Wellness
          </h2>
          <p className="text-pretty text-lg text-muted-foreground">
            A complete toolkit designed to help you understand, track, and improve your mental health journey.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <Card 
              key={feature.title} 
              className={`group border-2 ${feature.borderColor} bg-card transition-all duration-300 hover:-translate-y-1 hover:shadow-xl`}
            >
              <CardContent className="p-6">
                <div className={`mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl ${feature.color}`}>
                  <feature.icon className="h-7 w-7" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-card-foreground">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

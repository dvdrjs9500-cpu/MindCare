"use client"

import { UserPlus, ClipboardCheck, BarChart3, Stethoscope } from "lucide-react"

const steps = [
  {
    step: "01",
    icon: UserPlus,
    title: "Create Your Account",
    description: "Sign up with your details to access all features. Your information is always kept secure and confidential.",
    color: "bg-coral text-coral-foreground",
  },
  {
    step: "02",
    icon: ClipboardCheck,
    title: "Take the Assessment",
    description: "Complete our comprehensive quiz and emotion detection test. Speak for 1 minute while we analyze your expressions.",
    color: "bg-teal text-teal-foreground",
  },
  {
    step: "03",
    icon: BarChart3,
    title: "Get Your Results",
    description: "Receive detailed insights about your mental health state including potential indicators for Depression, Anxiety, PTSD, or Bipolar.",
    color: "bg-lavender text-lavender-foreground",
  },
  {
    step: "04",
    icon: Stethoscope,
    title: "Find Support",
    description: "Based on your results, we recommend nearby mental health professionals and clinics with GPS navigation.",
    color: "bg-mint text-mint-foreground",
  },
]

export function HowItWorksSection() {
  return (
    <section className="bg-muted/50 px-4 py-20">
      <div className="container mx-auto">
        <div className="mx-auto mb-16 max-w-2xl text-center">
          <span className="mb-4 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
            Simple Process
          </span>
          <h2 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl lg:text-5xl">
            How It Works
          </h2>
          <p className="text-pretty text-lg text-muted-foreground">
            Your journey to better mental health starts with four simple steps.
          </p>
        </div>

        <div className="relative">
          {/* Connection line for desktop */}
          <div className="absolute left-0 right-0 top-24 hidden h-0.5 bg-border lg:block" />
          
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {steps.map((item, index) => (
              <div key={item.step} className="relative text-center">
                {/* Step number badge */}
                <div className="relative mx-auto mb-6">
                  <div className={`mx-auto flex h-20 w-20 items-center justify-center rounded-2xl ${item.color} shadow-lg`}>
                    <item.icon className="h-10 w-10" />
                  </div>
                  <span className="absolute -right-2 -top-2 flex h-8 w-8 items-center justify-center rounded-full bg-foreground text-sm font-bold text-background">
                    {item.step}
                  </span>
                </div>

                {/* Arrow connector for desktop */}
                {index < steps.length - 1 && (
                  <div className="absolute right-0 top-24 hidden -translate-y-1/2 translate-x-1/2 lg:block">
                    <div className="h-3 w-3 rotate-45 border-r-2 border-t-2 border-foreground/30" />
                  </div>
                )}

                <h3 className="mb-3 text-xl font-semibold text-foreground">
                  {item.title}
                </h3>
                <p className="text-muted-foreground">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

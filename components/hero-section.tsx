"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, Sparkles, Shield, Heart } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden px-4 py-20 md:py-32">
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute left-1/4 top-20 h-72 w-72 rounded-full bg-coral-light/50 blur-3xl" />
        <div className="absolute right-1/4 top-40 h-64 w-64 rounded-full bg-teal-light/50 blur-3xl" />
        <div className="absolute bottom-20 left-1/3 h-56 w-56 rounded-full bg-lavender-light/50 blur-3xl" />
      </div>

      <div className="container mx-auto">
        <div className="mx-auto max-w-4xl text-center">
          {/* Badge */}
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
            <Sparkles className="h-4 w-4" />
            <span>Your mental health matters</span>
          </div>

          {/* Heading */}
          <h1 className="mb-6 text-balance text-4xl font-bold tracking-tight text-foreground md:text-6xl lg:text-7xl">
            Understand Your Mind,{" "}
            <span className="bg-gradient-to-r from-primary via-secondary to-teal bg-clip-text text-transparent">
              Embrace Your Journey
            </span>
          </h1>

          {/* Subheading */}
          <p className="mx-auto mb-10 max-w-2xl text-pretty text-lg text-muted-foreground md:text-xl">
            Take the first step towards better mental health. Our AI-powered platform helps you 
            understand your emotions, detect signs of depression, and connect you with professional support.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/quiz">
              <Button size="lg" className="group h-14 gap-2 rounded-xl bg-primary px-8 text-lg font-semibold hover:bg-primary/90">
                Take Self Assessment
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="/info">
              <Button size="lg" variant="outline" className="h-14 rounded-xl px-8 text-lg font-semibold">
                Learn More
              </Button>
            </Link>
          </div>

          {/* Trust badges */}
          <div className="mt-12 flex flex-wrap items-center justify-center gap-8">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-mint/20">
                <Shield className="h-5 w-5 text-mint" />
              </div>
              <span>100% Confidential</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-coral/20">
                <Heart className="h-5 w-5 text-coral" />
              </div>
              <span>Evidence-Based</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-teal/20">
                <Sparkles className="h-5 w-5 text-teal" />
              </div>
              <span>AI-Powered Analysis</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

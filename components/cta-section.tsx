"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, Heart } from "lucide-react"

export function CTASection() {
  return (
    <section className="relative overflow-hidden px-4 py-20">
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute right-1/4 top-10 h-48 w-48 rounded-full bg-sunshine-light/60 blur-3xl" />
        <div className="absolute bottom-10 left-1/4 h-56 w-56 rounded-full bg-mint-light/60 blur-3xl" />
      </div>

      <div className="container mx-auto">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
            <Heart className="h-8 w-8 text-primary" />
          </div>
          
          <h2 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl lg:text-5xl">
            Ready to Start Your Wellness Journey?
          </h2>
          
          <p className="mx-auto mb-8 max-w-xl text-pretty text-lg text-muted-foreground">
            Take the first step towards understanding your mental health. 
            Our free assessment takes just a few minutes and can make a world of difference.
          </p>

          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/quiz">
              <Button size="lg" className="group h-14 gap-2 rounded-xl bg-primary px-8 text-lg font-semibold hover:bg-primary/90">
                Start Free Assessment
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="/signup">
              <Button size="lg" variant="outline" className="h-14 rounded-xl px-8 text-lg font-semibold">
                Create Account
              </Button>
            </Link>
          </div>

          <p className="mt-6 text-sm text-muted-foreground">
            No credit card required. Your privacy is our priority.
          </p>
        </div>
      </div>
    </section>
  )
}

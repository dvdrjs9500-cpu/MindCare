"use client"

import Link from "next/link"
import { Brain, Mail, Phone, MapPin } from "lucide-react"

const footerLinks = {
  features: [
    { label: "Self Assessment", href: "/quiz" },
    { label: "Emotion Detection", href: "/emotion-detect" },
    { label: "Find Clinics", href: "/clinics" },
    { label: "Resources", href: "/info" },
    { label: "Workbook", href: "/workbook" },
  ],
  support: [
    { label: "Help Center", href: "#" },
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
    { label: "Contact Us", href: "#" },
  ],
  resources: [
    { label: "About Depression", href: "/info" },
    { label: "About Anxiety", href: "/info" },
    { label: "About PTSD", href: "/info" },
    { label: "About Bipolar", href: "/info" },
  ],
}

export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/30">
      <div className="container mx-auto px-4 py-12">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-5">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link href="/" className="mb-4 flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary">
                <Brain className="h-6 w-6 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold text-foreground">MindCare</span>
            </Link>
            <p className="mb-6 max-w-sm text-muted-foreground">
              Your trusted companion on the journey to better mental health. 
              We are here to help you understand, track, and improve your wellness.
            </p>
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Mail className="h-4 w-4" />
                <span>support@mindcare.com</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Phone className="h-4 w-4" />
                <span>Crisis Hotline: 988</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>Available Worldwide</span>
              </div>
            </div>
          </div>

          {/* Features */}
          <div>
            <h4 className="mb-4 font-semibold text-foreground">Features</h4>
            <ul className="space-y-2">
              {footerLinks.features.map((link) => (
                <li key={link.label}>
                  <Link 
                    href={link.href} 
                    className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="mb-4 font-semibold text-foreground">Resources</h4>
            <ul className="space-y-2">
              {footerLinks.resources.map((link) => (
                <li key={link.label}>
                  <Link 
                    href={link.href} 
                    className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="mb-4 font-semibold text-foreground">Support</h4>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.label}>
                  <Link 
                    href={link.href} 
                    className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-8 md:flex-row">
          <p className="text-sm text-muted-foreground">
            © 2026 MindCare. All rights reserved.
          </p>
          <p className="text-center text-sm text-muted-foreground">
            If you are in crisis, please call{" "}
            <span className="font-semibold text-primary">988</span> (Suicide & Crisis Lifeline)
          </p>
        </div>
      </div>
    </footer>
  )
}

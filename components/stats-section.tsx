"use client"

const stats = [
  {
    value: "300M+",
    label: "People Affected Worldwide",
    description: "Depression affects millions globally each year",
  },
  {
    value: "1 in 15",
    label: "Adults Suffer Annually",
    description: "Every year, depression impacts countless lives",
  },
  {
    value: "80%",
    label: "Treatment Success Rate",
    description: "With proper help, most people improve significantly",
  },
  {
    value: "24/7",
    label: "Support Available",
    description: "Our resources are always here for you",
  },
]

export function StatsSection() {
  return (
    <section className="px-4 py-20">
      <div className="container mx-auto">
        <div className="overflow-hidden rounded-3xl bg-gradient-to-br from-primary via-primary to-secondary p-8 md:p-12">
          <div className="mx-auto mb-12 max-w-2xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold text-primary-foreground md:text-4xl">
              Mental Health Matters More Than Ever
            </h2>
            <p className="text-pretty text-primary-foreground/80">
              Understanding the scale of mental health challenges helps us work together towards better solutions.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => (
              <div 
                key={stat.label} 
                className="rounded-2xl bg-primary-foreground/10 p-6 text-center backdrop-blur-sm"
              >
                <div className="mb-2 text-4xl font-bold text-primary-foreground md:text-5xl">
                  {stat.value}
                </div>
                <div className="mb-2 text-lg font-semibold text-primary-foreground">
                  {stat.label}
                </div>
                <div className="text-sm text-primary-foreground/70">
                  {stat.description}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

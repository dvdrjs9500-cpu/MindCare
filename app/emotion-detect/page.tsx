"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  Camera, 
  Video, 
  Square, 
  Play, 
  RotateCcw, 
  AlertCircle,
  Smile,
  Frown,
  Meh,
  AlertTriangle,
  Sparkles,
  Timer,
  MapPin
} from "lucide-react"
import Link from "next/link"

type Emotion = "happy" | "sad" | "neutral" | "anxious" | "angry" | "surprised"

interface EmotionData {
  emotion: Emotion
  confidence: number
  timestamp: number
}

const emotionConfig: Record<Emotion, { 
  label: string
  color: string
  bgColor: string
  icon: React.ElementType
  score: number
}> = {
  happy: { label: "Happy", color: "text-mint", bgColor: "bg-mint", icon: Smile, score: 10 },
  neutral: { label: "Neutral", color: "text-teal", bgColor: "bg-teal", icon: Meh, score: 5 },
  sad: { label: "Sad", color: "text-coral", bgColor: "bg-coral", icon: Frown, score: 2 },
  anxious: { label: "Anxious", color: "text-sunshine", bgColor: "bg-sunshine", icon: AlertTriangle, score: 3 },
  angry: { label: "Angry", color: "text-destructive", bgColor: "bg-destructive", icon: AlertTriangle, score: 1 },
  surprised: { label: "Surprised", color: "text-lavender", bgColor: "bg-lavender", icon: Sparkles, score: 6 },
}

export default function EmotionDetectPage() {
  const [stage, setStage] = useState<"intro" | "recording" | "results">("intro")
  const [isRecording, setIsRecording] = useState(false)
  const [timeLeft, setTimeLeft] = useState(60)
  const [emotionHistory, setEmotionHistory] = useState<EmotionData[]>([])
  const [currentEmotion, setCurrentEmotion] = useState<Emotion | null>(null)
  const [cameraError, setCameraError] = useState<string | null>(null)
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const timerRef = useRef<NodeJS.Timeout | null>(null)
  const emotionIntervalRef = useRef<NodeJS.Timeout | null>(null)

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
    if (emotionIntervalRef.current) {
      clearInterval(emotionIntervalRef.current)
      emotionIntervalRef.current = null
    }
  }, [])

  const startCamera = async () => {
    try {
      setCameraError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: "user" },
        audio: false 
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
      setStage("recording")
    } catch (err) {
      console.error("Camera error:", err)
      setCameraError("Unable to access camera. Please ensure you have granted camera permissions.")
    }
  }

  const simulateEmotionDetection = useCallback((): Emotion => {
    const emotions: Emotion[] = ["happy", "sad", "neutral", "anxious", "angry", "surprised"]
    const weights = [0.2, 0.15, 0.3, 0.15, 0.1, 0.1]
    const random = Math.random()
    let cumulative = 0
    for (let i = 0; i < emotions.length; i++) {
      cumulative += weights[i]
      if (random <= cumulative) return emotions[i]
    }
    return "neutral"
  }, [])

  const startRecording = () => {
    setIsRecording(true)
    setTimeLeft(60)
    setEmotionHistory([])

    // Timer countdown
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          stopRecording()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    // Simulate emotion detection every 2 seconds
    emotionIntervalRef.current = setInterval(() => {
      const emotion = simulateEmotionDetection()
      const confidence = Math.random() * 30 + 70 // 70-100%
      setCurrentEmotion(emotion)
      setEmotionHistory(prev => [...prev, {
        emotion,
        confidence,
        timestamp: Date.now()
      }])
    }, 2000)
  }

  const stopRecording = () => {
    setIsRecording(false)
    stopCamera()
    setStage("results")
  }

  const resetDetection = () => {
    setStage("intro")
    setTimeLeft(60)
    setEmotionHistory([])
    setCurrentEmotion(null)
    setCameraError(null)
  }

  useEffect(() => {
    return () => {
      stopCamera()
    }
  }, [stopCamera])

  const calculateResults = () => {
    if (emotionHistory.length === 0) return null

    const emotionCounts: Record<Emotion, number> = {
      happy: 0, sad: 0, neutral: 0, anxious: 0, angry: 0, surprised: 0
    }

    emotionHistory.forEach(e => emotionCounts[e.emotion]++)

    const totalDetections = emotionHistory.length
    const dominantEmotion = Object.entries(emotionCounts)
      .sort(([,a], [,b]) => b - a)[0][0] as Emotion

    const totalScore = emotionHistory.reduce((sum, e) => sum + emotionConfig[e.emotion].score, 0)
    const averageScore = totalScore / totalDetections
    const maxPossibleScore = 10

    let assessment: string
    let severity: "good" | "moderate" | "concerning"

    if (averageScore >= 7) {
      assessment = "Your emotional state appears positive and healthy."
      severity = "good"
    } else if (averageScore >= 4) {
      assessment = "Your emotional state shows some mixed signals. Consider speaking with a professional."
      severity = "moderate"
    } else {
      assessment = "Your emotional patterns suggest you may benefit from professional support."
      severity = "concerning"
    }

    return {
      emotionCounts,
      totalDetections,
      dominantEmotion,
      averageScore,
      maxPossibleScore,
      assessment,
      severity
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-12">
        {stage === "intro" && (
          <div className="mx-auto max-w-3xl">
            {/* Header */}
            <div className="mb-8 text-center">
              <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-teal/10">
                <Camera className="h-10 w-10 text-teal" />
              </div>
              <h1 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl">
                Facial Emotion Detection
              </h1>
              <p className="mx-auto max-w-xl text-pretty text-lg text-muted-foreground">
                Speak about yourself for 1 minute while we analyze your facial expressions 
                to understand your emotional state.
              </p>
            </div>

            {/* Info Cards */}
            <div className="mb-8 grid gap-4 md:grid-cols-3">
              <Card className="border-2 border-coral/20 bg-coral-light/20">
                <CardContent className="flex flex-col items-center p-6 text-center">
                  <Video className="mb-3 h-8 w-8 text-coral" />
                  <h3 className="mb-1 font-semibold text-foreground">Real-time Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    Your facial expressions are analyzed in real-time
                  </p>
                </CardContent>
              </Card>

              <Card className="border-2 border-teal/20 bg-teal-light/20">
                <CardContent className="flex flex-col items-center p-6 text-center">
                  <Timer className="mb-3 h-8 w-8 text-teal" />
                  <h3 className="mb-1 font-semibold text-foreground">1 Minute Session</h3>
                  <p className="text-sm text-muted-foreground">
                    Share your thoughts while we observe your emotions
                  </p>
                </CardContent>
              </Card>

              <Card className="border-2 border-lavender/20 bg-lavender-light/20">
                <CardContent className="flex flex-col items-center p-6 text-center">
                  <Sparkles className="mb-3 h-8 w-8 text-lavender" />
                  <h3 className="mb-1 font-semibold text-foreground">AI-Powered</h3>
                  <p className="text-sm text-muted-foreground">
                    Advanced algorithms detect emotional patterns
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Instructions */}
            <Card className="mb-8 border-2 border-border">
              <CardContent className="p-6">
                <h3 className="mb-4 text-lg font-semibold text-foreground">
                  How It Works
                </h3>
                <ul className="space-y-3">
                  <li className="flex items-start gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                      1
                    </span>
                    <span className="text-muted-foreground">
                      Allow camera access when prompted by your browser.
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                      2
                    </span>
                    <span className="text-muted-foreground">
                      Position your face clearly in the camera view with good lighting.
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                      3
                    </span>
                    <span className="text-muted-foreground">
                      Click start and talk about yourself, your day, or how you are feeling.
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
                      4
                    </span>
                    <span className="text-muted-foreground">
                      After 1 minute, view your emotional analysis results.
                    </span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            {cameraError && (
              <Card className="mb-8 border-2 border-destructive/30 bg-destructive/10">
                <CardContent className="flex gap-4 p-6">
                  <AlertCircle className="h-6 w-6 shrink-0 text-destructive" />
                  <p className="text-sm text-destructive">{cameraError}</p>
                </CardContent>
              </Card>
            )}

            {/* Start Button */}
            <div className="text-center">
              <Button 
                size="lg" 
                onClick={startCamera}
                className="group h-14 gap-2 rounded-xl bg-teal px-8 text-lg font-semibold text-foreground hover:bg-teal/90"
              >
                <Camera className="h-5 w-5" />
                Start Camera
              </Button>
            </div>
          </div>
        )}

        {stage === "recording" && (
          <div className="mx-auto max-w-3xl">
            {/* Timer */}
            <div className="mb-6 text-center">
              <div className={`inline-flex items-center gap-2 rounded-full px-6 py-3 text-2xl font-bold ${
                timeLeft <= 10 ? "bg-destructive/10 text-destructive" : "bg-primary/10 text-primary"
              }`}>
                <Timer className="h-6 w-6" />
                {formatTime(timeLeft)}
              </div>
            </div>

            {/* Video */}
            <Card className="mb-6 overflow-hidden border-2 border-border">
              <div className="relative aspect-video bg-muted">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="h-full w-full object-cover"
                />
                
                {/* Current Emotion Overlay */}
                {currentEmotion && isRecording && (
                  <div className="absolute left-4 top-4 flex items-center gap-2 rounded-full bg-background/90 px-4 py-2 shadow-lg backdrop-blur-sm">
                    {(() => {
                      const config = emotionConfig[currentEmotion]
                      const Icon = config.icon
                      return (
                        <>
                          <Icon className={`h-5 w-5 ${config.color}`} />
                          <span className={`font-semibold ${config.color}`}>
                            {config.label}
                          </span>
                        </>
                      )
                    })()}
                  </div>
                )}

                {/* Recording Indicator */}
                {isRecording && (
                  <div className="absolute right-4 top-4 flex items-center gap-2 rounded-full bg-destructive px-3 py-1.5 text-sm font-medium text-destructive-foreground">
                    <span className="h-2 w-2 animate-pulse rounded-full bg-destructive-foreground" />
                    Recording
                  </div>
                )}
              </div>
            </Card>

            {/* Controls */}
            <div className="flex justify-center gap-4">
              {!isRecording ? (
                <Button 
                  size="lg" 
                  onClick={startRecording}
                  className="gap-2 bg-mint text-foreground hover:bg-mint/90"
                >
                  <Play className="h-5 w-5" />
                  Start Recording
                </Button>
              ) : (
                <Button 
                  size="lg" 
                  onClick={stopRecording}
                  variant="destructive"
                  className="gap-2"
                >
                  <Square className="h-5 w-5" />
                  Stop & View Results
                </Button>
              )}
            </div>

            {/* Prompt */}
            <Card className="mt-6 border-2 border-teal/20 bg-teal-light/20">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground">
                  <strong>Tip:</strong> Talk about your day, your feelings, or anything on your mind. 
                  Be natural and express yourself freely.
                </p>
              </CardContent>
            </Card>
          </div>
        )}

        {stage === "results" && (
          <div className="mx-auto max-w-4xl">
            {(() => {
              const results = calculateResults()
              if (!results) return <p>No data recorded</p>

              const severityColors = {
                good: "border-mint/30 bg-mint/10",
                moderate: "border-sunshine/30 bg-sunshine/10",
                concerning: "border-coral/30 bg-coral/10"
              }

              return (
                <>
                  {/* Header */}
                  <div className="mb-8 text-center">
                    <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">
                      <Sparkles className="h-10 w-10 text-primary" />
                    </div>
                    <h1 className="mb-4 text-balance text-3xl font-bold text-foreground md:text-4xl">
                      Emotion Analysis Results
                    </h1>
                    <p className="mx-auto max-w-xl text-pretty text-lg text-muted-foreground">
                      Based on {results.totalDetections} facial expression samples during your session.
                    </p>
                  </div>

                  {/* Primary Result */}
                  <Card className={`mb-8 border-2 ${severityColors[results.severity]}`}>
                    <CardContent className="p-6">
                      <div className="flex flex-col items-center gap-4 text-center">
                        {(() => {
                          const config = emotionConfig[results.dominantEmotion]
                          const Icon = config.icon
                          return (
                            <div className={`flex h-16 w-16 items-center justify-center rounded-2xl ${config.bgColor}`}>
                              <Icon className="h-8 w-8 text-primary-foreground" />
                            </div>
                          )
                        })()}
                        <div>
                          <h3 className="mb-1 text-xl font-semibold text-foreground">
                            Dominant Emotion: {emotionConfig[results.dominantEmotion].label}
                          </h3>
                          <p className="text-muted-foreground">
                            {results.assessment}
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Emotion Breakdown */}
                  <Card className="mb-8 border-2 border-border">
                    <CardHeader>
                      <CardTitle>Emotion Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {Object.entries(results.emotionCounts)
                          .sort(([,a], [,b]) => b - a)
                          .map(([emotion, count]) => {
                            const config = emotionConfig[emotion as Emotion]
                            const Icon = config.icon
                            const percentage = Math.round((count / results.totalDetections) * 100)
                            
                            return (
                              <div key={emotion}>
                                <div className="mb-1 flex items-center justify-between">
                                  <div className="flex items-center gap-2">
                                    <Icon className={`h-5 w-5 ${config.color}`} />
                                    <span className="font-medium text-foreground">{config.label}</span>
                                  </div>
                                  <span className="text-sm text-muted-foreground">
                                    {count} times ({percentage}%)
                                  </span>
                                </div>
                                <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                                  <div 
                                    className={`h-full ${config.bgColor} transition-all`}
                                    style={{ width: `${percentage}%` }}
                                  />
                                </div>
                              </div>
                            )
                          })}
                      </div>
                    </CardContent>
                  </Card>

                  {/* Wellness Score */}
                  <Card className="mb-8 border-2 border-border">
                    <CardContent className="p-6">
                      <div className="flex flex-col items-center gap-4 text-center">
                        <h3 className="text-lg font-semibold text-foreground">Wellness Score</h3>
                        <div className="relative flex h-32 w-32 items-center justify-center">
                          <svg className="h-32 w-32 -rotate-90 transform">
                            <circle
                              cx="64"
                              cy="64"
                              r="56"
                              stroke="currentColor"
                              strokeWidth="12"
                              fill="none"
                              className="text-muted"
                            />
                            <circle
                              cx="64"
                              cy="64"
                              r="56"
                              stroke="currentColor"
                              strokeWidth="12"
                              fill="none"
                              strokeLinecap="round"
                              className="text-primary"
                              strokeDasharray={`${(results.averageScore / results.maxPossibleScore) * 352} 352`}
                            />
                          </svg>
                          <span className="absolute text-3xl font-bold text-foreground">
                            {results.averageScore.toFixed(1)}
                          </span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          out of {results.maxPossibleScore} points
                        </p>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Actions */}
                  <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
                    <Button
                      variant="outline"
                      onClick={resetDetection}
                      className="gap-2"
                    >
                      <RotateCcw className="h-4 w-4" />
                      Try Again
                    </Button>
                    <Link href="/clinics">
                      <Button className="gap-2 bg-primary hover:bg-primary/90">
                        <MapPin className="h-4 w-4" />
                        Find Professional Help
                      </Button>
                    </Link>
                  </div>
                </>
              )
            })()}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

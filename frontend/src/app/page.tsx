"use client";

import { useState } from 'react';
import AudioRecorder from '@/components/AudioRecorder';
import TranscriptionView from '@/components/TranscriptionView';

export default function Home() {
  const [segments, setSegments] = useState([]);

  const handleTranscription = (transcription) => {
    setSegments(prev => [...prev, ...transcription.segments]);
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">MedAssistent</h1>
      <div className="grid gap-8">
        <AudioRecorder onTranscriptionReceived={handleTranscription} />
        <TranscriptionView segments={segments} />
      </div>
    </main>
  );
}
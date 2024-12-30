"use client";

import { useState } from 'react';
import AudioRecorder from '@/components/AudioRecorder';
import TranscriptionView from '@/components/TranscriptionView';
import GPTAnalysis from '@/components/analysis/GPTAnalysis';
import PatientList from '@/components/patients/PatientList';

export default function DashboardPage() {
  const [transcription, setTranscription] = useState('');
  const [segments, setSegments] = useState([]);

  const handleTranscription = (data) => {
    setSegments(prev => [...prev, ...data.segments]);
    setTranscription(prev => prev + ' ' + data.full_text);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-bold mb-4">Patients</h2>
          <PatientList />
        </div>
        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-bold mb-4">Transcription</h2>
            <AudioRecorder onTranscriptionReceived={handleTranscription} />
            <TranscriptionView segments={segments} />
          </div>
          <div>
            <h2 className="text-xl font-bold mb-4">Analysis</h2>
            <GPTAnalysis transcription={transcription} />
          </div>
        </div>
      </div>
    </div>
  );
}
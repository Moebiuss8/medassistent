"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import MedicalRecord from '@/components/MedicalRecord';

export default function PatientRecordsPage() {
  const params = useParams();
  const [transcript, setTranscript] = useState('');
  const [record, setRecord] = useState({
    patientId: params.id as string,
    visitDate: new Date().toISOString(),
    chiefComplaint: '',
    history: '',
    exam: '',
    diagnosis: '',
    plan: ''
  });

  return (
    <div className="container mx-auto py-8 h-screen">
      <MedicalRecord 
        {...record}
        transcription={transcript}
        onTranscriptUpdate={setTranscript}
      />
    </div>
  );
}
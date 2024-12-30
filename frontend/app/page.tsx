import React from 'react';
import TranscriptionService from '@/components/transcription/TranscriptionService';
import ClinicalNoteGenerator from '@/components/notes/ClinicalNoteGenerator';

export default function Home() {
  return (
    <div className='container mx-auto py-6'>
      <h1 className='text-3xl font-bold mb-6'>MedAssistent</h1>
      <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
        <TranscriptionService />
        <ClinicalNoteGenerator />
      </div>
    </div>
  );
}
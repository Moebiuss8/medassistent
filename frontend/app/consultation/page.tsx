import React from 'react';
import TranscriptionService from '@/components/transcription/TranscriptionService';
import ClinicalNoteGenerator from '@/components/notes/ClinicalNoteGenerator';

const ConsultationPage = () => {
  return (
    <div className='container mx-auto py-6'>
      <h1 className='text-3xl font-bold mb-6'>Patient Consultation</h1>
      
      <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
        <TranscriptionService />
        <ClinicalNoteGenerator />
      </div>
    </div>
  );
};

export default ConsultationPage;
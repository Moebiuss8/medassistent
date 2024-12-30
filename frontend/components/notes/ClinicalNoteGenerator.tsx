import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface SOAPNote {
  subjective: string;
  objective: string;
  assessment: string;
  plan: string;
}

const ClinicalNoteGenerator = () => {
  const [note, setNote] = useState<SOAPNote>({
    subjective: '',
    objective: '',
    assessment: '',
    plan: ''
  });

  const handleSave = async () => {
    // TODO: Implement API call to save note
    console.log('Saving note:', note);
  };

  return (
    <Card className='p-6'>
      <div className='flex flex-col space-y-4'>
        <h2 className='text-2xl font-bold'>SOAP Note Generator</h2>
        
        <div className='space-y-4'>
          <div>
            <label className='block text-sm font-medium mb-1'>Subjective</label>
            <Textarea
              value={note.subjective}
              onChange={(e) => setNote({...note, subjective: e.target.value})}
              placeholder='Patient complaints and history...'
              className='min-h-[100px]'
            />
          </div>
          
          <div>
            <label className='block text-sm font-medium mb-1'>Objective</label>
            <Textarea
              value={note.objective}
              onChange={(e) => setNote({...note, objective: e.target.value})}
              placeholder='Physical examination findings...'
              className='min-h-[100px]'
            />
          </div>
          
          <div>
            <label className='block text-sm font-medium mb-1'>Assessment</label>
            <Textarea
              value={note.assessment}
              onChange={(e) => setNote({...note, assessment: e.target.value})}
              placeholder='Diagnosis and clinical impressions...'
              className='min-h-[100px]'
            />
          </div>
          
          <div>
            <label className='block text-sm font-medium mb-1'>Plan</label>
            <Textarea
              value={note.plan}
              onChange={(e) => setNote({...note, plan: e.target.value})}
              placeholder='Treatment plan and follow-up...'
              className='min-h-[100px]'
            />
          </div>
        </div>

        <div className='flex justify-end'>
          <Button onClick={handleSave}>Save Note</Button>
        </div>
      </div>
    </Card>
  );
};

export default ClinicalNoteGenerator;
import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mic, MicOff } from 'lucide-react';

const TranscriptionService = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');

  useEffect(() => {
    let recognition: any;
    
    if ('webkitSpeechRecognition' in window) {
      recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      
      recognition.onresult = (event: any) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          setTranscript(prev => prev + ' ' + finalTranscript);
        }
      };
    }

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };

  return (
    <Card className='p-6'>
      <div className='flex flex-col space-y-4'>
        <div className='flex items-center justify-between'>
          <h2 className='text-2xl font-bold'>Voice Transcription</h2>
          <Button
            onClick={toggleRecording}
            variant={isRecording ? 'destructive' : 'default'}
            className='w-12 h-12 rounded-full'
          >
            {isRecording ? <MicOff /> : <Mic />}
          </Button>
        </div>
        <div className='min-h-[200px] p-4 bg-gray-50 rounded-lg'>
          <p className='whitespace-pre-wrap'>{transcript}</p>
        </div>
      </div>
    </Card>
  );
};

export default TranscriptionService;
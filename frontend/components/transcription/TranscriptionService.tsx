import React, { useState, useEffect, useRef } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import type { TranscriptionResult } from '@/lib/types';

const TranscriptionService = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      setError('Speech recognition is not supported in this browser');
      return;
    }

    recognitionRef.current = new window.webkitSpeechRecognition();
    const recognition = recognitionRef.current;

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsProcessing(false);
      setError(null);
    };

    recognition.onerror = (event: any) => {
      setError(`Error: ${event.error}`);
      setIsRecording(false);
      setIsProcessing(false);
    };

    recognition.onend = () => {
      if (isRecording) {
        recognition.start();
      }
    };

    recognition.onresult = (event: any) => {
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          finalTranscript += result[0].transcript;
        } else {
          interimTranscript += result[0].transcript;
        }
      }

      if (finalTranscript) {
        setTranscript(prev => {
          const newTranscript = prev + ' ' + finalTranscript;
          analyzeTranscript(newTranscript);
          return newTranscript;
        });
      }
    };

    return () => {
      recognition.stop();
    };
  }, [isRecording]);

  const toggleRecording = async () => {
    try {
      if (!isRecording) {
        setIsProcessing(true);
        await recognitionRef.current?.start();
      } else {
        recognitionRef.current?.stop();
      }
      setIsRecording(!isRecording);
    } catch (err) {
      setError('Failed to toggle recording');
      setIsProcessing(false);
    }
  };

  const analyzeTranscript = async (text: string) => {
    try {
      // TODO: Implement medical term extraction and analysis
      const response = await fetch('/api/analyze-transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!response.ok) throw new Error('Analysis failed');
      
      const analysis = await response.json();
      // Handle analysis results
    } catch (err) {
      console.error('Analysis error:', err);
    }
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
            disabled={isProcessing || !!error}
          >
            {isProcessing ? (
              <Loader2 className='h-6 w-6 animate-spin' />
            ) : isRecording ? (
              <MicOff className='h-6 w-6' />
            ) : (
              <Mic className='h-6 w-6' />
            )}
          </Button>
        </div>

        {error && (
          <Alert variant='destructive'>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className='min-h-[200px] p-4 bg-gray-50 rounded-lg'>
          <p className='whitespace-pre-wrap'>{transcript}</p>
        </div>

        <div className='flex justify-end space-x-2'>
          <Button
            variant='outline'
            onClick={() => setTranscript('')}
            disabled={!transcript}
          >
            Clear
          </Button>
          <Button
            onClick={() => {
              // TODO: Implement save functionality
              console.log('Saving transcript:', transcript);
            }}
            disabled={!transcript}
          >
            Save to Notes
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default TranscriptionService;
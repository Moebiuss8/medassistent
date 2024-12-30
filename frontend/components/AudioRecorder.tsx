import React, { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, Square } from 'lucide-react';
import { TranscriptionWebSocket } from '@/lib/websocket';

export default function AudioRecorder({ onTranscriptUpdate }: { onTranscriptUpdate: (text: string) => void }) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const wsRef = useRef<TranscriptionWebSocket | null>(null);

  useEffect(() => {
    return () => {
      wsRef.current?.close();
    };
  }, []);

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      wsRef.current = new TranscriptionWebSocket(onTranscriptUpdate);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          wsRef.current?.sendAudioChunk(event.data);
        }
      };

      mediaRecorder.start(1000); // Send chunks every second
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    wsRef.current?.close();
    setIsRecording(false);
  }

  return (
    <div className="flex items-center gap-4">
      {!isRecording ? (
        <Button onClick={startRecording} variant="outline" size="icon">
          <Mic className="h-4 w-4" />
        </Button>
      ) : (
        <Button onClick={stopRecording} variant="destructive" size="icon">
          <Square className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
}
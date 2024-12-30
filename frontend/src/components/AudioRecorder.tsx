import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, Square } from 'lucide-react';

export default function AudioRecorder({ onTranscriptionReceived }) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const wsRef = useRef(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;

    const ws = new WebSocket('ws://localhost:8000/transcription/ws');
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const transcription = JSON.parse(event.data);
      onTranscriptionReceived(transcription);
    };

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
        ws.send(event.data);
      }
    };

    mediaRecorder.start(1000);
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    wsRef.current?.close();
    setIsRecording(false);
  };

  return (
    <div className="flex items-center gap-4">
      <Button
        onClick={isRecording ? stopRecording : startRecording}
        variant={isRecording ? "destructive" : "default"}
      >
        {isRecording ? <Square className="w-4 h-4 mr-2" /> : <Mic className="w-4 h-4 mr-2" />}
        {isRecording ? "Stop Recording" : "Start Recording"}
      </Button>
    </div>
  );
}
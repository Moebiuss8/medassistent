export class TranscriptionWebSocket {
  private ws: WebSocket;
  private onTranscriptUpdate: (transcript: string) => void;

  constructor(onTranscriptUpdate: (transcript: string) => void) {
    this.onTranscriptUpdate = onTranscriptUpdate;
    this.ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/transcribe');
    this.setupWebSocket();
  }

  private setupWebSocket() {
    this.ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'transcript') {
        this.onTranscriptUpdate(data.text);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  sendAudioChunk(audioChunk: Blob) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(audioChunk);
    }
  }

  close() {
    this.ws.close();
  }
}
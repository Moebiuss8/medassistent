import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface AnalysisProps {
  transcription: string;
}

export default function GPTAnalysis({ transcription }: AnalysisProps) {
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!transcription) return;

    setLoading(true);
    fetch('/api/analysis/analyze-transcription', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ transcription })
    })
      .then(res => res.json())
      .then(data => {
        setAnalysis(data.soap_note);
        setLoading(false);
      });
  }, [transcription]);

  if (loading) return <div>Analyzing transcription...</div>;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="prose max-w-none">
          {analysis.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
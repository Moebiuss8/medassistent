import { API_URL } from '../config';

export async function analyzeTranscript(text: string) {
  const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });

  if (!response.ok) throw new Error('Analysis failed');
  return await response.json();
}

export async function analyzeTranscript(text: string) {
  try {
    const response = await fetch('/api/analyze-transcript', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error('Analysis failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Analysis error:', error);
    throw error;
  }
}

export async function saveTranscript(text: string) {
  try {
    const response = await fetch('/api/transcripts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error('Failed to save transcript');
    }

    return await response.json();
  } catch (error) {
    console.error('Save error:', error);
    throw error;
  }
}

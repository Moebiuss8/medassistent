export interface TranscriptionResult {
  text: string;
  confidence: number;
  isFinal: boolean;
}

export interface AudioAnalysis {
  symptoms: string[];
  diagnoses: string[];
  medications: string[];
  procedures: string[];
}

export interface SOAPNote {
  subjective: string;
  objective: string;
  assessment: string;
  plan: string;
}

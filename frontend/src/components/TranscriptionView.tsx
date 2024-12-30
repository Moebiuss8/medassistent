import { useEffect, useRef } from 'react';

interface TranscriptionSegment {
  text: string;
  start: number;
  end: number;
  confidence: number;
}

interface TranscriptionViewProps {
  segments: TranscriptionSegment[];
}

export default function TranscriptionView({ segments }: TranscriptionViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current && segments.length > 0) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [segments]);

  return (
    <div
      ref={containerRef}
      className="h-96 overflow-y-auto p-4 bg-white rounded-lg shadow"
    >
      {segments.map((segment, index) => (
        <div
          key={index}
          className={`mb-2 p-2 rounded ${segment.confidence > 0.8 ? 'bg-gray-50' : 'bg-yellow-50'}`}
        >
          <p className="text-gray-900">{segment.text}</p>
          <p className="text-xs text-gray-500">
            {Math.round(segment.confidence * 100)}% confidence
          </p>
        </div>
      ))}
    </div>
  );
}
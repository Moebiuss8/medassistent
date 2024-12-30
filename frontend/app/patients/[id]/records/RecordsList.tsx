"use client";

import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { getPatientRecords } from '@/lib/api/records';

export default function RecordsList({ patientId }: { patientId: string }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadRecords() {
      try {
        const data = await getPatientRecords(patientId);
        setRecords(data);
        setError('');
      } catch (err) {
        setError('Failed to load records');
      } finally {
        setLoading(false);
      }
    }
    loadRecords();
  }, [patientId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="space-y-4">
      {records.map((record: any) => (
        <Card key={record.id}>
          <CardHeader>
            <CardTitle>{new Date(record.visit_date).toLocaleDateString()}</CardTitle>
          </CardHeader>
          <CardContent>
            <p><strong>Chief Complaint:</strong> {record.chief_complaint}</p>
            <p><strong>Diagnosis:</strong> {record.diagnosis}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
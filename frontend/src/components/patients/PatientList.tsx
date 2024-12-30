import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
}

export default function PatientList() {
  const [patients, setPatients] = useState<Patient[]>([]);

  useEffect(() => {
    fetch('/api/patients', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(res => res.json())
      .then(data => setPatients(data));
  }, []);

  return (
    <div className="space-y-4">
      {patients.map(patient => (
        <Card key={patient.id}>
          <CardHeader>
            <CardTitle>{patient.first_name} {patient.last_name}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Date of Birth: {new Date(patient.date_of_birth).toLocaleDateString()}</p>
            <Button className="mt-2">View Records</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
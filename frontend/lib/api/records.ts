import { useAuth } from '../auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getPatientRecords(patientId: string) {
  const { token } = useAuth.getState();
  const response = await fetch(`${API_URL}/api/v1/patient/${patientId}/records`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!response.ok) throw new Error('Failed to fetch records');
  return response.json();
}

export async function createRecord(patientId: string, recordData: any) {
  const { token } = useAuth.getState();
  const response = await fetch(`${API_URL}/api/v1/patient/${patientId}/records`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(recordData),
  });
  if (!response.ok) throw new Error('Failed to create record');
  return response.json();
}

export async function updateRecord(recordId: string, recordData: any) {
  const { token } = useAuth.getState();
  const response = await fetch(`${API_URL}/api/v1/records/${recordId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(recordData),
  });
  if (!response.ok) throw new Error('Failed to update record');
  return response.json();
}
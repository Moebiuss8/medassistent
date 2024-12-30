const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchPatients() {
  const response = await fetch(`${API_BASE_URL}/api/v1/patients`);
  if (!response.ok) throw new Error('Failed to fetch patients');
  return response.json();
}

export async function createPatient(patientData: any) {
  const response = await fetch(`${API_BASE_URL}/api/v1/patients`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(patientData),
  });
  if (!response.ok) throw new Error('Failed to create patient');
  return response.json();
}

export async function updatePatient(id: number, patientData: any) {
  const response = await fetch(`${API_BASE_URL}/api/v1/patients/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(patientData),
  });
  if (!response.ok) throw new Error('Failed to update patient');
  return response.json();
}

export async function deletePatient(id: number) {
  const response = await fetch(`${API_BASE_URL}/api/v1/patients/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete patient');
  return response.json();
}
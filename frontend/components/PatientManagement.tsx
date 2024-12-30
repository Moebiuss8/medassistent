import React from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Plus } from 'lucide-react';

interface Patient {
  id: string;
  name: string;
  dateOfBirth: string;
  lastVisit: string;
  status: string;
}

const mockPatients: Patient[] = [
  {
    id: "1",
    name: "John Doe",
    dateOfBirth: "1985-03-15",
    lastVisit: "2024-12-15",
    status: "Active"
  },
  {
    id: "2",
    name: "Jane Smith",
    dateOfBirth: "1990-07-22",
    lastVisit: "2024-12-20",
    status: "Scheduled"
  }
];

export default function PatientManagement() {
  return (
    <div className="p-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Patient Management</CardTitle>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" /> Add Patient
          </Button>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Date of Birth</TableHead>
                <TableHead>Last Visit</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockPatients.map((patient) => (
                <TableRow key={patient.id}>
                  <TableCell>{patient.name}</TableCell>
                  <TableCell>{patient.dateOfBirth}</TableCell>
                  <TableCell>{patient.lastVisit}</TableCell>
                  <TableCell>{patient.status}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">View</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
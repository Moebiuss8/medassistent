import React from 'react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import AudioRecorder from './AudioRecorder';

interface MedicalRecordProps {
  patientId: string;
  visitDate: string;
  chiefComplaint?: string;
  history?: string;
  exam?: string;
  diagnosis?: string;
  plan?: string;
  transcription?: string;
  onTranscriptUpdate: (text: string) => void;
}

export default function MedicalRecord({
  patientId,
  visitDate,
  chiefComplaint = '',
  history = '',
  exam = '',
  diagnosis = '',
  plan = '',
  transcription = '',
  onTranscriptUpdate
}: MedicalRecordProps) {
  return (
    <div className="h-full flex flex-col gap-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">Visit Record</h3>
          <p className="text-sm text-muted-foreground">{new Date(visitDate).toLocaleDateString()}</p>
        </div>
        <div className="flex items-center gap-2">
          <AudioRecorder onTranscriptUpdate={onTranscriptUpdate} />
          <Button>Save Record</Button>
        </div>
      </div>

      <Tabs defaultValue="soap" className="flex-1">
        <TabsList>
          <TabsTrigger value="soap">SOAP Note</TabsTrigger>
          <TabsTrigger value="transcript">Transcription</TabsTrigger>
        </TabsList>

        <TabsContent value="soap" className="h-[calc(100%-2rem)]">
          <ScrollArea className="h-full rounded-md border p-4">
            <div className="space-y-4">
              <section>
                <h4 className="font-semibold mb-2">Subjective</h4>
                <div className="space-y-2">
                  <div>
                    <label className="text-sm font-medium">Chief Complaint</label>
                    <textarea 
                      className="w-full h-20 p-2 border rounded-md"
                      value={chiefComplaint}
                      readOnly
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">History</label>
                    <textarea 
                      className="w-full h-32 p-2 border rounded-md"
                      value={history}
                      readOnly
                    />
                  </div>
                </div>
              </section>

              <section>
                <h4 className="font-semibold mb-2">Objective</h4>
                <textarea 
                  className="w-full h-32 p-2 border rounded-md"
                  value={exam}
                  readOnly
                />
              </section>

              <section>
                <h4 className="font-semibold mb-2">Assessment</h4>
                <textarea 
                  className="w-full h-32 p-2 border rounded-md"
                  value={diagnosis}
                  readOnly
                />
              </section>

              <section>
                <h4 className="font-semibold mb-2">Plan</h4>
                <textarea 
                  className="w-full h-32 p-2 border rounded-md"
                  value={plan}
                  readOnly
                />
              </section>
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="transcript" className="h-[calc(100%-2rem)]">
          <ScrollArea className="h-full rounded-md border p-4">
            <div className="space-y-4">
              <textarea
                className="w-full h-full min-h-[400px] p-2 border rounded-md"
                value={transcription}
                readOnly
              />
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </div>
  );
}
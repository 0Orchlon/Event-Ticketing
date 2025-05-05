// src/app/admin/events/[id]/page.tsx
"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function EventDetails() {
  const params = useParams();
  const id = params?.id as string;

  const [event, setEvent] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    
    fetch("http://localhost:8000/eventapi/", {
      method: "POST",
      body: JSON.stringify({ action: "event_detail", eventid: id }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setEvent(data);
      })
      .catch((err) => {
        setError("Failed to fetch event details.");
        console.error("Error:", err);
      });
  }, [id]);

  if (error) return <div>{error}</div>;
  if (!event) return <div>Loading...</div>;

  return (
    <>
    <div>
        <a href="/admin/events">back</a>
    </div>
    <div className="p-6 max-w-2xl space-y-4">
      <h1 className="text-2xl font-bold">{event.name}</h1>
      <div>

      <p>Description:</p>
      <p>{event.description}</p>
      </div>
      <p>
        <strong>Start:</strong> {new Date(event.start_time).toLocaleString()}
      </p>
      <p>
        <strong>End:</strong> {new Date(event.end_time).toLocaleString()}
      </p>
      <p>
        <strong>Venue:</strong> {event.venue}
      </p>
      <div>
        <strong>Images:</strong>
        <div className="flex gap-2 mt-2 flex-wrap">
        {event.images?.map((img: string, idx: number) => (
      <img
        key={idx}
        src={`http://localhost:8000${img}`}
        alt={`Event Image ${idx + 1}`}
        className="w-32 h-32 object-cover rounded"
            />
          ))}
        </div>
      </div>
    </div>
    </>

  );
}

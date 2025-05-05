// src/app/admin/events/create/page.tsx
"use client";
import { useState } from "react";
import { createEvent } from "@/lib/api";

export default function CreateEvent() {
  const [form, setForm] = useState({
    ename: "",
    edesc: "",
    edateb: "",
    edatee: "",
    vid: "1",
  });
  const [images, setImages] = useState<File[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("action", "create_event");

    // Add form data to the formData object
    Object.entries(form).forEach(([key, value]) => formData.append(key, value));
    
    // Add files to the formData object
    images.forEach((file) => formData.append("images", file));

    try {
      // Send the form data to the backend
      await createEvent(formData);
      alert("Event created successfully!");
    } catch {
      alert("Failed to create event");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 space-y-4 max-w-xl">
      <h1 className="text-2xl font-bold">Create Event</h1>
      <input
        type="text"
        placeholder="Name"
        className="w-full p-2 border rounded"
        value={form.ename}
        onChange={(e) => setForm({ ...form, ename: e.target.value })}
        required
      />
      <textarea
        placeholder="Description"
        className="w-full p-2 border rounded"
        value={form.edesc}
        onChange={(e) => setForm({ ...form, edesc: e.target.value })}
        required
      />
      <input
        type="datetime-local"
        className="w-full p-2 border rounded"
        value={form.edateb}
        onChange={(e) => setForm({ ...form, edateb: e.target.value })}
        required
      />
      <input
        type="datetime-local"
        className="w-full p-2 border rounded"
        value={form.edatee}
        onChange={(e) => setForm({ ...form, edatee: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Venue ID"
        className="w-full p-2 border rounded"
        value={form.vid}
        onChange={(e) => setForm({ ...form, vid: e.target.value })}
        required
      />
      <input
        type="file"
        accept="image/*"
        multiple
        className="w-full"
        onChange={(e) => setImages(Array.from(e.target.files || []))}
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Create
      </button>
    </form>
  );
}

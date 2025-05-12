"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

function formatDatetimeLocal(datetime: string) {
  const date = new Date(datetime);
  const offset = date.getTimezoneOffset();
  const localDate = new Date(date.getTime() - offset * 60000);
  return localDate.toISOString().slice(0, 16);
}

export default function EditEvent() {
  const params = useParams();
  const id = params?.id as string;

  const [form, setForm] = useState({
    ename: "",
    edesc: "",
    edateb: "",
    edatee: "",
  });
  const [images, setImages] = useState<File[]>([]);
  const [existingImages, setExistingImages] = useState<string[]>([]);

  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/eventapi/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "event_detail",
            eventid: id,
          }),
        });

        const text = await res.text();
        const data = JSON.parse(text);

        setForm({
          ename: data.name,
          edesc: data.description,
          edateb: formatDatetimeLocal(data.start_time),
          edatee: formatDatetimeLocal(data.end_time),
        });

        if (Array.isArray(data.images)) {
          setExistingImages(data.images);
        }
      } catch (error) {
        console.error("Failed to fetch event:", error);
      }
    };

    fetchData();
  }, [id]);

  const handleRemoveImage = (imgUrl: string) => {
    setExistingImages((imgs) => imgs.filter((img) => img !== imgUrl));
  };

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("action", "edit_event");
  formData.append("eventid", id);
  
  Object.entries(form).forEach(([key, value]) => {
    formData.append(key, value);
  });
  
  if (images.length > 0) {
    images.forEach((file) => formData.append("images", file));
  } else {
    formData.append("images", "");  // Optional: Send an empty string to signify no images
  }
  
  const res = await fetch("http://localhost:8000/eventapi/", {
    method: "POST",
    body: formData,
  });
  
  const result = await res.json();
  console.log(result);
  alert(result.code === 200 ? "Updated!" : "Update failed");};

  return (
    <>
    <div><a href="/admin/events">
      Back
    </a></div>
    <form onSubmit={handleSubmit} className="p-6 space-y-4 max-w-xl">
      <h1 className="text-2xl font-bold">Edit Event</h1>
      <div className="text-gray-500 mb-2">Editing Event ID: {id}</div>

      <input
        type="text"
        value={form.ename}
        onChange={(e) => setForm({ ...form, ename: e.target.value })}
        placeholder="Event Name"
        required
        className="w-full p-2 border rounded"
      />

      <textarea
        value={form.edesc}
        onChange={(e) => setForm({ ...form, edesc: e.target.value })}
        placeholder="Event Description"
        required
        className="w-full p-2 border rounded"
      />

      <input
        type="datetime-local"
        value={form.edateb}
        onChange={(e) => setForm({ ...form, edateb: e.target.value })}
        required
        className="w-full p-2 border rounded"
      />

      <input
        type="datetime-local"
        value={form.edatee}
        onChange={(e) => setForm({ ...form, edatee: e.target.value })}
        required
        className="w-full p-2 border rounded"
      />
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={(e) => setImages(Array.from(e.target.files || []))}
        className="w-full p-2 border rounded"
      />

      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Existing Images</h2>
        {existingImages.map((imgUrl) => (
          <div key={imgUrl} className="flex items-center space-x-2">
            <img
              src={`http://localhost:8000${imgUrl}`}
              alt="event"
              className="w-24 h-24 object-cover rounded border"
            />
            <button
              type="button"
              onClick={() => handleRemoveImage(imgUrl)}
              className="text-red-500 underline"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Update
      </button>
    </form>
    </>
  );
}

const API_URL = "http://localhost:8000/eventapi/"; // Adjust if needed

export async function fetchEvents() {
    const res = await fetch(API_URL, {
        method: "POST",
        body: JSON.stringify({ action: "list_events" }),
        headers: { "Content-Type": "application/json" },
    });
    return res.json();
}
export async function createEvent(formData: FormData) {
    const res = await fetch('http://localhost:8000/eventapi/', {
      method: 'POST',
      body: formData
    });
  
    if (!res.ok) throw new Error('Failed to create event');
    return res.json();
  }
  

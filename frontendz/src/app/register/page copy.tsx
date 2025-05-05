
// src/app/register/page.tsx
"use client";
import { useState } from "react";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    // Placeholder register logic
    alert(`Registered ${email}`);
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <input className="w-full p-2 border mb-2" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input className="w-full p-2 border mb-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="bg-green-600 text-white px-4 py-2 rounded" onClick={register}>Register</button>
    </div>
  );
}

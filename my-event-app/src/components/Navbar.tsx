export default function Navbar() {
  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800">
      <div className="text-pink-500 font-bold text-xl">DEV/<span className="text-white">AID</span></div>
      <ul className="flex gap-6 text-sm">
        {['Home', 'Albums', 'Бидний тухай', 'Зураг', 'Дэлгүүр', 'Холбоо барих'].map((item) => (
          <li key={item} className="hover:text-pink-400 cursor-pointer">{item}</li>
        ))}
      </ul>
    </nav>
  )
}
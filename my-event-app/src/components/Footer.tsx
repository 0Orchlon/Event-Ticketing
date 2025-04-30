import { FaPhone, FaEnvelope, FaMapMarkerAlt } from 'react-icons/fa'

export default function Footer() {
  return (
    <footer className="flex flex-col md:flex-row justify-between items-start gap-10 p-6 bg-gray-800 text-sm">
      <div>
        <h3 className="text-pink-400 font-bold mb-2">Download</h3>
        <div className="flex gap-3">
          <img src="/images/appstore.png" alt="App Store" className="h-10" />
          <img src="/images/googleplay.png" alt="Google Play" className="h-10" />
        </div>
      </div>
      <div>
        <h3 className="text-pink-400 font-bold mb-2">Contact info</h3>
        <p className="flex items-center gap-2"><FaMapMarkerAlt />Баянгол дүүргийн шинэ хороолол MBC МТС</p>
        <p className="flex items-center gap-2"><FaPhone />91081991</p>
        <p className="flex items-center gap-2"><FaEnvelope />swz200803@masd.edu.mn</p>
      </div>
    </footer>
  )
}
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Artists from './pages/Artists'
import Footer from './components/Footer'

function App() {
  return (
    <div className="bg-gray-900 text-white min-h-screen">
      <Navbar />
      <Hero />
      <Artists />
      <Footer />
    </div>
  )
}
export default App
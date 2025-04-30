import ArtistCard from '../components/ArtistCard'

const artists = [
  { name: 'ThunderZ', image: '/images/thunderz.jpg' },
  { name: 'Desant', image: '/images/desant.jpg' },
  { name: 'The c', image: '/images/thec.jpg' }
]

export default function Artists() {
  return (
    <div className="text-center py-12">
      <h2 className="text-pink-400 text-2xl font-semibold mb-8">Хуралд ирэх артистууд</h2>
      <div className="flex flex-wrap justify-center gap-10">
        {artists.map((artist) => (
          <ArtistCard key={artist.name} name={artist.name} image={artist.image} />
        ))}
      </div>
    </div>
  )
}
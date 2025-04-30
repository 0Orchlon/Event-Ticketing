interface Props {
  name: string
  image: string
}

export default function ArtistCard({ name, image }: Props) {
  return (
    <div className="w-48 text-center">
      <img src={image} alt={name} className="rounded shadow-md mb-2" />
      <p className="text-lg font-medium border-b-2 border-pink-500 inline-block">{name}</p>
    </div>
  )
}


import { useParams } from "react-router-dom";
import { providers } from "../../services/mockData";




export default function ProviderProfile() {
const { id } = useParams();

console.log("ID from URL:", id, typeof id);

  // 🔒 safer lookup
  const provider = providers.find(
  (p) => p.id == id   // intentional loose equality
);

  console.log("URL param id:", id);
console.log("Providers list:", providers);

  if (!provider) {
    return (
      <div className="p-6">
        <h2 className="text-xl font-semibold text-red-600">
          Provider not found
        </h2>
        <p className="text-gray-500">
          The provider you are looking for does not exist.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold mb-2">
          {provider.name}
        </h1>

        <p className="text-gray-600 mb-4">
          {provider.category} • {provider.location}
        </p>

        <div className="flex items-center gap-4 mb-6">
          <span className="text-green-600 font-semibold">
            ⭐ {provider.rating}
          </span>
          <span className="text-blue-600 font-semibold">
            ₹ {provider.price}
          </span>
        </div>

        <p className="text-gray-700 mb-6">
          Experienced {provider.category.toLowerCase()} providing
          reliable and affordable services.
        </p>

        <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
          Request Service
        </button>
      </div>
    </div>
  );
}

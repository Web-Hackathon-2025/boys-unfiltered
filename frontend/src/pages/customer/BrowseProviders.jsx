import { useState } from "react";
import ProviderCard from "../../components/booking/ProviderCard";
import { providers } from "../../services/mockData";

const categories = [
  "All",
  "Electrician",
  "Plumber",
  "AC Repair",
  "Carpenter",
  "Painter",
];

export default function BrowseProviders() {
  const [category, setCategory] = useState("All");

  const filteredProviders =
    category === "All"
      ? providers
      : providers.filter((p) => p.category === category);

  return (
    <div className="space-y-12">

      {/* HERO TITLE */}
      <section className="bg-slate-900 text-white py-14 rounded-xl">
        <div className="max-w-6xl mx-auto text-center px-6">
          <h1 className="text-3xl md:text-4xl font-bold mb-3">
            Find the Right Professional for Your Job
          </h1>
          <p className="text-slate-300 max-w-2xl mx-auto">
            Browse trusted local service providers, compare prices,
            and book instantly — just like Fiverr, but local.
          </p>
        </div>
      </section>

      {/* FILTER BAR */}
      <section className="bg-white shadow rounded-xl p-4">
        <div className="flex flex-wrap gap-3 justify-center">

          {/* Category Filter */}
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition
                ${
                  category === cat
                    ? "bg-blue-600 text-white"
                    : "bg-slate-100 hover:bg-slate-200"
                }`}
            >
              {cat}
            </button>
          ))}

          {/* Other Filters (UI only) */}
          <select className="border rounded-full px-4 py-2 text-sm">
            <option>Price: Low to High</option>
            <option>Price: High to Low</option>
          </select>

          <select className="border rounded-full px-4 py-2 text-sm">
            <option>Rating</option>
            <option>4.5 & above</option>
            <option>4.0 & above</option>
          </select>

          <select className="border rounded-full px-4 py-2 text-sm">
            <option>Location</option>
            <option>Delhi</option>
            <option>Noida</option>
            <option>Gurgaon</option>
          </select>
        </div>
      </section>

      {/* PROVIDER GRID */}
      <section>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProviders.map((provider) => (
            <ProviderCard
              key={provider.id}
              provider={provider}
            />
          ))}
        </div>

        {filteredProviders.length === 0 && (
          <p className="text-center text-gray-500 mt-8">
            No providers found for this category.
          </p>
        )}
      </section>
    </div>
  );
}

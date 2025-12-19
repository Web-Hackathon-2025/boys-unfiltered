import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* HERO SECTION */}
      <section className="bg-slate-900 text-white py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Find Trusted Local Services, Instantly
          </h1>
          <p className="text-lg text-slate-300 mb-8">
            Electricians, plumbers, carpenters and more — all in one place.
          </p>

          <div className="flex justify-center gap-4">
            <Link
              to="/login"
              className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded font-semibold"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="border border-white px-6 py-3 rounded font-semibold"
            >
              Become a Provider
            </Link>
          </div>
        </div>
      </section>

      {/* CATEGORIES */}
      <section className="py-16 bg-slate-100">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-2xl font-bold mb-8 text-center">
            Popular Services
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              "Electrician",
              "Plumber",
              "Carpenter",
              "AC Repair",
              "Painter",
              "Cleaner",
              "Mechanic",
              "Technician",
            ].map((service) => (
              <div
                key={service}
                className="bg-white p-6 rounded shadow text-center hover:shadow-lg transition"
              >
                <p className="font-semibold">{service}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold mb-10">
            How Karigar Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-semibold mb-2">1. Choose Service</h3>
              <p className="text-gray-600">
                Browse verified local professionals.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">2. Book Instantly</h3>
              <p className="text-gray-600">
                Send a request in seconds.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">3. Get It Done</h3>
              <p className="text-gray-600">
                Pay after service completion.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

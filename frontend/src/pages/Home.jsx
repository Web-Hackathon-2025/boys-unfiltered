import { Link } from "react-router-dom";
import Header from "../components/layout/Header";

import {
  FaBolt,
  FaWrench,
  FaTools,
  FaSnowflake,
  FaPaintRoller,
  FaBroom,
} from "react-icons/fa";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Header />
      {/* HERO */}
      <section className="bg-slate-900 text-white py-24">
        <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">

          {/* TEXT */}
          <div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
              Find Trusted Local Services, Instantly
            </h1>

            <p className="text-lg text-slate-300 mb-8">
              Karigar connects you with reliable electricians, plumbers,
              carpenters, AC technicians, and more — all in one place.
            </p>

            <div className="flex gap-4">
              <Link
                to="/login"
                className="bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-semibold transition"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="border border-white/70 hover:bg-white hover:text-slate-900 px-8 py-3 rounded-lg font-semibold transition"
              >
                Become a Provider
              </Link>
            </div>
          </div>

          {/* ILLUSTRATION (unDraw – open source) */}
          <img
            src="https://undraw.co/api/illustrations/maintenance_re_59vn.svg"
            alt="Service professionals illustration"
            className="w-full max-w-md mx-auto"
          />
        </div>
      </section>

      {/* SERVICES */}
      <section className="py-20 bg-slate-100">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-2xl font-bold mb-4 text-center">
            Popular Services
          </h2>
          <p className="text-gray-600 text-center mb-12">
            Skilled professionals for every household need
          </p>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            <ServiceCard icon={<FaBolt />} title="Electrician" />
            <ServiceCard icon={<FaWrench />} title="Plumber" />
            <ServiceCard icon={<FaTools />} title="Carpenter" />
            <ServiceCard icon={<FaSnowflake />} title="AC Repair" />
            <ServiceCard icon={<FaPaintRoller />} title="Painter" />
            <ServiceCard icon={<FaBroom />} title="Cleaning" />
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">

          {/* ILLUSTRATION */}
          <img
            src="https://undraw.co/api/illustrations/online_booking_re_gw4f.svg"
            alt="Booking process illustration"
            className="w-full max-w-md mx-auto"
          />

          <div>
            <h2 className="text-2xl font-bold mb-8">
              How Karigar Works
            </h2>

            <ul className="space-y-6 text-gray-700">
              <li>
                <strong>1. Choose a Service</strong><br />
                Browse verified local professionals near you.
              </li>
              <li>
                <strong>2. Request Instantly</strong><br />
                Send a booking request in just a few clicks.
              </li>
              <li>
                <strong>3. Get It Done</strong><br />
                Sit back while the job gets completed professionally.
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-slate-900 text-white py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold mb-4">
            Ready to get started?
          </h2>
          <p className="text-slate-300 mb-8">
            Join Karigar today and experience hassle-free local services.
          </p>

          <Link
            to="/login"
            className="inline-block bg-green-500 hover:bg-green-600 text-white px-8 py-3 rounded-lg font-semibold transition"
          >
            Explore Services
          </Link>
        </div>
      </section>

      {/* FOOTER / WORDMARK */}
      <footer className="bg-slate-950 text-slate-400 py-6 mt-auto">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-sm tracking-wide">
            Made by{" "}
            <span className="font-semibold text-slate-200">
              Boys Unfiltered Team
            </span>
          </p>
        </div>
      </footer>
    </div>
  );
}

/* ---------------- SERVICE CARD ---------------- */

function ServiceCard({ icon, title }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-lg transition text-center">
      <div className="text-green-600 text-3xl mb-4 flex justify-center">
        {icon}
      </div>
      <p className="font-semibold">{title}</p>
    </div>
  );
}

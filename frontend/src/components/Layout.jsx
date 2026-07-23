import Navbar from './Navbar'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />
      <main className="mx-auto flex w-full max-w-6xl flex-col px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 rounded-2xl border border-slate-200 bg-white px-6 py-5 shadow-sm">
          <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-blue-600">
            Academic Research Assistant
          </p>
          <div className="mt-2 h-px w-16 bg-slate-200" />
        </div>
        {children}
      </main>
    </div>
  )
}
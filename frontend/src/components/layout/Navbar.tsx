import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex flex-shrink-0 items-center">
              <Link href="/" className="text-xl font-bold text-primary-600">
                YouTube LabelBase
              </Link>
            </div>
          </div>
          {/* <div className="flex items-center">
            <Link
              href="/about"
              className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
            >
              About
            </Link>
          </div> */}
        </div>
      </div>
    </nav>
  );
} 
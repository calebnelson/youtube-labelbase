import Navbar from '@/components/layout/Navbar';
import VideoInputForm from '@/components/video/VideoInputForm';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="mx-auto max-w-3xl">
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                YouTube Video Analysis
              </h1>
              <VideoInputForm />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

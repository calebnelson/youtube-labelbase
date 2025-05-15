'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { runPrompt, type runPromptResponse } from '@/services/api';

const videoInputSchema = z.object({
  videoUrl: z.string().url('Please enter a valid YouTube URL'),
  systemPrompt: z.string().min(1, 'System prompt is required'),
  userPrompt: z.string().min(1, 'User prompt is required'),
});

type VideoInputFormData = z.infer<typeof videoInputSchema>;

export default function VideoInputForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<runPromptResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<VideoInputFormData>({
    resolver: zodResolver(videoInputSchema),
  });

  const onSubmit = async (data: VideoInputFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await runPrompt({
        videoUrl: data.videoUrl,
        prompt: {
          systemPrompt: data.systemPrompt,
          userPrompt: data.userPrompt,
        },
      });
      setResponse(response);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label
            htmlFor="videoUrl"
            className="block text-sm font-medium text-gray-700"
          >
            YouTube Video URL
          </label>
          <div className="mt-1">
            <input
              type="text"
              id="videoUrl"
              className="input-primary"
              placeholder="https://www.youtube.com/watch?v=I8h1GLqYr1Y"
              {...register('videoUrl')}
            />
            {errors.videoUrl && (
              <p className="mt-1 text-sm text-red-600">{errors.videoUrl.message}</p>
            )}
          </div>
        </div>

        <div>
          <label
            htmlFor="systemPrompt"
            className="block text-sm font-medium text-gray-700"
          >
            System Prompt
          </label>
          <div className="mt-1">
            <textarea
              id="systemPrompt"
              className="input-primary min-h-[100px]"
              placeholder="Enter the system prompt..."
              {...register('systemPrompt')}
            />
            {errors.systemPrompt && (
              <p className="mt-1 text-sm text-red-600">{errors.systemPrompt.message}</p>
            )}
          </div>
        </div>

        <div>
          <label
            htmlFor="userPrompt"
            className="block text-sm font-medium text-gray-700"
          >
            User Prompt
          </label>
          <div className="mt-1">
            <textarea
              id="userPrompt"
              className="input-primary min-h-[100px]"
              placeholder="Enter the user prompt..."
              {...register('userPrompt')}
            />
            {errors.userPrompt && (
              <p className="mt-1 text-sm text-red-600">{errors.userPrompt.message}</p>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="btn-primary w-full"
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Run Prompt'}
        </button>
      </form>

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {response && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Prompt Executed</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>Prompt ID: {response.promptId}</p>
                <p>Output: {JSON.stringify(response.output, null, 2)}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 
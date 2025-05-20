"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  runPrompt,
  type runPromptResponse,
  getPrompts,
  getVideos,
} from "@/services/api";
import { Video, Prompt } from "@/utils/types";

const videoInputSchema = z.object({
  videoUrl: z.string().url("Please enter a valid YouTube URL"),
  prompt: z.string().min(1, "Prompt is required"),
});

type VideoInputFormData = z.infer<typeof videoInputSchema>;

type InputMode = "new" | "existing";

export default function VideoInputForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [response, setResponse] = useState<runPromptResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [videoMode, setVideoMode] = useState<InputMode>("new");
  const [promptMode, setPromptMode] = useState<InputMode>("new");
  const [existingVideos, setExistingVideos] = useState<Video[]>([]);
  const [existingPrompts, setExistingPrompts] = useState<Prompt[]>([]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<VideoInputFormData>({
    resolver: zodResolver(videoInputSchema),
  });

  useEffect(() => {
    const fetchExistingData = async () => {
      setIsLoadingData(true);
      try {
        console.log('Fetching videos and prompts...');
        const [videosResponse, promptsResponse] = await Promise.all([
          getVideos(),
          getPrompts(),
        ]);
        
        console.log('Videos Response:', videosResponse);
        console.log('Prompts Response:', promptsResponse);
        
        if (!videosResponse?.videos) {
          console.error('No videos array in response:', videosResponse);
        }
        if (!promptsResponse?.prompts) {
          console.error('No prompts array in response:', promptsResponse);
        }

        setExistingVideos(videosResponse?.videos || []);
        setExistingPrompts(promptsResponse?.prompts || []);
        
        console.log('Set videos:', videosResponse?.videos || []);
        console.log('Set prompts:', promptsResponse?.prompts || []);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError("Failed to load existing videos and prompts");
      } finally {
        setIsLoadingData(false);
      }
    };
    fetchExistingData();
  }, []);

  const onSubmit = async (data: VideoInputFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await runPrompt({
        videoUrl: data.videoUrl,
        prompt: data.prompt,
      });
      setResponse(response);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleVideoSelect = (videoId: string) => {
    console.log('Selected video ID:', videoId);
    console.log('Available videos:', existingVideos);
    const selectedVideo = existingVideos.find((v) => v.id.toString() === videoId);
    console.log('Selected video:', selectedVideo);
    if (selectedVideo) {
      setValue(
        "videoUrl",
        `https://www.youtube.com/watch?v=${selectedVideo.youtube_id}`
      );
    }
  };

  const handlePromptSelect = (promptId: string) => {
    console.log('Selected prompt ID:', promptId);
    console.log('Available prompts:', existingPrompts);
    const selectedPrompt = existingPrompts.find((p) => p.id === promptId);
    console.log('Selected prompt:', selectedPrompt);
    if (selectedPrompt) {
      setValue("prompt", selectedPrompt.user_prompt);
    }
  };

  if (isLoadingData) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="text-gray-500">Loading existing videos and prompts...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <div className="flex items-center space-x-4 mb-2">
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                checked={videoMode === "new"}
                onChange={() => setVideoMode("new")}
              />
              <span className="ml-2">New Video</span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                checked={videoMode === "existing"}
                onChange={() => setVideoMode("existing")}
              />
              <span className="ml-2">Existing Video</span>
            </label>
          </div>

          {videoMode === "new" ? (
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
                  {...register("videoUrl")}
                />
                {errors.videoUrl && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.videoUrl.message}
                  </p>
                )}
              </div>
            </div>
          ) : (
            <div>
              <label
                htmlFor="existingVideo"
                className="block text-sm font-medium text-gray-700"
              >
                Select Existing Video
              </label>
              <div className="mt-1">
                <select
                  id="existingVideo"
                  className="input-primary"
                  onChange={(e) => handleVideoSelect(e.target.value)}
                >
                  <option value="">Select a video...</option>
                  {existingVideos && existingVideos.length > 0 ? (
                    existingVideos.map((video) => (
                      <option key={video.id} value={video.id}>
                        {video.title ? `${video.title} (${video.youtube_id})` : `Video ${video.youtube_id}`}
                      </option>
                    ))
                  ) : (
                    <option value="" disabled>No existing videos found</option>
                  )}
                </select>
              </div>
            </div>
          )}
        </div>

        <div>
          <div className="flex items-center space-x-4 mb-2">
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                checked={promptMode === "new"}
                onChange={() => setPromptMode("new")}
              />
              <span className="ml-2">New Prompt</span>
            </label>
            <label className="inline-flex items-center">
              <input
                type="radio"
                className="form-radio"
                checked={promptMode === "existing"}
                onChange={() => setPromptMode("existing")}
              />
              <span className="ml-2">Existing Prompt</span>
            </label>
          </div>

          {promptMode === "new" ? (
            <div>
              <label
                htmlFor="prompt"
                className="block text-sm font-medium text-gray-700"
              >
                Prompt
              </label>
              <div className="mt-1">
                <textarea
                  id="prompt"
                  className="input-primary min-h-[200px]"
                  placeholder="Enter your prompt..."
                  {...register("prompt")}
                />
                {errors.prompt && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.prompt.message}
                  </p>
                )}
              </div>
            </div>
          ) : (
            <div>
              <label
                htmlFor="existingPrompt"
                className="block text-sm font-medium text-gray-700"
              >
                Select Existing Prompt
              </label>
              <div className="mt-1">
                <select
                  id="existingPrompt"
                  className="input-primary"
                  onChange={(e) => handlePromptSelect(e.target.value)}
                >
                  <option value="">Select a prompt...</option>
                  {existingPrompts && existingPrompts.length > 0 ? (
                    existingPrompts.map((prompt) => (
                      <option key={prompt.id} value={prompt.id}>
                        {prompt.user_prompt.substring(0, 100)}...
                      </option>
                    ))
                  ) : (
                    <option value="" disabled>No existing prompts found</option>
                  )}
                </select>
              </div>
            </div>
          )}
        </div>

        <button
          type="submit"
          className="btn-primary w-full"
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Run Prompt"}
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
              <h3 className="text-sm font-medium text-green-800">
                Prompt Executed
              </h3>
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

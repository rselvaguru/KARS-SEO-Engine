import React, { useState } from "react";

interface PipelineComponentProps {
  onRunPipeline: (topic: string, count: number) => Promise<void>;
  loading: boolean;
}

export default function PipelineComponent({
  onRunPipeline,
  loading,
}: PipelineComponentProps) {
  const [topic, setTopic] = useState("");
  const [articleCount, setArticleCount] = useState(5);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!topic.trim()) {
      setError("Please enter a topic");
      return;
    }

    if (articleCount < 1 || articleCount > 20) {
      setError("Article count must be between 1 and 20");
      return;
    }

    try {
      await onRunPipeline(topic.trim(), articleCount);
      setTopic("");
      setArticleCount(5);
    } catch (err: any) {
      setError(err.message || "Failed to run pipeline");
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-slate-200">
      <h2 className="text-xl font-bold text-slate-800 mb-2 flex items-center gap-2">
        🔁 SEO Pipeline
      </h2>
      <p className="text-xs text-slate-500 mb-6">Full automation: clusters → keywords → content → linking</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Main Topic
          </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={loading}
            placeholder="e.g., Machine Learning..."
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-slate-100"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Articles to Generate: {articleCount}
          </label>
          <input
            type="range"
            min="1"
            max="20"
            value={articleCount}
            onChange={(e) => setArticleCount(parseInt(e.target.value))}
            disabled={loading}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm flex items-start gap-2">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !topic.trim()}
          className="w-full bg-gradient-to-r from-indigo-500 to-blue-500 hover:shadow-lg text-white font-bold py-3 px-4 rounded-lg transition-all disabled:bg-slate-300 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="inline-block animate-spin">⟳</span>
              <span>Pipeline Running...</span>
            </>
          ) : (
            <>
              <span>⚙️ Run Pipeline</span>
            </>
          )}
        </button>

        {loading && (
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 text-center">
            <p className="text-xs text-indigo-800 font-medium">
              🤖 Running full automation pipeline...
            </p>
            <ul className="text-xs text-indigo-600 mt-2 space-y-1 text-left ml-4 list-disc">
              <li>Analyzing keywords</li>
              <li>Generating content</li>
              <li>Optimizing for SEO</li>
              <li>Building links</li>
              <li>Storing in vector DB</li>
            </ul>
          </div>
        )}
      </form>
    </div>
  );
}

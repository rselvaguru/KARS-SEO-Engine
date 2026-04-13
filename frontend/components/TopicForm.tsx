import React, { useState } from "react";

interface TopicFormProps {
  onSubmit: (topic: string) => Promise<void>;
  loading: boolean;
}

export default function TopicForm({ onSubmit, loading }: TopicFormProps) {
  const [topic, setTopic] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!topic.trim()) {
      setError("Please enter a topic");
      return;
    }

    if (topic.trim().length < 3) {
      setError("Topic must be at least 3 characters");
      return;
    }

    try {
      await onSubmit(topic.trim());
      setTopic("");
    } catch (err: any) {
      setError(err.message || "An error occurred");
    }
  };

  const charCount = topic.length;
  const charLimit = 255;
  const charPercentage = (charCount / charLimit) * 100;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 h-fit sticky top-24 border border-slate-200">
      <h2 className="text-xl font-bold text-slate-800 mb-2 flex items-center gap-2">
        ✍️ New Content
      </h2>
      <p className="text-xs text-slate-500 mb-6">Generate AI-optimized content</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Topic or Keyword
          </label>
          <textarea
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={loading}
            placeholder="e.g., Machine Learning for Beginners, Digital Marketing Tips..."
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none disabled:bg-slate-100 disabled:cursor-not-allowed"
            rows={4}
          />
          
          {/* Character Count Bar */}
          <div className="mt-2">
            <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${
                  charPercentage > 90
                    ? "bg-red-500"
                    : charPercentage > 70
                      ? "bg-yellow-500"
                      : "bg-green-500"
                }`}
                style={{ width: `${Math.min(charPercentage, 100)}%` }}
              />
            </div>
            <p className={`text-xs mt-1 ${
              charPercentage > 90
                ? "text-red-600"
                : charPercentage > 70
                  ? "text-yellow-600"
                  : "text-slate-500"
            }`}>
              {charCount}/{charLimit} characters
            </p>
          </div>
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
          className="w-full bg-gradient-to-r from-primary to-secondary hover:shadow-lg text-white font-bold py-3 px-4 rounded-lg transition-all disabled:bg-slate-300 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="inline-block animate-spin">⟳</span>
              <span>Generating...</span>
              <span className="text-xs opacity-75">(30-60s)</span>
            </>
          ) : (
            <>
              <span>✨ Generate</span>
            </>
          )}
        </button>

        {loading && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-center">
            <p className="text-xs text-blue-800 font-medium">
              🤖 AI is working on your content...
            </p>
            <p className="text-xs text-blue-600 mt-1">
              This may take up to 60 seconds on first run
            </p>
          </div>
        )}

        <div className="bg-teal-50 border border-teal-200 rounded-lg p-4">
          <p className="text-xs font-semibold text-teal-800 mb-2">
            📋 AI will generate:
          </p>
          <ul className="text-xs text-teal-800 space-y-1 ml-4 list-disc">
            <li>SEO-optimized title & meta tags</li>
            <li>Well-structured content with headings</li>
            <li>Internal links to related articles</li>
            <li>FAQ section with answers</li>
            <li>SEO score (0-100)</li>
          </ul>
        </div>
      </form>
    </div>
  );
}

import React, { useState } from "react";
import { ContentData } from "../services/api";

interface ContentCardProps {
  content: ContentData;
  onDelete: (id: number) => Promise<void>;
  onRegenerate?: () => Promise<void>;
}

export default function ContentCard({
  content,
  onDelete,
  onRegenerate,
}: ContentCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [showFullContent, setShowFullContent] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleDelete = async () => {
    if (
      !window.confirm(
        "Are you sure you want to delete this content?"
      )
    ) {
      return;
    }

    try {
      setIsDeleting(true);
      await onDelete(content.id);
    } catch (err) {
      alert("Failed to delete content");
    } finally {
      setIsDeleting(false);
    }
  };

  const handleRegenerate = async () => {
    if (onRegenerate) {
      try {
        setIsRegenerating(true);
        await onRegenerate();
      } catch (err) {
        alert("Failed to regenerate content");
      } finally {
        setIsRegenerating(false);
      }
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSEOScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600 bg-green-50";
    if (score >= 60) return "text-yellow-600 bg-yellow-50";
    return "text-red-600 bg-red-50";
  };

  const getSEOScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    return "Needs Improvement";
  };

  const contentPreview = content.content.substring(0, 300);
  const displayContent = showFullContent
    ? content.content
    : contentPreview;

  const formattedDate = new Date(
    content.created_at
  ).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden border border-slate-200">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary to-secondary text-white p-6">
        <div className="flex justify-between items-start gap-4">
          <div className="flex-1">
            <h3 className="text-2xl font-bold mb-2">{content.title}</h3>
            <p className="text-teal-50 text-sm">
              Topic: <strong>{content.topic}</strong>
            </p>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-bold ${getSEOScoreColor(content.seo_score)}`}>
            {content.seo_score}
          </div>
        </div>
      </div>

      {/* SEO Score Badge */}
      <div className="px-6 py-3 bg-slate-50 border-b border-slate-200">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-xs text-slate-600 mb-1">SEO Score</p>
            <div className="flex items-center gap-2">
              <div className="h-2 w-32 bg-slate-200 rounded-full">
                <div
                  className={`h-full rounded-full transition-all ${
                    content.seo_score >= 80
                      ? "bg-green-500"
                      : content.seo_score >= 60
                        ? "bg-yellow-500"
                        : "bg-red-500"
                  }`}
                  style={{ width: `${content.seo_score}%` }}
                />
              </div>
              <span className="text-sm font-semibold">
                {getSEOScoreLabel(content.seo_score)}
              </span>
            </div>
          </div>
          <span className="text-xs text-slate-600">{formattedDate}</span>
        </div>
      </div>

      {/* Meta Information */}
      <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 space-y-3">
        <div>
          <p className="text-xs font-semibold text-slate-600 mb-1">
            Meta Title ({content.meta_title.length}/60)
          </p>
          <div className="flex justify-between items-start">
            <p className="text-sm text-slate-800 break-words flex-1">
              {content.meta_title}
            </p>
            <button
              onClick={() => handleCopy(content.meta_title)}
              className="ml-2 p-1 hover:bg-slate-200 rounded transition-colors"
              title="Copy to clipboard"
            >
              📋
            </button>
          </div>
        </div>

        <div>
          <p className="text-xs font-semibold text-slate-600 mb-1">
            Meta Description ({content.meta_description.length}/160)
          </p>
          <div className="flex justify-between items-start">
            <p className="text-sm text-slate-800 break-words flex-1">
              {content.meta_description}
            </p>
            <button
              onClick={() => handleCopy(content.meta_description)}
              className="ml-2 p-1 hover:bg-slate-200 rounded transition-colors"
              title="Copy to clipboard"
            >
              📋
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-6 py-6">
        <div className="max-h-96 overflow-y-auto">
          <div className="prose prose-sm max-w-none text-slate-700">
            <pre className="bg-slate-100 p-4 rounded-lg overflow-x-auto text-xs whitespace-pre-wrap break-words">
              {displayContent}
              {!showFullContent &&
                content.content.length > 300 &&
                "..."}
            </pre>
          </div>
        </div>

        {content.content.length > 300 && (
          <button
            onClick={() => setShowFullContent(!showFullContent)}
            className="mt-4 text-primary hover:text-secondary font-semibold text-sm transition-colors"
          >
            {showFullContent ? "Show Less" : "Show More"}
          </button>
        )}
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-4 border-t border-slate-200 grid grid-cols-2 gap-3">
        <button
          onClick={() => handleCopy(content.content)}
          className={`flex items-center justify-center gap-2 font-medium py-2 px-4 rounded-lg transition-colors ${
            copied
              ? "bg-green-500 text-white"
              : "bg-blue-500 hover:bg-blue-600 text-white"
          }`}
        >
          {copied ? "✓ Copied" : "📋 Copy"}
        </button>

        {onRegenerate && (
          <button
            onClick={handleRegenerate}
            disabled={isRegenerating}
            className={`flex items-center justify-center gap-2 font-medium py-2 px-4 rounded-lg transition-colors ${
              isRegenerating
                ? "bg-yellow-300 text-yellow-800 cursor-wait"
                : "bg-orange-500 hover:bg-orange-600 text-white"
            }`}
          >
            {isRegenerating ? (
              <>
                <span className="inline-block animate-spin">⟳</span> Generating...
              </>
            ) : (
              <>
                🔄 Regenerate
              </>
            )}
          </button>
        )}
      </div>

      {/* Delete Button */}
      <div className="px-6 py-3 border-t border-slate-200">
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-lg transition-colors disabled:bg-slate-300 disabled:cursor-not-allowed"
        >
          {isDeleting ? "Deleting..." : "🗑️ Delete"}
        </button>
      </div>
    </div>
  );
}

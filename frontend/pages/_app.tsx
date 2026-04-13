import React, { useState, useEffect } from "react";
import Head from "next/head";
import TopicForm from "../components/TopicForm";
import ContentCard from "../components/ContentCard";
import BulkGenerator from "../components/BulkGenerator";
import PipelineComponent from "../components/PipelineComponent";
import APIClient, { ContentData } from "../services/api";
import "../styles/globals.css";

type TabType = "single" | "bulk" | "pipeline" | "history";

export default function App() {
  const [contents, setContents] = useState<ContentData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generatedContent, setGeneratedContent] = useState<ContentData | null>(null);
  const [backendStatus, setBackendStatus] = useState<string>("checking");
  const [activeTab, setActiveTab] = useState<TabType>("single");
  const [vectorDBStats, setVectorDBStats] = useState<any>(null);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
    fetchContents();
    fetchVectorDBStats();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const health = await APIClient.healthCheck();
      if (health.status === "healthy") {
        setBackendStatus("healthy");
        setError(null);
      } else {
        setBackendStatus("unhealthy");
      }
    } catch (err) {
      setBackendStatus("unreachable");
      setError(
        "Cannot connect to backend. Ensure backend is running on http://localhost:8000"
      );
    }
  };

  const fetchContents = async () => {
    try {
      const response = await APIClient.getAllContent(0, 100);
      if (response.success) {
        setContents(response.data);
      }
    } catch (err) {
      console.error("Error fetching contents:", err);
    }
  };

  const fetchVectorDBStats = async () => {
    try {
      const response = await APIClient.getVectorDBStatus();
      if (response.success) {
        setVectorDBStats(response.vector_db);
      }
    } catch (err) {
      console.error("Error fetching vector DB stats:", err);
    }
  };

  const handleGenerateContent = async (topic: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await APIClient.generateContent(topic);

      if (response.success && response.data) {
        setGeneratedContent(response.data);
        fetchContents();
      } else {
        setError(response.error || "Failed to generate content");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred while generating content");
    } finally {
      setLoading(false);
    }
  };

  const handleBulkGeneration = async (topic: string, count: number) => {
    try {
      setLoading(true);
      setError(null);
      const response = await APIClient.generateBulkContent(topic, count);

      if (response.success) {
        setGeneratedContent(null);
        setError(`Generated ${response.total_generated} articles!`);
        fetchContents();
        fetchVectorDBStats();
      } else {
        setError(response.error || "Failed to generate bulk content");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleRunPipeline = async (topic: string, count: number) => {
    try {
      setLoading(true);
      setError(null);
      const response = await APIClient.runPipeline(topic, count);

      if (response.success) {
        setGeneratedContent(null);
        const stats = response.pipeline?.stats || {};
        setError(
          `Pipeline completed: ${stats.total_articles} articles generated!`
        );
        fetchContents();
        fetchVectorDBStats();
      } else {
        setError(response.error || "Failed to run pipeline");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteContent = async (id: number) => {
    try {
      await APIClient.deleteContent(id);
      setContents(contents.filter((c) => c.id !== id));
      if (generatedContent?.id === id) {
        setGeneratedContent(null);
      }
    } catch (err) {
      setError("Failed to delete content");
    }
  };

  const handleSelectContent = (content: ContentData) => {
    setGeneratedContent(content);
    setActiveTab("single");
  };

  const handleReset = () => {
    setGeneratedContent(null);
    setError(null);
  };

  return (
    <>
      <Head>
        <title>KARS SEO Engine v2.0 - AI SEO Automation</title>
        <meta
          name="description"
          content="AI-powered SEO automation platform with bulk generation and semantic linking"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <link rel="apple-touch-icon" href="/favicon.svg" />
      </Head>

      <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
        {/* Header */}
        <header className="bg-white shadow-md border-b border-slate-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                
                <div>
                  <h1 className="text-2xl font-bold text-primary">KARS SEO Engine v2.0</h1>
                  <p className="text-slate-600 text-xs mt-0.5">
                    AI Automation with Semantic Linking
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div
                    className={`h-3 w-3 rounded-full ${
                      backendStatus === "healthy"
                        ? "bg-green-500"
                        : backendStatus === "unhealthy"
                          ? "bg-yellow-500"
                          : "bg-red-500"
                    }`}
                  />
                  <span className="text-xs text-slate-600 capitalize">
                    {backendStatus}
                  </span>
                </div>
                {vectorDBStats && (
                  <div className="text-xs bg-teal-50 text-teal-700 px-3 py-1 rounded-full">
                    🧠 {vectorDBStats.documents} indexed
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Tab Navigation */}
        <div className="bg-white border-b border-slate-200 sticky top-20 z-40">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex gap-2 overflow-x-auto">
              <button
                onClick={() => setActiveTab("single")}
                className={`py-3 px-4 text-sm font-medium transition-all whitespace-nowrap ${
                  activeTab === "single"
                    ? "border-b-2 border-primary text-primary"
                    : "text-slate-600 hover:text-slate-800"
                }`}
              >
                ✨ Single Article
              </button>
              <button
                onClick={() => setActiveTab("bulk")}
                className={`py-3 px-4 text-sm font-medium transition-all whitespace-nowrap ${
                  activeTab === "bulk"
                    ? "border-b-2 border-purple-500 text-purple-600"
                    : "text-slate-600 hover:text-slate-800"
                }`}
              >
                🚀 Bulk Generation
              </button>
              <button
                onClick={() => setActiveTab("pipeline")}
                className={`py-3 px-4 text-sm font-medium transition-all whitespace-nowrap ${
                  activeTab === "pipeline"
                    ? "border-b-2 border-indigo-500 text-indigo-600"
                    : "text-slate-600 hover:text-slate-800"
                }`}
              >
                🔁 Pipeline
              </button>
              <button
                onClick={() => setActiveTab("history")}
                className={`py-3 px-4 text-sm font-medium transition-all whitespace-nowrap ${
                  activeTab === "history"
                    ? "border-b-2 border-amber-500 text-amber-600"
                    : "text-slate-600 hover:text-slate-800"
                }`}
              >
                📚 History ({contents.length})
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Error Alert */}
          {error && !error.includes("Generated") && !error.includes("completed") && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
              <div className="flex">
                <span>⚠️</span>
                <p className="ml-2">{error}</p>
              </div>
            </div>
          )}

          {/* Success Alert */}
          {error && (error.includes("Generated") || error.includes("completed")) && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm">
              <div className="flex">
                <span>✓</span>
                <p className="ml-2">{error}</p>
              </div>
            </div>
          )}

          {/* Single Article Tab */}
          {activeTab === "single" && (
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                <TopicForm
                  onSubmit={handleGenerateContent}
                  loading={loading}
                />
              </div>

              <div className="lg:col-span-2">
                {loading ? (
                  <div className="flex justify-center items-center h-96 bg-white rounded-lg shadow">
                    <div className="text-center">
                      <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                      <p className="mt-4 text-slate-600 font-medium">
                        Generating content...
                      </p>
                      <p className="text-sm text-slate-500 mt-1">
                        This may take 30-60 seconds
                      </p>
                    </div>
                  </div>
                ) : generatedContent ? (
                  <div>
                    <ContentCard
                      content={generatedContent}
                      onDelete={handleDeleteContent}
                      onRegenerate={() => handleGenerateContent(generatedContent.topic)}
                    />
                    <button
                      onClick={handleReset}
                      className="mt-4 w-full bg-slate-200 hover:bg-slate-300 text-slate-800 font-medium py-2 px-4 rounded-lg transition-colors"
                    >
                      ← Back to Form
                    </button>
                  </div>
                ) : (
                  <div className="bg-white rounded-lg shadow-md p-8 text-center h-96 flex flex-col items-center justify-center">
                    <h3 className="text-xl font-semibold text-slate-800 mb-2">
                      Generate Single Article
                    </h3>
                    <p className="text-slate-600 mb-6">
                      Enter a topic on the left for standard content generation
                    </p>
                  </div>
                )}
              </div>

              <div className="lg:col-span-1">
                <div className="bg-white rounded-lg shadow-md p-4 sticky top-40">
                  <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                    📚 History
                  </h2>
                  {contents.length > 0 ? (
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                      {[...contents].reverse().map((content) => (
                        <button
                          key={content.id}
                          onClick={() => handleSelectContent(content)}
                          className={`w-full text-left p-3 rounded-lg transition-all text-sm ${
                            generatedContent?.id === content.id
                              ? "bg-primary text-white shadow-md"
                              : "bg-slate-50 hover:bg-slate-100 text-slate-800"
                          }`}
                        >
                          <p className="font-medium truncate">{content.topic}</p>
                          <p className={`text-xs mt-1 ${
                            generatedContent?.id === content.id
                              ? "text-teal-100"
                              : "text-slate-500"
                          }`}>
                            {content.seo_score}/100
                          </p>
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-slate-600 text-sm text-center py-8">
                      No content yet
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Bulk Generation Tab */}
          {activeTab === "bulk" && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <BulkGenerator
                  onStartGeneration={handleBulkGeneration}
                  loading={loading}
                />
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-bold text-slate-800 mb-4">
                  📊 How Bulk Generation Works
                </h3>
                <div className="space-y-3 text-sm text-slate-600">
                  <div className="flex gap-3">
                    <span className="text-lg">1️⃣</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Keyword Clustering
                      </p>
                      <p className="text-xs">
                        AI analyzes your topic and creates keyword clusters by
                        search intent
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">2️⃣</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Parallel Generation
                      </p>
                      <p className="text-xs">
                        Content is generated for each keyword independently
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">3️⃣</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        SEO Optimization
                      </p>
                      <p className="text-xs">
                        Each article is optimized with titles, meta tags, and
                        scores
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">4️⃣</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Semantic Linking
                      </p>
                      <p className="text-xs">
                        Automatically link related articles using vector
                        embeddings
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Pipeline Tab */}
          {activeTab === "pipeline" && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <PipelineComponent
                  onRunPipeline={handleRunPipeline}
                  loading={loading}
                />
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-bold text-slate-800 mb-4">
                  🔁 Pipeline Workflow
                </h3>
                <div className="space-y-3 text-sm text-slate-600">
                  <div className="flex gap-3">
                    <span className="text-lg">🧠</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Keyword Intelligence
                      </p>
                      <p className="text-xs">
                        Cluster keywords by informational, transactional, and
                        navigational intent
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">✍️</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Content Generation
                      </p>
                      <p className="text-xs">
                        Generate unique, SEO-optimized content for each keyword
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">📊</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Semantic Linking
                      </p>
                      <p className="text-xs">
                        Connect articles using AI-powered vector embeddings
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <span className="text-lg">💾</span>
                    <div>
                      <p className="font-medium text-slate-800">
                        Storage & Indexing
                      </p>
                      <p className="text-xs">
                        Store in database and vector DB for future queries
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* History Tab */}
          {activeTab === "history" && (
            <div>
              <h2 className="text-2xl font-bold text-slate-800 mb-6">
                All Generated Content ({contents.length})
              </h2>
              {contents.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[...contents].reverse().map((content) => (
                    <ContentCard
                      key={content.id}
                      content={content}
                      onDelete={handleDeleteContent}
                      onRegenerate={() => handleGenerateContent(content.topic)}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-slate-600">
                    No content generated yet. Start creating!
                  </p>
                </div>
              )}
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-slate-600 text-sm">
              <p>✨ KARS SEO Engine v2.0 | AI Automation with Semantic Linking</p>
              <p className="mt-2">
                🔗 Backend: http://localhost:8000 | 🧠 Vector DB: ChromaDB
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}

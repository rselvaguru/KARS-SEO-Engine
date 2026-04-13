/**
 * API Service Client
 * Handles all HTTP requests to the FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ContentData {
  id: number;
  topic: string;
  title: string;
  content: string;
  meta_title: string;
  meta_description: string;
  seo_score: number;
  created_at: string;
}

export interface GenerateResponse {
  success: boolean;
  message: string;
  data?: ContentData;
  error?: string;
}

export interface AllContentResponse {
  success: boolean;
  total: number;
  data: ContentData[];
}

class APIClient {
  /**
   * Generate SEO content for a topic
   */
  static async generateContent(topic: string): Promise<GenerateResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate content");
      }

      return await response.json();
    } catch (error) {
      console.error("Error generating content:", error);
      throw error;
    }
  }

  /**
   * Fetch all generated content
   */
  static async getAllContent(
    skip: number = 0,
    limit: number = 10
  ): Promise<AllContentResponse> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/content?skip=${skip}&limit=${limit}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch content");
      }

      return await response.json();
    } catch (error) {
      console.error("Error fetching content:", error);
      throw error;
    }
  }

  /**
   * Fetch a specific content by ID
   */
  static async getContentById(id: number): Promise<GenerateResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/content/${id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch content");
      }

      return await response.json();
    } catch (error) {
      console.error("Error fetching content:", error);
      throw error;
    }
  }

  /**
   * Delete content by ID
   */
  static async deleteContent(id: number): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/content/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete content");
      }

      return await response.json();
    } catch (error) {
      console.error("Error deleting content:", error);
      throw error;
    }
  }

  /**
   * Check backend health
   */
  static async healthCheck(): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      return await response.json();
    } catch (error) {
      console.error("Health check failed:", error);
      return { status: "unavailable" };
    }
  }

  /**
   * Generate keyword clusters for a topic
   */
  static async generateKeywordClusters(topic: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/keyword-clusters`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate keyword clusters");
      }

      return await response.json();
    } catch (error) {
      console.error("Error generating keyword clusters:", error);
      throw error;
    }
  }

  /**
   * Generate multiple articles in bulk
   */
  static async generateBulkContent(
    topic: string,
    num_articles: number = 5
  ): Promise<any> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/generate-bulk?num_articles=${num_articles}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ topic }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate bulk content");
      }

      return await response.json();
    } catch (error) {
      console.error("Error generating bulk content:", error);
      throw error;
    }
  }

  /**
   * Run complete SEO pipeline
   */
  static async runPipeline(topic: string, num_articles: number = 5): Promise<any> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/pipeline?num_articles=${num_articles}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ topic }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to run pipeline");
      }

      return await response.json();
    } catch (error) {
      console.error("Error running pipeline:", error);
      throw error;
    }
  }

  /**
   * Get vector DB status
   */
  static async getVectorDBStatus(): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/vector-db/status`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to get vector DB status");
      }

      return await response.json();
    } catch (error) {
      console.error("Error getting vector DB status:", error);
      return { success: false };
    }
  }
}

export default APIClient;
